#!/usr/bin/env python3
"""Generate downloadable Media Kit PDF for press."""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "downloads"
OUT_PDF = OUT_DIR / "michael-kofman-media-kit.pdf"
PORTRAIT = ROOT / "images" / "portrait-hero-3.png"


def load_media_kit_copy() -> dict[str, str]:
    raw = (ROOT / "js" / "translations.js").read_text(encoding="utf-8")
    start, end = raw.find("{"), raw.rfind("}")
    data = json.loads(raw[start : end + 1])
    mk = data["en"]["mediaKit"]
    return {
        "title": mk["title"],
        "bio_short": mk["bioShort"],
        "bio_medium": mk["bioMedium"],
        "bio_long": mk["bioLong"],
        "contact_lead": mk["contactLead"],
    }


def main() -> None:
    try:
        from fpdf import FPDF
    except ImportError as exc:
        raise SystemExit(
            "fpdf2 required: python3 -m venv .venv && .venv/bin/pip install fpdf2"
        ) from exc

    copy = load_media_kit_copy()
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=18)
    pdf.add_page()

    pdf.set_font("Helvetica", "B", 22)
    pdf.cell(0, 12, "Michael Kofman", ln=True)
    pdf.set_font("Helvetica", "", 11)
    pdf.set_text_color(100, 100, 100)
    pdf.cell(0, 8, "CEO, Digital Invest Inc.  |  mkofman.com", ln=True)
    pdf.set_text_color(0, 0, 0)
    pdf.ln(4)

    if PORTRAIT.exists():
        img_w = 55
        x = (pdf.w - img_w) / 2
        pdf.image(str(PORTRAIT), x=x, w=img_w)
        pdf.ln(6)

    pdf.set_font("Helvetica", "B", 14)
    pdf.cell(0, 10, copy["title"], ln=True)
    pdf.set_font("Helvetica", "B", 11)
    pdf.cell(0, 8, "50-Word Bio", ln=True)
    pdf.set_font("Helvetica", "", 10)
    pdf.multi_cell(0, 5.5, copy["bio_short"])
    pdf.ln(3)

    pdf.set_font("Helvetica", "B", 11)
    pdf.cell(0, 8, "150-Word Bio", ln=True)
    pdf.set_font("Helvetica", "", 10)
    pdf.multi_cell(0, 5.5, copy["bio_medium"])
    pdf.ln(3)

    pdf.set_font("Helvetica", "B", 11)
    pdf.cell(0, 8, "Extended Bio", ln=True)
    pdf.set_font("Helvetica", "", 10)
    pdf.multi_cell(0, 5.5, copy["bio_long"])
    pdf.ln(4)

    pdf.set_font("Helvetica", "B", 11)
    pdf.cell(0, 8, "Press Contact", ln=True)
    pdf.set_font("Helvetica", "", 10)
    pdf.multi_cell(0, 5.5, copy["contact_lead"])
    pdf.cell(0, 6, "Email: mkofman@mkofman.com", ln=True)
    pdf.cell(
        0,
        6,
        "LinkedIn: linkedin.com/in/michael-kofman-0509176",
        ln=True,
    )
    pdf.ln(6)
    pdf.set_font("Helvetica", "I", 9)
    pdf.set_text_color(120, 120, 120)
    pdf.multi_cell(
        0,
        5,
        "High-resolution portraits available upon request. "
        "© Michael Kofman. For press and event use only.",
    )

    pdf.output(str(OUT_PDF))
    size_kb = OUT_PDF.stat().st_size / 1024
    print(f"Wrote {OUT_PDF.relative_to(ROOT)} ({size_kb:.0f} KB)")


if __name__ == "__main__":
    main()
