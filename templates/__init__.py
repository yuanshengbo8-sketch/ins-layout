"""Template registry: templates/ins_<num>.py each exposes META (dict) and build(canvas, ctx)."""
import importlib
from pathlib import Path

HERE = Path(__file__).resolve().parent


def _num(layout_id: str) -> str:
    return layout_id.upper().replace("INS-", "").zfill(3)


def module_path(layout_id: str):
    return HERE / f"ins_{_num(layout_id)}.py"


def implemented():
    return sorted(f"INS-{p.stem.split('_')[1]}" for p in HERE.glob("ins_*.py"))


def get(layout_id: str):
    n = _num(layout_id)
    if not (HERE / f"ins_{n}.py").exists():
        raise SystemExit(f"INS-{n} is not implemented yet (see status.json). Implemented: {', '.join(implemented())}")
    return importlib.import_module(f"templates.ins_{n}")
