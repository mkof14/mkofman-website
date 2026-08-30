#!/usr/bin/env python3
"""Rebuild hero portrait — cutout + railing repair from original pixels."""
from __future__ import annotations

import io
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ORIGINALS = [
    ROOT / "images" / "portrait-hero-original.png",
    ROOT / "images" / "portrait-hero-original.jpg",
]
OUT_SOURCE = ROOT / "images" / "portrait-hero-source.png"


def _find_original() -> Path:
    for path in ORIGINALS:
        if path.exists():
            return path
    raise FileNotFoundError("No portrait-hero-original.png or .jpg found")


def _remove_background(img):
    from rembg import remove, new_session

    session = new_session("u2net")
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    out = remove(buf.getvalue(), session=session)
    from PIL import Image
    return Image.open(io.BytesIO(out)).convert("RGBA")


def _sharpen_railing(rgb, rail_mask):
    """Upscale-sharpen-downscale on railing bbox for clearer stone detail."""
    import cv2
    import numpy as np

    if not rail_mask.any():
        return rgb.copy()

    out = rgb.copy()
    ys, xs = np.where(rail_mask)
    pad = 12
    y1, y2 = max(0, ys.min() - pad), min(rgb.shape[0], ys.max() + pad)
    x1, x2 = max(0, xs.min() - pad), min(rgb.shape[1], xs.max() + pad)
    crop = rgb[y1:y2, x1:x2]
    ch, cw = crop.shape[:2]
    scale = 2
    big = cv2.resize(crop, (cw * scale, ch * scale), interpolation=cv2.INTER_CUBIC)
    blur = cv2.GaussianBlur(big, (0, 0), 1.1)
    sharp = cv2.addWeighted(big, 1.75, blur, -0.75, 0)
    blur2 = cv2.GaussianBlur(sharp, (0, 0), 2.2)
    sharp = cv2.addWeighted(sharp, 1.45, blur2, -0.45, 0)
    restored = cv2.resize(sharp, (cw, ch), interpolation=cv2.INTER_AREA)
    restored = np.clip(restored, 0, 255).astype(np.uint8)
    out[y1:y2, x1:x2][rail_mask[y1:y2, x1:x2]] = restored[rail_mask[y1:y2, x1:x2]]
    return out


def _repair_railing(original, cutout):
    """Restore railing from original pixels with a clean alpha mask."""
    import cv2
    import numpy as np
    from PIL import Image

    w, h = original.size
    rgb = np.array(original.convert("RGB"), dtype=np.uint8)
    person_a = np.array(cutout.convert("RGBA"), dtype=np.uint8)[:, :, 3].astype(np.float32)

    y0 = int(h * 0.58)
    r, g, b = rgb[:, :, 0], rgb[:, :, 1], rgb[:, :, 2]
    lum = 0.299 * r + 0.587 * g + 0.114 * b

    stone = (
        (np.arange(h)[:, None] >= y0)
        & (lum >= 165)
        & (lum <= 242)
        & (np.max(rgb, axis=2) - np.min(rgb, axis=2) < 45)
        & ~((r > 175) & (g > 140) & (b > 120) & (r - b < 55))
    )
    stone[: int(h * 0.70), : int(w * 0.24)] = False

    mask = stone.astype(np.uint8) * 255
    n, labels, stats, _ = cv2.connectedComponentsWithStats(mask, connectivity=8)
    cleaned = np.zeros_like(mask)
    for i in range(1, n):
        x, y, bw, bh, area = stats[i]
        if area < 150:
            continue
        if bh < 10 and bw > bh * 5:
            continue
        touches_bottom = (y + bh) >= h - 6
        if touches_bottom and x >= int(w * 0.12):
            cleaned[labels == i] = 255

    cleaned = cv2.morphologyEx(cleaned, cv2.MORPH_CLOSE, np.ones((5, 5), np.uint8), 1)
    cleaned = cv2.erode(cleaned, np.ones((2, 2), np.uint8), 1)
    cleaned = cv2.dilate(cleaned, np.ones((3, 3), np.uint8), 1)

    rail = cleaned > 0
    rgb_out = _sharpen_railing(rgb, rail)

    alpha = np.zeros_like(person_a)
    alpha[person_a > 8] = person_a[person_a > 8]
    alpha[rail] = 255.0
    alpha = np.clip(alpha, 0, 255).astype(np.uint8)

    return Image.fromarray(np.dstack([rgb_out, alpha]))


def _defringe_railing_edges(img):
    """Remove light halos on semi-transparent railing edges only."""
    img = img.copy()
    px = img.load()
    w, h = img.size
    y0 = int(h * 0.54)
    for y in range(y0, h):
        for x in range(w):
            r, g, b, a = px[x, y]
            if 0 < a < 255:
                af = a / 255.0
                nr = int(max(0, min(255, (r - 255 * (1 - af)) / af)))
                ng = int(max(0, min(255, (g - 255 * (1 - af)) / af)))
                nb = int(max(0, min(255, (b - 255 * (1 - af)) / af)))
                px[x, y] = (nr, ng, nb, a)
    return img


def main() -> None:
    from PIL import Image

    original_path = _find_original()
    src = Image.open(original_path).convert("RGB")
    print(f"original: {original_path.name} {src.size}")

    cutout = _remove_background(src)
    print(f"cutout: {cutout.size}")

    fixed = _repair_railing(src, cutout)
    fixed = _defringe_railing_edges(fixed)
    print("railing: sharpened (2x upscale + unsharp)")

    OUT_SOURCE.parent.mkdir(parents=True, exist_ok=True)
    fixed.save(OUT_SOURCE, "PNG")
    print(f"wrote {OUT_SOURCE.relative_to(ROOT)} ({OUT_SOURCE.stat().st_size // 1024} KB)")


if __name__ == "__main__":
    main()
