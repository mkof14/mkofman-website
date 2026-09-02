"""Shared translation constants and helpers."""

LANGS = ("es", "de", "fr", "ru", "uk", "zh", "ar", "he")

# Proper nouns — keep in all languages
RECORD = {
    "es": "El registro", "de": "Der Werdegang", "fr": "Le parcours",
    "ru": "Хроника", "uk": "Хроніка", "zh": "履历",
    "ar": "السجل", "he": "הרישום",
}
RECORD_ARROW = {l: f"{v} →" for l, v in RECORD.items()}


def T(es, de, fr, ru, uk, zh, ar, he):
    return {"es": es, "de": de, "fr": fr, "ru": ru, "uk": uk, "zh": zh, "ar": ar, "he": he}


def build_section(flat: dict) -> dict:
    """Convert flat 'section.key' dict to {section: {lang: {key: val}}}."""
    result = {lang: {} for lang in LANGS}
    for path, langs in flat.items():
        sec, key = path.split(".", 1)
        for lang in LANGS:
            result[lang].setdefault(sec, {})[key] = langs[lang]
    return result
