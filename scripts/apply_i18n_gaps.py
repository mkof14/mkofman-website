#!/usr/bin/env python3
"""Deep-merge i18n gap translations into js/translations.js and report remaining English-identical keys."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
TRANSLATIONS_PATH = ROOT / "js" / "translations.js"
PATCHES_PATH = Path(__file__).resolve().parent / "i18n_gaps_translations.json"
GAPS_PATH = Path("/tmp/i18n_gaps.json")

LANGS = ("es", "de", "fr", "ru", "uk", "zh", "ar", "he")


def load_translations(path: Path) -> dict[str, Any]:
    raw = path.read_text(encoding="utf-8")
    start = raw.find("{")
    end = raw.rfind("}")
    if start == -1 or end == -1 or end <= start:
        raise ValueError(f"Could not locate JSON object in {path}")
    return json.loads(raw[start : end + 1])


def deep_merge(base: dict[str, Any], patch: dict[str, Any]) -> dict[str, Any]:
    for key, value in patch.items():
        if isinstance(value, dict) and isinstance(base.get(key), dict):
            deep_merge(base[key], value)
        else:
            base[key] = value
    return base


def expand_meta_section(section_patch: dict[str, str]) -> dict[str, Any]:
    """Convert flat meta keys like 'board.description' to nested meta.board.description."""
    expanded: dict[str, Any] = {}
    for key, value in section_patch.items():
        if "." in key:
            page, field = key.split(".", 1)
            expanded.setdefault(page, {})[field] = value
        else:
            expanded[key] = value
    return expanded


def normalize_patch(section: str, section_patch: dict[str, Any]) -> dict[str, Any]:
    if section == "meta":
        return expand_meta_section(section_patch)  # type: ignore[arg-type]
    return section_patch


def apply_patches(translations: dict[str, Any], patches: dict[str, Any]) -> dict[str, Any]:
    for lang in LANGS:
        if lang not in patches:
            continue
        if lang not in translations:
            translations[lang] = {}
        for section, section_patch in patches[lang].items():
            target = translations[lang].setdefault(section, {})
            deep_merge(target, normalize_patch(section, section_patch))
    return translations


def write_translations(path: Path, translations: dict[str, Any]) -> None:
    output = "const TRANSLATIONS = " + json.dumps(translations, ensure_ascii=False, indent=2) + ";\n"
    path.write_text(output, encoding="utf-8")


def count_english_identical(translations: dict[str, Any], gaps: dict[str, dict[str, str]]) -> dict[str, int]:
    en = translations.get("en", {})
    counts: dict[str, int] = {}
    for lang in LANGS:
        remaining = 0
        lang_data = translations.get(lang, {})
        for section, keys in gaps.items():
            en_section = en.get(section, {})
            lang_section = lang_data.get(section, {})
            for key, en_val in keys.items():
                if section == "meta" and "." in key:
                    page, field = key.split(".", 1)
                    current = lang_section.get(page, {}).get(field)
                else:
                    current = lang_section.get(key)
                if current == en_val:
                    remaining += 1
        counts[lang] = remaining
    return counts


def main() -> None:
    translations = load_translations(TRANSLATIONS_PATH)
    patches = json.loads(PATCHES_PATH.read_text(encoding="utf-8"))
    gaps = json.loads(GAPS_PATH.read_text(encoding="utf-8"))

    updated = apply_patches(translations, patches)
    write_translations(TRANSLATIONS_PATH, updated)

    counts = count_english_identical(updated, gaps)
    print(f"Updated {TRANSLATIONS_PATH}")
    print("Remaining English-identical gap keys per language:")
    for lang in LANGS:
        patch_keys = sum(len(v) for v in patches.get(lang, {}).values())
        print(f"  {lang}: {counts[lang]} remaining ({patch_keys} patched)")


if __name__ == "__main__":
    main()
