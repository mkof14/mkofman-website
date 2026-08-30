#!/usr/bin/env python3
"""Rebuild hero portrait from original photo: crop, sharpen, rembg cutout."""
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


def _crop_for_hero(img):
    """Trim only the lowest balusters; keep natural lean on railing."""
    w, h = img.size
    left = int(w * 0.03)
    top = int(h * 0.015)
    right = int(w * 0.995)
    bottom = int(h * 0.875)
    return img.crop((left, top, right, bottom))


def _enhance_photo(img):
    """Restore clarity from soft camera original — natural, not plastic."""
    from PIL import Image, ImageEnhance, ImageFilter

    rgb = img.convert("RGB")
    resample = getattr(Image, "Resampling", Image).LANCZOS
    # Source is 683px — upscale to hero display width.
    target_w = 800
    if rgb.width < target_w:
        scale = target_w / rgb.width
        rgb = rgb.resize(
            (target_w, int(rgb.height * scale)),
            resample,
        )
    rgb = ImageEnhance.Contrast(rgb).enhance(1.04)
    rgb = ImageEnhance.Color(rgb).enhance(1.03)
    rgb = rgb.filter(
        ImageFilter.UnsharpMask(radius=1.2, percent=140, threshold=2)
    )
    rgb = ImageEnhance.Sharpness(rgb).enhance(1.1)
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

    original_path = _find_original()
    src = Image.open(original_path)
    print(f"original: {original_path.name} {src.size}")

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
