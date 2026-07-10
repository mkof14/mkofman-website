import json
from pathlib import Path
from typing import Any

from ui_patches import LANG_PATCHES


ROOT = Path(__file__).resolve().parents[1]
TRANSLATIONS_PATH = ROOT / "js" / "translations.js"


def load_translations(path: Path) -> dict[str, Any]:
    raw = path.read_text(encoding="utf-8")
    start = raw.find("{")
    end = raw.rfind("}")
    if start == -1 or end == -1 or end <= start:
        raise ValueError("Could not locate JSON object in translations.js")
    return json.loads(raw[start : end + 1])


def deep_merge(base: dict[str, Any], patch: dict[str, Any]) -> dict[str, Any]:
    for key, value in patch.items():
        if isinstance(value, dict) and isinstance(base.get(key), dict):
            deep_merge(base[key], value)
        else:
            base[key] = value
    return base


def apply_patches(translations: dict[str, Any]) -> dict[str, Any]:
    for lang, patch in LANG_PATCHES.items():
        if lang not in translations:
            translations[lang] = {}
        deep_merge(translations[lang], patch)

    # Hard-enforce Ukrainian content for these sections so they cannot remain in English.
    uk_required_sections = ["speaking", "caseStudies", "mediaKit", "articles", "cta"]
    for section in uk_required_sections:
        deep_merge(translations["uk"].setdefault(section, {}), LANG_PATCHES["uk"][section])

    return translations


def write_translations(path: Path, translations: dict[str, Any]) -> None:
    output = "const TRANSLATIONS = " + json.dumps(
        translations, ensure_ascii=False, indent=2
    ) + ";\n"
    path.write_text(output, encoding="utf-8")


def main() -> None:
    translations = load_translations(TRANSLATIONS_PATH)
    updated = apply_patches(translations)
    write_translations(TRANSLATIONS_PATH, updated)


if __name__ == "__main__":
    main()
