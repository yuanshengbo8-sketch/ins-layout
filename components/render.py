"""SVG -> PNG through Playwright Chromium (the renderer that passed preflight on this machine).

The SVG is wrapped in a minimal HTML page so system fonts, emoji, CSS filters and
foreignObject (if ever needed) all resolve exactly as a browser would.
"""
import json
from pathlib import Path

_browser = None
_pw = None


def _get_browser():
    global _browser, _pw
    if _browser is None:
        from playwright.sync_api import sync_playwright
        _pw = sync_playwright().start()
        _browser = _pw.chromium.launch()
    return _browser


def close():
    global _browser, _pw
    if _browser is not None:
        _browser.close(); _browser = None
    if _pw is not None:
        _pw.stop(); _pw = None


def render_svg(svg: str, out_path, width: int, height: int, transparent=False, scale=1):
    out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    html = f"""<!doctype html><html><head><meta charset='utf-8'>
<style>html,body{{margin:0;padding:0;background:{'transparent' if transparent else '#fff'};}}
svg{{display:block}}</style></head><body>{svg}</body></html>"""
    b = _get_browser()
    page = b.new_page(viewport={"width": width, "height": height}, device_scale_factor=scale)
    try:
        page.set_content(html, wait_until="load")
        page.evaluate("document.fonts.ready")
        page.wait_for_timeout(80)
        page.screenshot(path=str(out_path), omit_background=transparent, clip={"x": 0, "y": 0, "width": width, "height": height})
    finally:
        page.close()
    return out_path


def probe_fonts(families):
    """Return {family: bool} by measuring text width vs. a fallback in Chromium."""
    b = _get_browser()
    page = b.new_page()
    try:
        page.set_content("<html><body></body></html>")
        res = page.evaluate(
            """(fams) => {
                const c = document.createElement('canvas').getContext('2d');
                const sample = 'mmmmmmmmmmlllllllllliiiiiiiiiiWWWWWWWWWW 中文测试 0123456789';
                const w = (f, fb) => { c.font = `48px "${f}", ${fb}`; return c.measureText(sample).width; };
                const out = {};
                for (const f of fams) {
                  // a real family gives the same width whatever fallback is named; a missing one follows the fallback
                  const a = w(f, 'monospace'), b = w(f, 'serif');
                  out[f] = Math.abs(a - b) < 0.5 && Math.abs(a - w('__nonexistent_zz__', 'monospace')) > 0.5;
                }
                return out;
            }""",
            families,
        )
        return res
    finally:
        page.close()


def measure_text(text, family, size, weight="normal", style="normal", letter_spacing=0):
    """Measure text width in px using Chromium's canvas (same engine that renders)."""
    b = _get_browser()
    page = b.new_page()
    try:
        page.set_content("<html><body></body></html>")
        return page.evaluate(
            """([t,f,s,w,st,ls]) => { const c=document.createElement('canvas').getContext('2d');
               c.font = `${st} ${w} ${s}px "${f}"`; if ('letterSpacing' in c) c.letterSpacing = ls+'px';
               return c.measureText(t).width + (('letterSpacing' in c)?0:ls*Math.max(0,t.length-1)); }""",
            [text, family, size, weight, style, letter_spacing],
        )
    finally:
        page.close()


def measure_many(items):
    """items: list of dicts {text,family,size,weight,style,letter_spacing} -> list of widths (one page)."""
    b = _get_browser()
    page = b.new_page()
    try:
        page.set_content("<html><body></body></html>")
        return page.evaluate(
            """(items) => { const c=document.createElement('canvas').getContext('2d');
               return items.map(it => { c.font = `${it.style||'normal'} ${it.weight||'normal'} ${it.size}px "${it.family}"`;
                 const ls = it.letter_spacing||0; if ('letterSpacing' in c) c.letterSpacing = ls+'px';
                 return c.measureText(it.text).width + (('letterSpacing' in c)?0:ls*Math.max(0,it.text.length-1)); }); }""",
            items,
        )
    finally:
        page.close()
