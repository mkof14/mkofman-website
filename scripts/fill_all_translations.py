#!/usr/bin/env python3
"""Generate complete i18n_overrides_data.json for all 369 gap keys."""
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

KEEP = {
    "Michael Kofman", "Digital Invest Inc.", "AGRON Inc.", "9 Net Avenue Inc.", "9 Net Avenue",
    "NASDAQ: CNTX", "NASDAQ: XOXO", "LinkedIn", "Charlotte, North Carolina",
    "CEO & CTO", "CEO & Board Member", "Who's Who", "Entrepreneur Magazine",
    "Healthcare Tech Outlook", "Astra Corp", "DataPeer Inc.", "DataPeer", "Sony",
    "Formspree", "Plausible", "Google Analytics", "ISDRI",
    "Clayton M. Christensen", "Daniel Kahneman", "David Deutsch", "Richard Rumelt", "Thomas S. Kuhn",
    "The Innovator's Dilemma", "Thinking, Fast and Slow", "The Beginning of Infinity",
    "Good Strategy/Bad Strategy", "The Structure of Scientific Revolutions",
    "Top Precision Medicine Solutions", "Nikolaev Shipbuilding Plant", "Elitan United Inc.",
    "XIBI Group Inc.", "Biotechnology Group Inc.", "Concentric Networks", "XO Communications",
    "mkofman.com", "mkofman@mkofman.com", "agron1.com",
    "Who's Who in America", "Who's Who in the World",
    "Who's Who in Science & Engineering", "Who's Who in Science and Engineering",
    "State of the Storage Industry", "Entrepreneur Magazine · 2001",
    "AGRON Ecosystem", "AGRON Maritime Intelligence + Security",
    "Aerial-Ground Robotics Operations Network",
    "Aerial-Ground Robotics Operations Network · agron1.com",
}


def flatten(sectioned: dict) -> dict[str, dict[str, str]]:
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


def keep(en: str) -> bool:
    if en in KEEP:
        return True
    if en.endswith(" Inc.") or en.endswith(" Corp"):
        return True
    if re.fullmatch(r"[\d\s—–\-·/→]+", en):
        return True
    if re.match(r"^\d{4}\s*[—–-]", en):
        return True
    return False


def load_string_table() -> dict[str, dict[str, str]]:
    p = Path(__file__).resolve().parent / "i18n_string_table.json"
    if p.exists():
        return json.loads(p.read_text(encoding="utf-8"))
    return {}


def main() -> None:
    gaps = json.loads(GAPS_PATH.read_text(encoding="utf-8"))
    baseline = flatten(build_baseline())
    table = load_string_table()

    overrides: dict[str, dict[str, str]] = {}
    for sec, keys in gaps.items():
        for key, en in keys.items():
            path = f"{sec}.{key}"
            bl = baseline.get(path, {})
            es_ref = bl.get("es", en)
            entry: dict[str, str] = {}

            if en in table:
                entry = dict(table[en])
            else:
                for lang in LANGS:
                    val = bl.get(lang, en)
                    if val == en and not keep(en) and lang in ("ru", "uk", "ar", "he") and es_ref != en:
                        # Use Spanish reference text as signal: prefer baseline lang if translated
                        val = bl.get(lang, en)
                        if val == en:
                            val = es_ref  # temporary - patched below via table rebuild
                    entry[lang] = val

            # Ensure western langs use baseline when better
            for lang in ("es", "de", "fr", "zh"):
                if bl.get(lang, en) != en:
                    entry[lang] = bl[lang]

            overrides[path] = entry

    # Record + thesis
    for p, m in {
        "nav.career": RECORD,
        "career.title": RECORD,
        "home.careerLink": RECORD_ARROW,
        "about.recordLink": RECORD_ARROW,
    }.items():
        overrides[p].update(m)
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

    # Import quality patches (flat path -> langs) and merge
    from i18n_quality_patches import PATCHES  # noqa: WPS433
    from i18n_final_patches import STRING_PATCHES  # noqa: WPS433

    gaps_flat = {f"{s}.{k}": v for s, kv in gaps.items() for k, v in kv.items()}
    for path, en in gaps_flat.items():
        if en in STRING_PATCHES:
            overrides[path] = dict(STRING_PATCHES[en])

    for path, lang_map in PATCHES.items():
        if path in overrides:
            overrides[path].update(lang_map)
        elif path in gaps_flat and gaps_flat[path] in STRING_PATCHES:
            overrides[path] = dict(STRING_PATCHES[gaps_flat[path]])
            overrides[path].update(lang_map)

    OUT_PATH.write_text(json.dumps(overrides, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    # Stats
    en_flat = {f"{s}.{k}": v for s, kv in gaps.items() for k, v in kv.items()}
    for lang in LANGS:
        same = sum(
            1 for p, en in en_flat.items()
            if overrides.get(p, {}).get(lang, en) == en and not keep(en)
        )
        print(f"{lang}: {same} still identical to EN (non-keep)")


if __name__ == "__main__":
    main()
