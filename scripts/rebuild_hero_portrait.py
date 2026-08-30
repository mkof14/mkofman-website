#!/usr/bin/env python3
"""Rebuild hero portrait from original — cutout only, no quality edits."""
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


def main() -> None:
    from PIL import Image

    original_path = _find_original()
    src = Image.open(original_path).convert("RGB")
    print(f"original: {original_path.name} {src.size} (unchanged)")

    cutout = _remove_background(src)
    print(f"cutout: {cutout.size}")

    OUT_SOURCE.parent.mkdir(parents=True, exist_ok=True)
    cutout.save(OUT_SOURCE, "PNG")
    print(f"wrote {OUT_SOURCE.relative_to(ROOT)} ({OUT_SOURCE.stat().st_size // 1024} KB)")


if __name__ == "__main__":
    main()
