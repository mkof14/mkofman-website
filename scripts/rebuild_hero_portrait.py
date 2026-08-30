#!/usr/bin/env python3
"""Rebuild hero portrait from original photo: crop, sharpen, rembg cutout."""
from __future__ import annotations

import io
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ORIGINAL = ROOT / "images" / "portrait-hero-original.jpg"
OUT_SOURCE = ROOT / "images" / "portrait-hero-source.png"


def _crop_for_hero(img):
    """Chest-up crop: exclude defective balustrade entirely."""
    w, h = img.size
    left = int(w * 0.06)
    top = int(h * 0.02)
    right = int(w * 0.98)
    bottom = int(h * 0.72)  # waist-up — no railing in frame
    return img.crop((left, top, right, bottom))


def _enhance_photo(img):
    """Clarity for soft original — sharpen before cutout."""
    from PIL import ImageEnhance, ImageFilter

    rgb = img.convert("RGB")
    # Upscale slightly for hero display (original is only 683px wide).
    resample = getattr(__import__("PIL.Image", fromlist=["Image"]).Image, "Resampling", None)
    lanczos = resample.LANCZOS if resample else 1
    scale = 1.15
    nw, nh = int(rgb.width * scale), int(rgb.height * scale)
    rgb = rgb.resize((nw, nh), lanczos)
    rgb = ImageEnhance.Contrast(rgb).enhance(1.05)
    rgb = ImageEnhance.Brightness(rgb).enhance(1.02)
    rgb = rgb.filter(
        ImageFilter.UnsharpMask(radius=1.6, percent=165, threshold=1)
    )
    rgb = ImageEnhance.Sharpness(rgb).enhance(1.18)
    return rgb


def _remove_background(img):
    from rembg import remove, new_session

    session = new_session("u2net")
    buf = io.BytesIO()
    img.save(buf, format="JPEG", quality=95)
    out = remove(
        buf.getvalue(),
        session=session,
        alpha_matting=True,
        alpha_matting_foreground_threshold=250,
        alpha_matting_background_threshold=8,
        alpha_matting_erode_size=6,
    )
    from PIL import Image
    return Image.open(io.BytesIO(out)).convert("RGBA")


def _trim_transparent(img, pad=8):
    from PIL import Image

    alpha = img.split()[3]
    bbox = alpha.getbbox()
    if not bbox:
        return img
    x0, y0, x1, y1 = bbox
    x0 = max(0, x0 - pad)
    y0 = max(0, y0 - pad)
    x1 = min(img.width, x1 + pad)
    y1 = min(img.height, y1 + pad)
    return img.crop((x0, y0, x1, y1))


def main() -> None:
    from PIL import Image

    if not ORIGINAL.exists():
        raise SystemExit(f"Missing original: {ORIGINAL}")

    src = Image.open(ORIGINAL)
    print(f"original: {src.size}")

    cropped = _crop_for_hero(src)
    print(f"cropped: {cropped.size}")

    enhanced = _enhance_photo(cropped)
    print("enhanced: contrast + unsharp mask")

    cutout = _remove_background(enhanced)
    print(f"cutout: {cutout.size}")

    cutout = _trim_transparent(cutout)
    OUT_SOURCE.parent.mkdir(parents=True, exist_ok=True)
    cutout.save(OUT_SOURCE, "PNG", optimize=True)
    print(f"wrote {OUT_SOURCE.relative_to(ROOT)} ({OUT_SOURCE.stat().st_size // 1024} KB)")


if __name__ == "__main__":
    main()
