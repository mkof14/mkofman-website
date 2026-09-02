#!/usr/bin/env python3
"""Apply STRING_PATCHES to js/translations.js by matching English source values."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from i18n_constants import LANGS
from i18n_final_patches import STRING_PATCHES

ROOT = Path(__file__).resolve().parents[1]
TRANSLATIONS_PATH = ROOT / "js" / "translations.js"


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


def set_flat(translations: dict[str, Any], path: str, lang: str, value: str) -> None:
    parts = path.split(".")
    target = translations.setdefault(lang, {})
    for part in parts[:-1]:
        target = target.setdefault(part, {})
    target[parts[-1]] = value


def write_translations(path: Path, translations: dict[str, Any]) -> None:
    output = "const TRANSLATIONS = " + json.dumps(translations, ensure_ascii=False, indent=2) + ";\n"
    path.write_text(output, encoding="utf-8")


def main() -> None:
    translations = load_translations(TRANSLATIONS_PATH)
    en_flat = flatten(translations.get("en", {}))
    applied = 0

    for path, en_val in en_flat.items():
        patch = STRING_PATCHES.get(en_val)
        if not patch:
            continue
        for lang in LANGS:
            if lang in patch:
                set_flat(translations, path, lang, patch[lang])
                applied += 1

    write_translations(TRANSLATIONS_PATH, translations)
    print(f"Updated {TRANSLATIONS_PATH}")
    print(f"Applied {applied} string patches ({len(STRING_PATCHES)} English keys in table)")


if __name__ == "__main__":
    main()
