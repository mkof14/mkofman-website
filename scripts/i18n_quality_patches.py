#!/usr/bin/env python3
"""Build flat path patches from English string translation table."""
from __future__ import annotations

import json
from pathlib import Path

from i18n_constants import LANGS

GAPS_PATH = Path("/tmp/i18n_gaps.json")
TABLE_PATH = Path(__file__).resolve().parent / "i18n_string_table.json"


def load_table() -> dict[str, dict[str, str]]:
    return json.loads(TABLE_PATH.read_text(encoding="utf-8"))


def load_gaps() -> dict[str, str]:
    gaps = json.loads(GAPS_PATH.read_text(encoding="utf-8"))
    return {f"{sec}.{k}": v for sec, keys in gaps.items() for k, v in keys.items()}


def build_patches() -> dict[str, dict[str, str]]:
    table = load_table()
    gaps = load_gaps()
    patches: dict[str, dict[str, str]] = {}
    for path, en in gaps.items():
        if en not in table:
            continue
        entry = {lang: table[en][lang] for lang in LANGS}
        patches[path] = entry
    return patches


PATCHES = build_patches()
