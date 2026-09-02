#!/usr/bin/env python3
"""Audit translations.js and report coverage to scripts/i18n_audit_report.md."""
from __future__ import annotations

import json
import re
from collections import defaultdict
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
TRANSLATIONS_PATH = ROOT / "js" / "translations.js"
GAPS_PATH = Path("/tmp/i18n_gaps.json")
REPORT_PATH = Path(__file__).resolve().parent / "i18n_audit_report.md"

LANGS = ("en", "es", "de", "fr", "ru", "uk", "zh", "ar", "he")
TARGET_LANGS = ("es", "de", "fr", "ru", "uk", "zh", "ar", "he")

KEEP_ENGLISH = (
    "Michael Kofman", "Digital Invest Inc.", "AGRON Inc.", "9 Net Avenue Inc.", "9 Net Avenue",
    "NASDAQ: CNTX", "NASDAQ: XOXO", "Concentric Networks", "XO Communications", "DataPeer Inc.",
    "DataPeer", "XIBI Group Inc.", "Biotechnology Group Inc.", "Nikolaev Shipbuilding Plant",
    "Elitan United Inc.", "Astra Corp", "Sony", "Formspree", "Plausible", "Google Analytics",
    "LinkedIn", "ISDRI", "Entrepreneur Magazine", "Healthcare Tech Outlook", "Who's Who",
    "Clayton M. Christensen", "Daniel Kahneman", "David Deutsch", "Richard Rumelt", "Thomas S. Kuhn",
    "The Innovator's Dilemma", "Thinking, Fast and Slow", "The Beginning of Infinity",
    "Good Strategy/Bad Strategy", "The Structure of Scientific Revolutions",
    "Top Precision Medicine Solutions", "mkofman.com", "mkofman@mkofman.com", "agron1.com",
    "Charlotte, North Carolina", "CEO & CTO", "CEO & Board Member", "Founder",
    "AGRON Ecosystem", "AGRON Maritime Intelligence + Security",
    "Aerial-Ground Robotics Operations Network",
    "Who's Who in America", "Who's Who in the World",
    "Who's Who in Science & Engineering", "Who's Who in Science and Engineering",
    "State of the Storage Industry", "Email", "Ph.D.", "Doctor of Technical Sciences",
    "UAV", "Counter-UAS", "iSCSI", "SAN", "agron1.com",
    "Entrepreneur Magazine · 2001", "agron1.com →",
)


def load_translations(path: Path) -> dict[str, Any]:
    raw = path.read_text(encoding="utf-8")
    start = raw.find("{")
    end = raw.rfind("}")
    return json.loads(raw[start : end + 1])


def flatten(obj: Any, prefix: str = "") -> dict[str, str]:
    out: dict[str, str] = {}
    if isinstance(obj, dict):
        for key, val in obj.items():
            path = f"{prefix}.{key}" if prefix else key
            out.update(flatten(val, path))
    elif isinstance(obj, str):
        out[prefix] = obj
    return out


def is_intentional_english(en_val: str, translated: str) -> bool:
    if translated != en_val:
        return False
    if en_val in KEEP_ENGLISH:
        return True
    if en_val.endswith(" Inc.") or en_val.endswith(" Corp"):
        return True
    if re.fullmatch(r"[\d\s—–\-·/→]+", en_val):
        return True
    if re.match(r"^\d{4}\s*[—–-]", en_val):
        return True
    for term in KEEP_ENGLISH:
        if term in en_val and len(en_val) <= len(term) + 30 and en_val.count(" ") < 8:
            if all(part in en_val or part in KEEP_ENGLISH for part in en_val.split()):
                pass
    return False


def has_english_sentence(text: str) -> bool:
    if not text or len(text) < 4:
        return False
    common = (
        " the ", " and ", " for ", " with ", " that ", " this ", " from ", " are ",
        " was ", " have ", " will ", " should ", " must ", " when ", " how ",
    )
    lower = f" {text.lower()} "
    return any(w in lower for w in common)


def main() -> None:
    translations = load_translations(TRANSLATIONS_PATH)
    en_flat = flatten(translations.get("en", {}))

    categories: dict[str, dict[str, list[str]]] = {
        lang: {"translated": [], "intentional": [], "needs_work": []} for lang in TARGET_LANGS
    }

    for path, en_val in sorted(en_flat.items()):
        for lang in TARGET_LANGS:
            lang_val = flatten(translations.get(lang, {})).get(path, "")
            if not lang_val:
                categories[lang]["needs_work"].append(f"{path} (missing)")
            elif lang_val == en_val:
                if is_intentional_english(en_val, lang_val):
                    categories[lang]["intentional"].append(path)
                else:
                    categories[lang]["needs_work"].append(path)
            elif lang in ("ar", "he") and has_english_sentence(lang_val):
                categories[lang]["needs_work"].append(f"{path} (mixed English)")
            else:
                categories[lang]["translated"].append(path)

    lines = [
        "# i18n Audit Report",
        "",
        f"Source: `{TRANSLATIONS_PATH.relative_to(ROOT)}`",
        f"English string keys: **{len(en_flat)}**",
        f"Languages audited: {', '.join(TARGET_LANGS)}",
        "",
        "## Summary",
        "",
        "| Language | Translated | Intentional English | Needs Work | Coverage |",
        "|----------|------------|---------------------|------------|----------|",
    ]
    for lang in TARGET_LANGS:
        c = categories[lang]
        total = len(en_flat)
        translated = len(c["translated"])
        intentional = len(c["intentional"])
        needs = len(c["needs_work"])
        pct = round(100 * (translated + intentional) / total, 1) if total else 0
        lines.append(
            f"| {lang} | {translated} | {intentional} | {needs} | {pct}% |"
        )

    total_strings = len(en_flat) * len(TARGET_LANGS)
    lines.extend(["", f"**Total audited string slots:** {total_strings}", ""])
    lines.extend([
        "**Coverage:** Translated + intentional English counts as localized.",
        "",
    ])

    for lang in TARGET_LANGS:
        c = categories[lang]
        lines.extend([
            f"## {lang.upper()} — needs work ({len(c['needs_work'])})",
            "",
        ])
        if c["needs_work"]:
            for item in c["needs_work"][:80]:
                lines.append(f"- `{item}`")
            if len(c["needs_work"]) > 80:
                lines.append(f"- … and {len(c['needs_work']) - 80} more")
        else:
            lines.append("_None_")
        lines.append("")

    REPORT_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")

    print(f"Wrote {REPORT_PATH}")
    print("Summary per language:")
    for lang in TARGET_LANGS:
        c = categories[lang]
        print(
            f"  {lang}: translated={len(c['translated'])}, "
            f"intentional={len(c['intentional'])}, needs_work={len(c['needs_work'])}"
        )


if __name__ == "__main__":
    main()
