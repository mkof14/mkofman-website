LANGS = ("es", "de", "fr", "ru", "uk", "zh", "ar", "he")


def t(section: dict) -> dict:
    return {lang: section[lang] for lang in LANGS}
