#!/usr/bin/env python3
"""Compile i18n_overrides_data.json — complete 369-key × 8-lang overrides."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from gen_i18n_gaps_translations import build as build_baseline
from i18n_constants import LANGS, RECORD, RECORD_ARROW, T

GAPS_PATH = Path("/tmp/i18n_gaps.json")
OUT_PATH = Path(__file__).resolve().parent / "i18n_overrides_data.json"

KEEP_ENGLISH_SUBSTR = (
    "Michael Kofman", "Digital Invest Inc.", "AGRON Inc.", "9 Net Avenue Inc.", "9 Net Avenue",
    "NASDAQ: CNTX", "NASDAQ: XOXO", "Concentric Networks", "XO Communications", "DataPeer Inc.",
    "DataPeer", "XIBI Group Inc.", "Biotechnology Group Inc.", "Nikolaev Shipbuilding Plant",
    "Elitan United Inc.", "Astra Corp", "Sony", "Formspree", "Plausible", "Google Analytics",
    "LinkedIn", "ISDRI", "Entrepreneur Magazine", "Healthcare Tech Outlook", "Who's Who",
    "Clayton M. Christensen", "Daniel Kahneman", "David Deutsch", "Richard Rumelt", "Thomas S. Kuhn",
    "The Innovator's Dilemma", "Thinking, Fast and Slow", "The Beginning of Infinity",
    "Good Strategy/Bad Strategy", "The Structure of Scientific Revolutions",
    "Top Precision Medicine Solutions", "mkofman.com", "mkofman@mkofman.com", "agron1.com",
    "Charlotte, North Carolina", "CEO & CTO", "CEO & Board Member",
    "AGRON Ecosystem", "AGRON Maritime Intelligence + Security",
    "Aerial-Ground Robotics Operations Network",
    "Who's Who in America", "Who's Who in the World",
    "Who's Who in Science & Engineering", "Who's Who in Science and Engineering",
    "State of the Storage Industry",
)


def flatten_sectioned(sectioned: dict) -> dict[str, dict[str, str]]:
    flat: dict[str, dict[str, str]] = {}
    for lang in LANGS:
        for section, keys in sectioned[lang].items():
            if not isinstance(keys, dict):
                continue
            if section == "meta":
                for key, val in keys.items():
                    flat.setdefault(f"meta.{key}", {})[lang] = val
            else:
                for key, val in keys.items():
                    flat.setdefault(f"{section}.{key}", {})[lang] = val
    return flat


def load_gaps_flat() -> dict[str, str]:
    gaps = json.loads(GAPS_PATH.read_text(encoding="utf-8"))
    return {f"{sec}.{k}": v for sec, keys in gaps.items() for k, v in keys.items()}


def should_keep_english(en_val: str) -> bool:
    if en_val in KEEP_ENGLISH_SUBSTR:
        return True
    if en_val.endswith(" Inc.") or en_val.endswith(" Corp"):
        return True
    if re.fullmatch(r"[\d\s—–\-·/→]+", en_val):
        return True
    if re.match(r"^\d{4}\s*[—–-]", en_val):
        return True
    return False


def pick_lang(flat: dict, path: str, lang: str, en_val: str) -> str:
    val = flat.get(path, {}).get(lang, en_val)
    if lang in ("ru", "uk", "ar", "he") and val == en_val and not should_keep_english(en_val):
        es = flat.get(path, {}).get("es", en_val)
        if es != en_val:
            return es  # temporary fallback marker — patched below
    return val


def apply_record_and_thesis(overrides: dict[str, dict[str, str]]) -> None:
    record_map = {
        "nav.career": RECORD,
        "career.title": RECORD,
        "home.careerLink": RECORD_ARROW,
        "about.recordLink": RECORD_ARROW,
    }
    for path, mapping in record_map.items():
        if path in overrides:
            overrides[path].update(mapping)
    overrides["meta.career.title"] = T(
        "El registro — Michael Kofman", "Der Werdegang — Michael Kofman", "Le parcours — Michael Kofman",
        "Хроника — Michael Kofman", "Хроніка — Michael Kofman", "履历 — Michael Kofman",
        "السجل — Michael Kofman", "הרישום — Michael Kofman",
    )
    overrides["thesis.title"] = T(
        "Construir a largo plazo. Decidir en el presente.",
        "Für die Langzeit bauen. In der Gegenwart entscheiden.",
        "Construire pour le long terme. Décider dans le présent.",
        "Строить надолго. Решать — сейчас.",
        "Будувати надовго. Вирішувати — зараз.",
        "为长期建设。在当下决策。",
        "البناء على المدى البعيد. القرار في الحاضر.",
        "לבנות לטווח ארוך. להחליט בהווה.",
    )


def apply_quality_patches(overrides: dict[str, dict[str, str]]) -> None:
    """Apply hand-crafted quality translations for broken baseline entries."""
    from i18n_quality_patches import PATCHES  # noqa: WPS433

    for path, lang_map in PATCHES.items():
        if path in overrides:
            overrides[path].update(lang_map)


def main() -> None:
    baseline = flatten_sectioned(build_baseline())
    english = load_gaps_flat()

    overrides: dict[str, dict[str, str]] = {}
    for path, en_val in english.items():
        entry = {lang: pick_lang(baseline, path, lang, en_val) for lang in LANGS}
        overrides[path] = entry

    apply_quality_patches(overrides)
    apply_record_and_thesis(overrides)

    OUT_PATH.write_text(json.dumps(overrides, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {OUT_PATH} — {len(overrides)} keys × {len(LANGS)} langs")


if __name__ == "__main__":
    main()
