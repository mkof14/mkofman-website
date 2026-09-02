#!/usr/bin/env python3
"""One-time generator: build i18n_overrides_data.json from baseline + quality patches."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from gen_i18n_gaps_translations import build as build_baseline
from i18n_constants import LANGS, RECORD, RECORD_ARROW

GAPS_PATH = Path("/tmp/i18n_gaps.json")
OUT_PATH = Path(__file__).resolve().parent / "i18n_overrides_data.json"

# Proper nouns / brand terms kept in English across all languages
KEEP_ENGLISH = (
    "Michael Kofman",
    "Digital Invest Inc.",
    "AGRON Inc.",
    "9 Net Avenue Inc.",
    "9 Net Avenue",
    "NASDAQ: CNTX",
    "NASDAQ: XOXO",
    "Concentric Networks",
    "XO Communications",
    "DataPeer Inc.",
    "DataPeer",
    "XIBI Group Inc.",
    "Biotechnology Group Inc.",
    "Nikolaev Shipbuilding Plant",
    "Elitan United Inc.",
    "Astra Corp",
    "Sony",
    "Formspree",
    "Plausible",
    "Google Analytics",
    "LinkedIn",
    "ISDRI",
    "Entrepreneur Magazine",
    "Healthcare Tech Outlook",
    "Who's Who",
    "Clayton M. Christensen",
    "Daniel Kahneman",
    "David Deutsch",
    "Richard Rumelt",
    "Thomas S. Kuhn",
    "The Innovator's Dilemma",
    "Thinking, Fast and Slow",
    "The Beginning of Infinity",
    "Good Strategy/Bad Strategy",
    "The Structure of Scientific Revolutions",
    "Top Precision Medicine Solutions",
    "mkofman.com",
    "mkofman@mkofman.com",
    "agron1.com",
    "Charlotte, North Carolina",
    "CEO & CTO",
    "CEO & Board Member",
    "Ph.D.",
    "Doctor of Technical Sciences",
    "UAV",
    "Counter-UAS",
    "iSCSI",
    "SAN",
    "AGRON Ecosystem",
    "AGRON Maritime Intelligence + Security",
    "Aerial-Ground Robotics Operations Network",
)

RECORD_KEYS = {
    "nav.career": RECORD,
    "career.title": RECORD,
    "home.careerLink": RECORD_ARROW,
    "about.recordLink": RECORD_ARROW,
}

RECORD_META = {
    "es": "El registro — Michael Kofman",
    "de": "Der Werdegang — Michael Kofman",
    "fr": "Le parcours — Michael Kofman",
    "ru": "Хроника — Michael Kofman",
    "uk": "Хроніка — Michael Kofman",
    "zh": "履历 — Michael Kofman",
    "ar": "السجل — Michael Kofman",
    "he": "הרישום — Michael Kofman",
}

THESIS_TITLE = {
    "es": "Construir a largo plazo. Decidir en el presente.",
    "de": "Für die Langzeit bauen. In der Gegenwart entscheiden.",
    "fr": "Construire pour le long terme. Décider dans le présent.",
    "ru": "Строить надолго. Решать — сейчас.",
    "uk": "Будувати надовго. Вирішувати — зараз.",
    "zh": "为长期建设。在当下决策。",
    "ar": "البناء على المدى البعيد. القرار في الحاضر.",
    "he": "לבנות לטווח ארוך. להחליט בהווה.",
}


def flatten_sectioned(sectioned: dict) -> dict[str, dict[str, str]]:
    flat: dict[str, dict[str, str]] = {}
    for lang in LANGS:
        for section, keys in sectioned[lang].items():
            if section == "meta":
                for page, fields in keys.items():
                    for field, val in fields.items():
                        flat.setdefault(f"meta.{page}.{field}", {})[lang] = val
            else:
                for key, val in keys.items():
                    flat.setdefault(f"{section}.{key}", {})[lang] = val
    return flat


def load_gaps_flat() -> dict[str, str]:
    gaps = json.loads(GAPS_PATH.read_text(encoding="utf-8"))
    flat: dict[str, str] = {}
    for section, keys in gaps.items():
        for key, val in keys.items():
            flat[f"{section}.{key}"] = val
    return flat


def is_intentional_english(en_val: str, translated: str) -> bool:
    if translated != en_val:
        return False
    for term in KEEP_ENGLISH:
        if term in en_val and en_val.strip() == term.strip():
            return True
    if re.fullmatch(r"[\d\s—–-]+", en_val):
        return True
    if en_val in KEEP_ENGLISH:
        return True
    return False


def main() -> None:
    baseline = flatten_sectioned(build_baseline())
    english = load_gaps_flat()

    # Import comprehensive quality patches
    from i18n_quality_patches import PATCHES  # noqa: WPS433

    overrides: dict[str, dict[str, str]] = {}
    for path, en_val in english.items():
        entry: dict[str, str] = {}
        for lang in LANGS:
            val = PATCHES.get(path, {}).get(lang)
            if val is None:
                val = baseline.get(path, {}).get(lang, en_val)
            entry[lang] = val
        overrides[path] = entry

    # Apply record + thesis title overrides
    for path, mapping in RECORD_KEYS.items():
        if path in overrides:
            overrides[path].update(mapping)

    if "meta.career.title" in overrides:
        overrides["meta.career.title"].update(RECORD_META)

    if "thesis.title" in overrides:
        overrides["thesis.title"].update(THESIS_TITLE)

    OUT_PATH.write_text(json.dumps(overrides, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {OUT_PATH} — {len(overrides)} keys × {len(LANGS)} langs")


if __name__ == "__main__":
    main()
