#!/usr/bin/env python3
"""Rebuild scripts/i18n_gaps_translations.json from gaps source and OVERRIDES."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from i18n_constants import LANGS
from i18n_complete_overrides import OVERRIDES
from i18n_final_patches import STRING_PATCHES

GAPS_PATH = Path("/tmp/i18n_gaps.json")
EXISTING_PATH = Path(__file__).resolve().parent / "i18n_gaps_translations.json"
OUT_PATH = EXISTING_PATH


def load_gaps() -> dict[str, dict[str, str]]:
    return json.loads(GAPS_PATH.read_text(encoding="utf-8"))


def load_existing() -> dict[str, Any]:
    if EXISTING_PATH.exists():
        return json.loads(EXISTING_PATH.read_text(encoding="utf-8"))
    return {lang: {} for lang in LANGS}


def get_override(path: str, lang: str, existing: dict[str, Any], gaps: dict[str, dict[str, str]]) -> str:
    if path in OVERRIDES and lang in OVERRIDES[path]:
        return OVERRIDES[path][lang]
    sec, key = path.split(".", 1)
    if sec in existing.get(lang, {}):
        section = existing[lang][sec]
        if sec == "meta" and "." in key:
            page, field = key.split(".", 1)
            val = section.get(page, {}).get(field)
            if val:
                return val
        else:
            val = section.get(key)
            if val:
                return val
    return gaps[sec][key]


def build_sectioned(gaps: dict[str, dict[str, str]], existing: dict[str, Any]) -> dict[str, Any]:
    result: dict[str, Any] = {lang: {} for lang in LANGS}
    for sec, keys in gaps.items():
        for key in keys:
            path = f"{sec}.{key}"
            en_val = keys[key]
            for lang in LANGS:
                val = get_override(path, lang, existing, gaps)
                # Apply string-level patches (Founder, Email, de/fr UI, long-form)
                if en_val in STRING_PATCHES and lang in STRING_PATCHES[en_val]:
                    val = STRING_PATCHES[en_val][lang]
                if sec == "meta" and "." in key:
                    page, field = key.split(".", 1)
                    result[lang].setdefault(sec, {}).setdefault(page, {})[field] = val
                else:
                    result[lang].setdefault(sec, {})[key] = val
    return result


def main() -> None:
    gaps = load_gaps()
    existing = load_existing()
    out = build_sectioned(gaps, existing)
    OUT_PATH.write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    key_count = sum(len(keys) for keys in gaps.values())
    print(f"Wrote {OUT_PATH} — {key_count} keys × {len(LANGS)} langs")


if __name__ == "__main__":
    main()
