"""Progress ledger for ins-layout (status.json).

  python scripts/status.py                       # summary + resume pointer
  python scripts/status.py list [pending|ready|blocked|repair|waiting_input]
  python scripts/status.py set 053 visual=pass note="matches reference"   # record a human/AI visual verdict
  python scripts/status.py set 032 status=blocked blocker="asset G14 ground master not generated"
  python scripts/status.py init                  # (re)create entries for all 126 ids without losing existing data

States per layout: pending / repair / blocked / waiting_input / ready.
`ready` is only granted when technical == pass AND visual == pass.
"""
import datetime as dt
import json
import sys
from pathlib import Path

SK = Path(__file__).resolve().parents[1]
STATUS = SK / "status.json"
INDEX = SK / "references" / "index.json"
EFFECTS = SK / "effects.json"


def load():
    return json.loads(STATUS.read_text("utf-8")) if STATUS.exists() else {"version": "V6", "layouts": {}}


def save(s):
    s["updated_at"] = dt.datetime.now().isoformat(timespec="seconds")
    STATUS.write_text(json.dumps(s, indent=1, ensure_ascii=False), "utf-8")


def init():
    s = load()
    idx = json.loads(INDEX.read_text("utf-8"))
    eff = json.loads(EFFECTS.read_text("utf-8")) if EFFECTS.exists() else {}
    for lid, meta in idx.items():
        ent = s["layouts"].setdefault(lid, {})
        ent.setdefault("status", "pending")
        ent.setdefault("page", meta["page"]); ent.setdefault("cell", [meta["row"], meta["col"]])
        if lid in eff.get("layouts", {}):
            ent.setdefault("photos", eff["layouts"][lid].get("photos"))
            ent.setdefault("deps", eff["layouts"][lid].get("assets", []))
    save(s)
    print(f"{len(s['layouts'])} entries")


def summary():
    s = load()
    counts = {}
    for ent in s["layouts"].values():
        counts[ent.get("status", "pending")] = counts.get(ent.get("status", "pending"), 0) + 1
    print("ins-layout status:", json.dumps(counts))
    impl = [k for k, v in s["layouts"].items() if v.get("technical")]
    print(f"implemented+rendered: {len(impl)}/126")
    nxt = s.get("next_action")
    if nxt:
        print("NEXT:", nxt)
    lv = s.get("last_verify")
    if lv:
        print("last verify:", lv["at"], f"{sum(1 for v in lv['results'].values() if v == 'pass')}/{len(lv['ids'])} pass")


def list_(state=None):
    s = load()
    for k, v in sorted(s["layouts"].items()):
        if state and v.get("status") != state:
            continue
        print(f"{k:8} {v.get('status','pending'):14} tech={v.get('technical','-'):5} vis={v.get('visual','-'):5} {v.get('blocker') or v.get('note') or ''}")


def set_(lid, kvs):
    s = load()
    lid = lid if lid.startswith("INS-") else f"INS-{lid[-3:]}"
    ent = s["layouts"].setdefault(lid, {})
    for kv in kvs:
        k, _, v = kv.partition("=")
        ent[k] = v
    if ent.get("technical") == "pass" and ent.get("visual") == "pass" and ent.get("status") in (None, "pending", "repair"):
        ent["status"] = "ready"
    if ent.get("visual") == "fail":
        ent["status"] = "repair"
    ent["updated_at"] = dt.datetime.now().isoformat(timespec="seconds")
    save(s)
    print(lid, json.dumps(ent, ensure_ascii=False))


if __name__ == "__main__":
    a = sys.argv[1:]
    if not a:
        summary()
    elif a[0] == "init":
        init()
    elif a[0] == "list":
        list_(a[1] if len(a) > 1 else None)
    elif a[0] == "set":
        set_(a[1], a[2:])
    elif a[0] == "next":
        s = load(); s["next_action"] = " ".join(a[1:]); save(s); print("next:", s["next_action"])
