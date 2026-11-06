"""Taste log: record which candidate the user picked, and summarise what the picks say.

  python scripts/taste.py pick <photo-name> <A|B|C|D|E> --ids 164 103 134 162 [--note "..."]
  python scripts/taste.py summary

Picks go to reports/taste.jsonl (machine-readable) and reports/taste.md (readable). `summary` counts picks and
rejections per layout family (effects.json["layouts"][id]["family"]) so selection rules can be tuned from evidence.
"""
import argparse
import datetime as dt
import json
from collections import Counter
from pathlib import Path

SK = Path(__file__).resolve().parents[1]
JL = SK / "reports" / "taste.jsonl"
MD = SK / "reports" / "taste.md"
JL.parent.mkdir(exist_ok=True)
FAM = {k: v.get("family", "?") for k, v in json.loads((SK / "effects.json").read_text("utf-8"))["layouts"].items()}


def pick(photo, letter, ids, note=""):
    ids = [f"INS-{i[-3:].zfill(3)}" for i in ids]
    letter = letter.upper()
    chosen = None if letter == "E" else ids["ABCDEFGH".index(letter)]
    rec = {"at": dt.datetime.now().isoformat(timespec="seconds"), "photo": photo, "candidates": ids, "pick": chosen,
           "rejected": [i for i in ids if i != chosen], "regenerate": letter == "E", "note": note}
    with JL.open("a", encoding="utf-8") as f:
        f.write(json.dumps(rec, ensure_ascii=False) + "\n")
    fam = lambda i: f"{i}({FAM.get(i, '?')})"  # noqa: E731
    line = (f"- {rec['at'][:10]} · {photo} · candidates {' / '.join(fam(i) for i in ids)} · "
            + (f"**pick: {fam(chosen)}**" if chosen else "**E = regenerate**") + (f" · {note}" if note else "") + "\n")
    with MD.open("a", encoding="utf-8") as f:
        f.write(line)
    print(line.strip())


def summary():
    if not JL.exists():
        print("no picks yet"); return
    picks, rejects = Counter(), Counter()
    for ln in JL.read_text("utf-8").splitlines():
        r = json.loads(ln)
        if r["pick"]:
            picks[FAM.get(r["pick"], "?")] += 1
        for i in r["rejected"]:
            rejects[FAM.get(i, "?")] += 1
    fams = sorted(set(picks) | set(rejects), key=lambda f: (-picks[f], rejects[f]))
    print(f"{'family':22} picked rejected")
    for f in fams:
        print(f"{f:22} {picks[f]:6} {rejects[f]:8}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("pick"); p.add_argument("photo"); p.add_argument("letter"); p.add_argument("--ids", nargs="+", required=True); p.add_argument("--note", default="")
    sub.add_parser("summary")
    a = ap.parse_args()
    if a.cmd == "pick":
        pick(a.photo, a.letter, a.ids, a.note)
    else:
        summary()
