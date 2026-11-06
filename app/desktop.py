"""ins排版台: a desktop window around the layout engine.

Double-click the desktop icon, drag photos in, answer one multiple-choice question per photo (A-D, E = show me four
others), press submit.  The picks are copied to the Desktop and recorded in the taste log, so the next round leans
toward them.  Everything stays on this machine: the server listens on 127.0.0.1 only.

  pythonw app/desktop.py
"""
import datetime as dt
import json
import os
import queue
import shutil
import subprocess
import sys
import threading
import time
import traceback
import urllib.request
import uuid
import webbrowser
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, unquote, urlparse

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

PORT = 8831
ORIGIN = f"http://127.0.0.1:{PORT}"
BASE = Path(os.environ.get("LOCALAPPDATA") or Path.home() / ".local" / "share") / "InsLayoutApp"
SESSIONS = BASE / "sessions"
LETTERS = "ABCD"
SIZE = (1080, 1350)
EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp", ".heic", ".heif"}

lock = threading.Lock()
jobs = queue.Queue()
state = {"photos": [], "done": None, "engine": "starting"}
files = {}  # url path -> file on disk; nothing else is ever served
session_dir = SESSIONS / uuid.uuid4().hex
last_seen = None
window_closing_at = None


def desktop_dir():
    if sys.platform == "win32":
        import ctypes
        buf = ctypes.create_unicode_buffer(260)
        if ctypes.windll.shell32.SHGetFolderPathW(0, 0x10, 0, 0, buf) == 0:  # follows a redirected Desktop
            return Path(buf.value)
    return Path.home() / "Desktop"


def find_photo(pid):
    return next((p for p in state["photos"] if p["id"] == pid), None)


def worker():
    """All rendering stays on this one thread: the Playwright browser belongs to the thread that opened it."""
    try:
        from PIL import Image, ImageOps
        from components import render as engine
        from scripts.recommend import recommend
        from scripts.render import render_one
    except Exception:  # noqa
        with lock:
            state["engine"] = "failed: " + traceback.format_exc(limit=1)[-300:]
        return
    with lock:
        state["engine"] = "ready"
    while True:
        pid = jobs.get()
        if pid is None:
            engine.close()
            return
        with lock:
            p = find_photo(pid)
            if not p:
                continue
            p["status"] = "working"
            used = {i for q in state["photos"] for i in q["shown"]}
            shown = list(p["shown"])
            round_no = p["round"]
        try:
            src = Path(p["path"])
            picks = recommend([str(src)], 4, used)[0]["candidates"]
            if len(picks) < 4:  # the pool ran out across this batch: only avoid what this photo has shown
                picks = recommend([str(src)], 4, shown)[0]["candidates"]
            if not picks:
                raise RuntimeError("no layouts left")
            out = src.parent / f"round{round_no}"
            for c in picks:
                try:
                    png = render_one(c["id"], [str(src)], out, size=SIZE)
                except Exception:  # noqa  one bad layout must not lose the whole question
                    traceback.print_exc()
                    continue
                with lock:
                    if find_photo(pid) is not p or p["round"] != round_no:
                        break
                    letter = LETTERS[len(p["cands"])]
                    url = f"/file/{pid}/{round_no}/{letter}.png"
                    files[url] = png
                    p["cands"].append({"letter": letter, "id": c["id"], "url": url})
                    p["shown"].append(c["id"])
            with lock:
                if p["round"] == round_no:
                    p["status"] = "ready" if p["cands"] else "error"
                    p["error"] = "" if p["cands"] else "这张照片没有渲染成功"
        except Exception as e:  # noqa
            traceback.print_exc()
            with lock:
                p["status"] = "error"
                p["error"] = "这张照片打不开，换一张试试" if "identify" in repr(e) else "这张照片处理失败"


def add_photo(name, body):
    suffix = Path(name).suffix.lower()
    if suffix not in EXTENSIONS:
        return False
    pid = uuid.uuid4().hex[:8]
    d = session_dir / pid
    d.mkdir(parents=True, exist_ok=True)
    src = d / f"photo{suffix}"
    src.write_bytes(body)
    with lock:
        state["done"] = None
        state["photos"].append({"id": pid, "name": Path(name).stem, "path": str(src), "status": "queued", "round": 1,
                                "cands": [], "shown": [], "pick": None, "error": ""})
    jobs.put(pid)
    return True


def regenerate(p):
    """E: remember the rejection, then queue four new layouts for this photo."""
    from scripts import taste
    ids = [c["id"] for c in p["cands"]]
    if ids:
        taste.pick(p["name"], "E", ids)
    p["round"] += 1
    p["cands"] = []
    p["pick"] = None
    p["status"] = "queued"
    jobs.put(p["id"])


def submit():
    from scripts import taste
    with lock:
        photos = list(state["photos"])
        if not photos or any(not p["pick"] for p in photos):
            return None
    out = desktop_dir() / "ins排版" / dt.datetime.now().strftime("%Y-%m-%d %H%M%S")
    out.mkdir(parents=True, exist_ok=True)
    saved = []
    for n, p in enumerate(photos, 1):
        c = next(c for c in p["cands"] if c["letter"] == p["pick"])
        shutil.copy2(files[c["url"]], out / f"{n:02d}_{p['name']}.png")
        taste.pick(p["name"], p["pick"], [x["id"] for x in p["cands"]])
        saved.append({"url": c["url"]})
    with lock:
        state["done"] = {"folder": str(out), "pages": saved}
    return out


def reset():
    global session_dir
    with lock:
        old = session_dir
        session_dir = SESSIONS / uuid.uuid4().hex
        state["photos"] = []
        state["done"] = None
        files.clear()
    shutil.rmtree(old, ignore_errors=True)


def public_state():
    with lock:
        return {"engine": state["engine"], "done": state["done"],
                "photos": [{k: p[k] for k in ("id", "name", "status", "cands", "pick", "error")} for p in state["photos"]]}


class Handler(BaseHTTPRequestHandler):
    def log_message(self, *a):
        pass

    def send(self, code, body=b"", ctype="application/json; charset=utf-8"):
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def send_json(self, obj):
        self.send(200, json.dumps(obj, ensure_ascii=False).encode("utf-8"))

    def trusted(self):
        """Only this app's own page may change anything: other sites can reach localhost too."""
        origin = self.headers.get("Origin")
        return origin in (None, ORIGIN) and self.headers.get("Host") == f"127.0.0.1:{PORT}"

    def do_GET(self):
        global last_seen, window_closing_at
        path = urlparse(self.path).path
        if path == "/":
            self.send(200, (ROOT / "app" / "index.html").read_bytes(), "text/html; charset=utf-8")
        elif path == "/icon.png":
            self.send(200, (ROOT / "app" / "icon.png").read_bytes(), "image/png")
        elif path == "/ping":
            self.send_json({"app": "ins-layout"})
        elif path == "/state":
            last_seen = time.time()
            window_closing_at = None
            self.send_json(public_state())
        elif path in files and Path(files[path]).exists():
            self.send(200, Path(files[path]).read_bytes(), "image/png")
        else:
            self.send(404)

    def do_PUT(self):
        if not self.trusted():
            return self.send(403)
        url = urlparse(self.path)
        name = unquote(parse_qs(url.query).get("name", [""])[0])
        body = self.rfile.read(int(self.headers.get("Content-Length", 0)))
        self.send_json({"ok": add_photo(name, body)})

    def do_POST(self):
        global window_closing_at
        if not self.trusted():
            return self.send(403)
        path = urlparse(self.path).path
        n = int(self.headers.get("Content-Length", 0))
        raw = self.rfile.read(n)
        data = json.loads(raw) if raw.startswith(b"{") else {}
        if path == "/pick":
            with lock:
                p = find_photo(data.get("id"))
                if p and any(c["letter"] == data.get("letter") for c in p["cands"]):
                    p["pick"] = data["letter"]
            self.send_json({"ok": bool(p)})
        elif path == "/again":
            with lock:
                p = find_photo(data.get("id"))
                if p and p["status"] in ("ready", "error"):
                    regenerate(p)
            self.send_json({"ok": bool(p)})
        elif path == "/remove":
            with lock:
                state["photos"] = [p for p in state["photos"] if p["id"] != data.get("id")]
            self.send_json({"ok": True})
        elif path == "/submit":
            out = submit()
            self.send_json({"ok": bool(out), "folder": str(out or "")})
        elif path == "/reset":
            reset()
            self.send_json({"ok": True})
        elif path == "/open":
            folder = (state["done"] or {}).get("folder")
            if folder:
                if sys.platform == "win32":
                    os.startfile(folder)  # noqa
                else:
                    subprocess.Popen(["open" if sys.platform == "darwin" else "xdg-open", folder])
            self.send_json({"ok": bool(folder)})
        elif path == "/bye":
            window_closing_at = time.time()
            self.send_json({"ok": True})
        else:
            self.send(404)


def open_window():
    url = ORIGIN + "/"
    candidates = [r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
                  r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
                  r"C:\Program Files\Google\Chrome\Application\chrome.exe",
                  "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
                  "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge"]
    exe = next((c for c in candidates if Path(c).exists()), None)
    if not exe:
        webbrowser.open(url)
        return
    subprocess.Popen([exe, f"--app={url}", f"--user-data-dir={BASE / 'window'}", "--window-size=1240,900",
                      "--no-first-run", "--no-default-browser-check", "--disable-background-timer-throttling",
                      "--disable-renderer-backgrounding", "--disable-backgrounding-occluded-windows"])


def focus_window():
    """A second double-click brings the open window forward instead of opening another one."""
    if sys.platform != "win32":
        return False
    import ctypes
    user32 = ctypes.windll.user32
    hwnd = user32.FindWindowW(None, "ins排版台")
    if not hwnd:
        return False
    user32.ShowWindow(hwnd, 9)  # SW_RESTORE, in case it is minimised
    user32.SetForegroundWindow(hwnd)
    return True


def already_running():
    try:
        with urllib.request.urlopen(ORIGIN + "/ping", timeout=1) as r:
            return json.load(r).get("app") == "ins-layout"
    except Exception:  # noqa
        return False


def watchdog(server):
    """Quit once the window is gone: soon after it says goodbye, or if it goes silent."""
    while True:
        time.sleep(1)
        now = time.time()
        closing = window_closing_at and now - window_closing_at > 4
        silent = last_seen and now - last_seen > 90
        if closing or silent:
            jobs.put(None)
            time.sleep(1.5)
            shutil.rmtree(SESSIONS, ignore_errors=True)  # the app's own copies; finished pages are on the Desktop
            server.shutdown()
            os._exit(0)


def main():
    if already_running():
        if not focus_window():
            open_window()
        return
    shutil.rmtree(SESSIONS, ignore_errors=True)  # copies left by a previous run
    server = ThreadingHTTPServer(("127.0.0.1", PORT), Handler)
    threading.Thread(target=worker, daemon=True).start()
    threading.Thread(target=watchdog, args=(server,), daemon=True).start()
    open_window()
    server.serve_forever()


if __name__ == "__main__":
    main()
