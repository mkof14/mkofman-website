#!/usr/bin/env python3
"""Patch missing page-content.js keys for Chromox entry and portfolio links."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PC_PATH = ROOT / "js" / "page-content.js"

PATCHES = {
    "es": {
        "ventures": {
            "v1p2": "Iniciativas de cartera: <a href=\"https://biomathlife.com\" target=\"_blank\" rel=\"noopener\">BioMath Life</a>, <a href=\"https://www.biomathcore.com\" target=\"_blank\" rel=\"noopener\">BioMath Core</a>, <a href=\"https://www.type1and2.com\" target=\"_blank\" rel=\"noopener\">Type 1 &amp; 2</a> y <a href=\"https://www.luna29.com\" target=\"_blank\" rel=\"noopener\">Luna29</a> — casos de estudio detallados próximamente.",
            "v1brole": "CEO",
            "v1bp1": "Período de transición entre biotecnología y nuevo desarrollo tecnológico — experiencia operativa y de I+D antes de Digital Invest Inc.",
            "v1byear": "2014 — 2020",
        },
        "career": {
            "t1bdesc": "Período de transición entre biotecnología y nuevo desarrollo tecnológico — experiencia operativa y de I+D antes de Digital Invest Inc.",
            "t1brole": "CEO",
            "t1byear": "2014 — 2020",
        },
    },
    "de": {
        "ventures": {
            "v1p2": "Portfolio-Initiativen: <a href=\"https://biomathlife.com\" target=\"_blank\" rel=\"noopener\">BioMath Life</a>, <a href=\"https://www.biomathcore.com\" target=\"_blank\" rel=\"noopener\">BioMath Core</a>, <a href=\"https://www.type1and2.com\" target=\"_blank\" rel=\"noopener\">Type 1 &amp; 2</a> und <a href=\"https://www.luna29.com\" target=\"_blank\" rel=\"noopener\">Luna29</a> — ausführliche Fallstudien folgen.",
            "v1brole": "CEO",
            "v1bp1": "Übergangszeit zwischen Biotechnologie und neuer Technologieentwicklung — operative und F&E-Erfahrung vor Digital Invest Inc.",
            "v1byear": "2014 — 2020",
        },
        "career": {
            "t1bdesc": "Übergangszeit zwischen Biotechnologie und neuer Technologieentwicklung — operative und F&E-Erfahrung vor Digital Invest Inc.",
            "t1brole": "CEO",
            "t1byear": "2014 — 2020",
        },
    },
    "fr": {
        "ventures": {
            "v1p2": "Initiatives du portefeuille : <a href=\"https://biomathlife.com\" target=\"_blank\" rel=\"noopener\">BioMath Life</a>, <a href=\"https://www.biomathcore.com\" target=\"_blank\" rel=\"noopener\">BioMath Core</a>, <a href=\"https://www.type1and2.com\" target=\"_blank\" rel=\"noopener\">Type 1 &amp; 2</a> et <a href=\"https://www.luna29.com\" target=\"_blank\" rel=\"noopener\">Luna29</a> — études de cas détaillées à venir.",
            "v1brole": "PDG",
            "v1bp1": "Période de transition entre biotechnologie et nouveau développement technologique — expérience opérationnelle et R&D avant Digital Invest Inc.",
            "v1byear": "2014 — 2020",
        },
        "career": {
            "t1bdesc": "Période de transition entre biotechnologie et nouveau développement technologique — expérience opérationnelle et R&D avant Digital Invest Inc.",
            "t1brole": "PDG",
            "t1byear": "2014 — 2020",
        },
    },
    "ru": {
        "ventures": {
            "v1p2": "Портфельные инициативы: <a href=\"https://biomathlife.com\" target=\"_blank\" rel=\"noopener\">BioMath Life</a>, <a href=\"https://www.biomathcore.com\" target=\"_blank\" rel=\"noopener\">BioMath Core</a>, <a href=\"https://www.type1and2.com\" target=\"_blank\" rel=\"noopener\">Type 1 &amp; 2</a> и <a href=\"https://www.luna29.com\" target=\"_blank\" rel=\"noopener\">Luna29</a> — подробные кейсы будут опубликованы позже.",
            "v1brole": "CEO",
            "v1bp1": "Переходный период между биотехнологией и новой технологической разработкой — операционный и R&D опыт перед Digital Invest Inc.",
            "v1byear": "2014 — 2020",
        },
        "career": {
            "t1bdesc": "Переходный период между биотехнологией и новой технологической разработкой — операционный и R&D опыт перед Digital Invest Inc.",
            "t1brole": "CEO",
            "t1byear": "2014 — 2020",
        },
    },
    "uk": {
        "ventures": {
            "v1p2": "Портфельні ініціативи: <a href=\"https://biomathlife.com\" target=\"_blank\" rel=\"noopener\">BioMath Life</a>, <a href=\"https://www.biomathcore.com\" target=\"_blank\" rel=\"noopener\">BioMath Core</a>, <a href=\"https://www.type1and2.com\" target=\"_blank\" rel=\"noopener\">Type 1 &amp; 2</a> та <a href=\"https://www.luna29.com\" target=\"_blank\" rel=\"noopener\">Luna29</a> — детальні кейси будуть опубліковані пізніше.",
            "v1brole": "CEO",
            "v1bp1": "Перехідний період між біотехнологією та новою технологічною розробкою — операційний і R&D досвід перед Digital Invest Inc.",
            "v1byear": "2014 — 2020",
        },
        "career": {
            "t1bdesc": "Перехідний період між біотехнологією та новою технологічною розробкою — операційний і R&D досвід перед Digital Invest Inc.",
            "t1brole": "CEO",
            "t1byear": "2014 — 2020",
        },
    },
    "zh": {
        "ventures": {
            "v1p2": "投资组合项目包括 <a href=\"https://biomathlife.com\" target=\"_blank\" rel=\"noopener\">BioMath Life</a>、<a href=\"https://www.biomathcore.com\" target=\"_blank\" rel=\"noopener\">BioMath Core</a>、<a href=\"https://www.type1and2.com\" target=\"_blank\" rel=\"noopener\">Type 1 &amp; 2</a> 和 <a href=\"https://www.luna29.com\" target=\"_blank\" rel=\"noopener\">Luna29</a> — 详细案例研究将陆续发布。",
            "v1brole": "首席执行官",
            "v1bp1": "生物技术工作向新技术开发过渡的时期 — 在 Digital Invest Inc. 之前积累运营和研发经验。",
            "v1byear": "2014 — 2020",
        },
        "career": {
            "t1bdesc": "生物技术工作向新技术开发过渡的时期 — 在 Digital Invest Inc. 之前积累运营和研发经验。",
            "t1brole": "首席执行官",
            "t1byear": "2014 — 2020",
        },
    },
    "ar": {
        "ventures": {
            "v1p2": "مبادرات المحفظة تشمل <a href=\"https://biomathlife.com\" target=\"_blank\" rel=\"noopener\">BioMath Life</a> و<a href=\"https://www.biomathcore.com\" target=\"_blank\" rel=\"noopener\">BioMath Core</a> و<a href=\"https://www.type1and2.com\" target=\"_blank\" rel=\"noopener\">Type 1 &amp; 2</a> و<a href=\"https://www.luna29.com\" target=\"_blank\" rel=\"noopener\">Luna29</a> — دراسات حالة مفصلة قريباً.",
            "v1brole": "الرئيس التنفيذي",
            "v1bp1": "فترة انتقالية بين العمل في التكنولوجيا الحيوية وتطوير تقنيات جديدة — بناء خبرة تشغيلية وبحث وتطوير قبل Digital Invest Inc.",
            "v1byear": "2014 — 2020",
        },
        "career": {
            "t1bdesc": "فترة انتقالية بين العمل في التكنولوجيا الحيوية وتطوير تقنيات جديدة — بناء خبرة تشغيلية وبحث وتطوير قبل Digital Invest Inc.",
            "t1brole": "الرئيس التنفيذي",
            "t1byear": "2014 — 2020",
        },
    },
    "he": {
        "ventures": {
            "v1p2": "יוזמות בתיק כוללות <a href=\"https://biomathlife.com\" target=\"_blank\" rel=\"noopener\">BioMath Life</a>, <a href=\"https://www.biomathcore.com\" target=\"_blank\" rel=\"noopener\">BioMath Core</a>, <a href=\"https://www.type1and2.com\" target=\"_blank\" rel=\"noopener\">Type 1 &amp; 2</a> ו-<a href=\"https://www.luna29.com\" target=\"_blank\" rel=\"noopener\">Luna29</a> — מחקרי מקרה מפורטים יעלו בהמשך.",
            "v1brole": "מנכ\"ל",
            "v1bp1": "תקופת מעבר בין ביוטכנולוגיה לפיתוח טכנולוגי חדש — בניית ניסיון תפעולי ו-R&D לפני Digital Invest Inc.",
            "v1byear": "2014 — 2020",
        },
        "career": {
            "t1bdesc": "תקופת מעבר בין ביוטכנולוגיה לפיתוח טכנולוגי חדש — בניית ניסיון תפעולי ו-R&D לפני Digital Invest Inc.",
            "t1brole": "מנכ\"ל",
            "t1byear": "2014 — 2020",
        },
    },
}


def deep_merge(base: dict, patch: dict) -> None:
    for key, value in patch.items():
        if isinstance(value, dict) and isinstance(base.get(key), dict):
            deep_merge(base[key], value)
        else:
            base[key] = value


def main() -> None:
    raw = PC_PATH.read_text(encoding="utf-8")
    data = json.loads(raw[raw.find("{") : raw.rfind("}") + 1])
    for lang, patch in PATCHES.items():
        if lang not in data:
            data[lang] = {}
        deep_merge(data[lang], patch)
    PC_PATH.write_text(
        "const PAGE_CONTENT = " + json.dumps(data, ensure_ascii=False, indent=2) + ";\n",
        encoding="utf-8",
    )
    print(f"Patched page-content.js for {len(PATCHES)} languages")


if __name__ == "__main__":
    main()
