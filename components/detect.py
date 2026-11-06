"""Automatic measurement of real photos (page-15 rule 08): face boxes and shoe/feet position.

faces : OpenCV YuNet (assets/models/face_detection_yunet_2023mar.onnx) - robust to profile / looking-down faces.
        Box is expanded from the detector's tight face box to a HEAD box (hair included) because layouts avoid heads.
feet  : MediaPipe PoseLandmarker (assets/models/pose_landmarker_lite.task) when present; otherwise None.
All results are normalised (0..1) relative to the ORIGINAL photo, so they survive any later crop/scale.
"""
from pathlib import Path

import numpy as np
from PIL import Image

SK = Path(__file__).resolve().parents[1]
YUNET = SK / "assets" / "models" / "face_detection_yunet_2023mar.onnx"
POSE = SK / "assets" / "models" / "pose_landmarker_lite.task"


def _to_bgr(im: Image.Image, max_side=1280):
    im = im.convert("RGB")
    s = min(1.0, max_side / max(im.size))
    if s < 1.0:
        im = im.resize((int(im.width * s), int(im.height * s)), Image.LANCZOS)
    arr = np.asarray(im)[:, :, ::-1].copy()
    return arr, s


def detect_faces(im: Image.Image, score=0.6):
    """Return list of dicts {cx, cy, w, h, score, kind:'head'} normalised to the original image, largest first."""
    import cv2
    if not YUNET.exists():
        raise FileNotFoundError(f"YuNet model missing: {YUNET}")
    bgr, s = _to_bgr(im)
    h, w = bgr.shape[:2]
    det = cv2.FaceDetectorYN.create(str(YUNET), "", (w, h), score_threshold=score, nms_threshold=0.3, top_k=50)
    det.setInputSize((w, h))
    _, faces = det.detect(bgr)
    out = []
    if faces is None:
        return out
    for f in faces:
        x, y, fw, fh, sc = float(f[0]), float(f[1]), float(f[2]), float(f[3]), float(f[-1])
        # expand tight face -> head (hair + chin): wider by 1.35, taller by 1.6, shifted up
        cx, cy = x + fw / 2, y + fh / 2 - fh * 0.15
        hw, hh = fw * 1.35, fh * 1.6
        out.append({"cx": cx / w, "cy": cy / h, "w": hw / w, "h": hh / h, "score": round(sc, 3), "kind": "head",
                    "face": [x / w, y / h, fw / w, fh / h]})
    out.sort(key=lambda d: -d["w"] * d["h"])
    return out


def detect_pose(im: Image.Image):
    """Return normalised landmarks of interest {feet:(cx,cy), nose:(x,y), hips:(x,y)} or None."""
    if not POSE.exists() or POSE.stat().st_size < 100_000:
        return None
    try:
        import mediapipe as mp
        from mediapipe.tasks.python import vision
        from mediapipe.tasks.python.core.base_options import BaseOptions
    except Exception as e:  # noqa
        print("pose import failed:", repr(e)); return None
    rgb = np.asarray(im.convert("RGB"))
    try:
        mp_im = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb)
    except AttributeError:
        from mediapipe.tasks.python.vision.core import image as mpimage
        mp_im = mpimage.Image(image_format=mpimage.ImageFormat.SRGB, data=rgb)
    opts = vision.PoseLandmarkerOptions(base_options=BaseOptions(model_asset_path=str(POSE)), num_poses=1)
    with vision.PoseLandmarker.create_from_options(opts) as lm:
        res = lm.detect(mp_im)
    if not res.pose_landmarks:
        return None
    pts = res.pose_landmarks[0]
    def P(i):
        return (pts[i].x, pts[i].y, pts[i].visibility)
    nose = P(0); l_heel, r_heel, l_toe, r_toe = P(29), P(30), P(31), P(32)
    feet_pts = [p for p in (l_heel, r_heel, l_toe, r_toe) if p[2] > 0.5]
    feet = None
    if feet_pts:
        feet = (sum(p[0] for p in feet_pts) / len(feet_pts), sum(p[1] for p in feet_pts) / len(feet_pts))
    hips = ((P(23)[0] + P(24)[0]) / 2, (P(23)[1] + P(24)[1]) / 2)
    return {"feet": feet, "nose": nose[:2], "hips": hips, "visible_feet": len(feet_pts)}


def measure(path):
    """Full measurement for one photo path -> dict used by render.py (faces list, feet, pose)."""
    im = Image.open(path)
    from PIL import ImageOps
    im = ImageOps.exif_transpose(im)
    faces = detect_faces(im)
    pose = detect_pose(im)
    return {"path": str(path), "size": im.size, "faces": faces, "feet": pose["feet"] if pose else None, "pose": pose}


if __name__ == "__main__":
    import json, sys
    for p in sys.argv[1:]:
        print(json.dumps(measure(p), ensure_ascii=False, default=lambda o: round(o, 4) if isinstance(o, float) else str(o)))
