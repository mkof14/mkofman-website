#!/usr/bin/env python3
"""Apply round-2 flat-path translation patches to js/translations.js."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
TRANSLATIONS_PATH = ROOT / "js" / "translations.js"
ROUND2_JSON_PATH = Path(__file__).resolve().parent / "i18n_round2_translations.json"
from i18n_constants import LANGS  # noqa: E402


def load_round2() -> dict[str, dict[str, str]]:
    if ROUND2_JSON_PATH.exists():
        return json.loads(ROUND2_JSON_PATH.read_text(encoding="utf-8"))
    from i18n_complete_overrides import ROUND2  # noqa: E402
    from i18n_path_patches import PATH_PATCHES  # noqa: E402
    return {**ROUND2, **PATH_PATCHES}


def load_translations(path: Path) -> dict[str, Any]:
    raw = path.read_text(encoding="utf-8")
    start = raw.find("{")
    end = raw.rfind("}")
    if start == -1 or end == -1 or end <= start:
        raise ValueError(f"Could not locate JSON object in {path}")
    return json.loads(raw[start : end + 1])


def set_flat(translations: dict[str, Any], path: str, lang: str, value: str) -> None:
    parts = path.split(".")
    target = translations.setdefault(lang, {})
    for part in parts[:-1]:
        target = target.setdefault(part, {})
    target[parts[-1]] = value


def apply_round2(translations: dict[str, Any]) -> int:
    patches = load_round2()
    applied = 0
    for path, lang_map in patches.items():
        for lang in LANGS:
            if lang in lang_map:
                set_flat(translations, path, lang, lang_map[lang])
                applied += 1
    return applied


def write_translations(path: Path, translations: dict[str, Any]) -> None:
    output = "const TRANSLATIONS = " + json.dumps(translations, ensure_ascii=False, indent=2) + ";\n"
    path.write_text(output, encoding="utf-8")


def main() -> None:
    translations = load_translations(TRANSLATIONS_PATH)
    patches = load_round2()
    count = apply_round2(translations)
    write_translations(TRANSLATIONS_PATH, translations)
    print(f"Updated {TRANSLATIONS_PATH}")
    print(f"Applied {count} round-2 patches ({len(patches)} keys × up to {len(LANGS)} langs)")


if __name__ == "__main__":
    main()
