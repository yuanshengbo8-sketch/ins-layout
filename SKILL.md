---
name: ins-layout
description: Lay out the user's photos in one of 126 "ins 风" (Instagram-style) layouts from The INS Layout Archive (INS-032 … INS-221) - big-word overlays, iMessage/IG UI chrome, stickers, schedules, colour cards, phone-screen carriers. Use when the user wants ins排版 / ins风排版 / 照片排版 / 做成 ins 图 / 用 INS-xxx / "每张一页，版式不重复" / 按穿搭分组排版, hands over photos for social-media layouts, or asks to continue building (续建), repair, or verify this skill. Output: 1200x1600 (3:4, user size wins) PNG + layered SVG + recipe JSON per page.
---

# ins-layout

An independent re-implementation of "排版效果库 · The INS Layout Archive · 126 layouts for your photos", designed by
普渡众神花 (https://www.douyin.com/note/7704661887081909540). Their 15 pages are not included in this repository;
`references/index.json` only records where each layout sat on those pages. See README.md and NOTICE.md.

## Entry points (all run from this folder)

```bash
python scripts/preflight.py                      # env check: image read, file io, perspective, SVG->PNG, fonts  (reports/preflight.json)
python scripts/status.py                         # progress summary + NEXT action (resume here after any interruption)
python scripts/status.py list ready|pending|blocked
python scripts/render.py --id 053 --photos a.jpg b.jpg --out ./out [--date 2026-11-05] [--text key=value ...] [--size 1080x1350]
python scripts/recommend.py a.jpg b.jpg [--n 4] [--exclude 203 167]   # ranked candidate sets per photo (fit + taste + variety)
python scripts/candidates.py --photo a.jpg --auto --out ./cands/a      # render the recommended set as A/B/C/D + sheet.jpg
python scripts/build_overlays.py [ids]                                 # refresh overlay maps after template changes
python scripts/verify.py [053 033 ...] [--sheet] # structural re-render with assets/test images into previews/structure/
python scripts/status.py set 053 visual=pass note="..."   # record the visual verdict after LOOKING at the render
```

Renderer: Playwright Chromium; final output is rendered at 2x and downscaled (crisp text), structure tests at 1x. Cover crops are centred on the measured head unless a template passes lock=True. Fonts: see `effects.json["fonts"]` (verified list + registered substitutes;
Futura/Avenir/Snell/Chalkboard/Silom/PingFang are substituted, never silently).

## How to serve a user request

1. Look at the actual photos first (count, portrait/landscape, framing, subject, empty space). Head boxes and feet are
   measured automatically by `components/detect.py` (OpenCV YuNet + MediaPipe pose, models in assets/models/) whenever
   `render.py` gets real photos; pass `--faces 0=cx,cy,w,h` / `--feet cx,cy` only to override. Still LOOK at the result.
2. Pick layouts: explicit `INS-xxx` wins; else choose by photo count (see `META["photos"]` in each template and
   `effects.json["layouts"]`). "每张一页，版式不重复" = one layout per photo, no repeats. Never AI-generate a person photo
   to fill a missing slot: list what is missing (type/count) or pick a layout that fits the photos given.
3. Render with `scripts/render.py`. Date defaults to today in the local timezone (`--date` to override); copy must
   describe the real photo (`--text key=value`, keys documented in each template's `T(ctx, key, default)` calls).
4. Open the PNG and check: window count/shape/position, text hierarchy and wrapping, UI/stickers, whitespace, face not
   covered (unless the layout is a face-cover layout). Fix and re-render before showing the user.
5. Deliver PNG + SVG + recipe JSON. The recipe records photo paths/hashes, windows, text, colour samples, substitutes.

Photos are read-only: never redraw identity, face, clothing or pose. Fit by cover-crop/pan inside the window only.

## Taste calibration mode (user: "一张照片生成四张，我来选")

Per photo: `python scripts/candidates.py --photo p.jpg --auto --out ./cands/<photo>` renders the set from
`scripts/recommend.py` (different families, head kept clear, one control from an unpicked family) -> A/B/C/D PNGs + `sheet.jpg`;
pass `--ids a b c d` to choose by hand and `--exclude` the ids already shown after an E.
Show the sheet, ask for one letter. A-D = pick, **E = regenerate a new set of four** (never repeat shown ids for that photo).
Record every answer: `python scripts/taste.py pick <photo> <letter> --ids a b c d [--note "why"]`; read
`python scripts/taste.py summary` before choosing the next set so the candidates lean toward families the user picks.
When every photo in the batch has a pick, package only the picked pages (plus captions) and copy them to the user's
Desktop folder.

Default taste (calibrated on one person's picks, so treat it as a starting point; your own picks in reports/ override
it): one small, realistic element (a UI card, a viewfinder, a serif label, a colour chip) beside the subject, never on
the face; the photo stays dominant; copy under ten words. Sticker and big-poster layouts appear at most once per set,
as a control.

## Scene variants

12 scene backgrounds have three versions (`NAME.webp`, `NAME__v2.webp`, `NAME__v3.webp`), so two people using the same
layout rarely get the same scene. `render.py` picks one from the photo's hash; `--variant 1|2|3` forces one. Sidecar
files (screen corners, cut-outs) follow the variant. Use `by_variant(ctx, v1, v2, v3)` in a template when text colour has
to change with the scene.

## Layout states (status.json)

`pending` (not implemented) / `repair` (implemented, visual mismatch queued) / `blocked` (needs a generated master
bitmap, see `effects.json["masters"]`) / `waiting_input` (project needs photos) / `ready` (technical + visual pass).

Current standing is in `status.json` and `reports/acceptance.md`. `installed` = true (dir, entry points, preflight).
`base_ready` requires 126/126: NOT reached yet (106/126 ready, 20 layouts still to write). `python scripts/status.py` -> NEXT.

## Build protocol (page 15, condensed)

- Each ID has its own module `templates/ins_<num>.py` with its own geometry/layers (`META` + `build(canvas, ctx)`);
  shared components live in `components/` (core canvas, ui chrome, deco vectors, imaging/perspective). Same skeleton
  with a different title does not count as a new layout.
- Structure test photos (`assets/test/`) stand in for photo CONTENT only; text, UI, decoration, materials, foreground
  masks and the whole composition must be real. Structure pass != real-photo pass.
- Generated masters (scenes, stickers, face masks) live in `assets/masters/` (see
  `effects.json["masters"]`). Screen corners and cut-outs ship ready-made. To add a scene, make a green-screen twin
  `*_GREEN.png` (screens or ground in #00FF00) and run `python scripts/chroma_masters.py`. A layout whose master is missing raises `AssetMissing` (blocked).
- Failed item: write "reference feature -> current difference -> responsible recipe/component/asset -> fix", re-render,
  re-look. Fix shared components first, then re-verify every affected layout.
- Save progress after each layout (`status.json`); on interruption, write `next_action` and resume from it.
