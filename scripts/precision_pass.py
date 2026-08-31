#!/usr/bin/env python3
"""Apply precision editorial pass updates across translations and page-content."""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# --- translations.js bulk patches per language ---
LANG_HOME = {
    "es": {
        "careerEyebrow": "Selected Record",
        "recEyebrow": "Reconocimientos",
        "award1desc": "Entrepreneur Magazine · 2001",
        "heroSub": "Technology, business, and investment across infrastructure, life sciences, and autonomous systems.",
        "introText": (
            "Michael Kofman is a technology executive and company founder. His work spans satellite engineering, "
            "internet infrastructure, public technology companies, and life sciences. He founded 9 Net Avenue Inc., "
            "acquired by Concentric Networks in 2000. He is CEO of Digital Invest Inc., in bio-mathematical medicine "
            "and genomic intelligence, and founder of AGRON Inc., in autonomous aerial-ground operations and geospatial "
            "systems. He serves on boards and advises in technology, health, and infrastructure."
        ),
    },
    "de": {
        "careerEyebrow": "Selected Record",
        "recEyebrow": "Anerkennung",
        "award1desc": "Entrepreneur Magazine · 2001",
    },
    "fr": {
        "careerEyebrow": "Selected Record",
        "recEyebrow": "Distinctions",
        "award1desc": "Entrepreneur Magazine · 2001",
    },
    "ru": {
        "careerEyebrow": "Selected Record",
        "recEyebrow": "Признание",
        "award1desc": "Entrepreneur Magazine · 2001",
    },
    "uk": {
        "careerEyebrow": "Selected Record",
        "recEyebrow": "Визнання",
        "award1desc": "Entrepreneur Magazine · 2001",
    },
    "zh": {
        "careerEyebrow": "Selected Record",
        "recEyebrow": "荣誉",
        "award1desc": "Entrepreneur Magazine · 2001",
    },
    "ar": {
        "careerEyebrow": "Selected Record",
        "recEyebrow": "التكريم",
        "award1desc": "Entrepreneur Magazine · 2001",
    },
    "he": {
        "careerEyebrow": "Selected Record",
        "recEyebrow": "הכרה",
        "award1desc": "Entrepreneur Magazine · 2001",
    },
}

FOOTER_DESC = "Technology executive, founder, and board advisor."

NAV_CAREER = "The Record"

INSIGHTS_EYEBROW = {
    "es": "Perspectivas",
    "de": "Perspektiven",
    "fr": "Perspectives",
    "ru": "Перспективы",
    "uk": "Перспективи",
    "zh": "观点",
    "ar": "Perspectives",
    "he": "Perspectives",
}


def load_translations() -> dict:
    raw = (ROOT / "js" / "translations.js").read_text(encoding="utf-8")
    start = raw.find("{")
    end = raw.rfind("}")
    return json.loads(raw[start : end + 1])


def save_translations(data: dict) -> None:
    payload = json.dumps(data, ensure_ascii=False, indent=2)
    (ROOT / "js" / "translations.js").write_text(
        "const TRANSLATIONS = " + payload + ";\n", encoding="utf-8"
    )


def patch_translations(data: dict) -> None:
    en = data["en"]

    # EN deck — remove promotional stats language
    en["deck"] = {
        "title": "Michael Kofman",
        "subtitle": "Technology Executive · Founder · Board Advisor",
        "thesis": (
            "Technology, business, and investment across infrastructure, life sciences, and autonomous systems."
        ),
        "contact": "Confidential discussion: contact Michael Kofman through mkofman.com",
    }

    # EN case studies factual softening
    cs = en["caseStudies"]
    cs["cs1actionText"] = (
        "Founded 9 Net Avenue Inc. in 1996 as a hosting and internet infrastructure company."
    )
    cs["cs2challengeText"] = (
        "Apply science, DNA technologies, AI, and ML through a bio-mathematical platform in medicine."
    )
    cs["cs2resultText"] = (
        "Healthcare Tech Outlook feature (2023). Projects include Human Digital Model and BioMath Life."
    )
    cs["cs3resultText"] = (
        "A connected professional services ecosystem spanning consulting, capability development, training "
        "infrastructure, geospatial systems, and maritime intelligence through AGRON, ISDRI, and related companies."
    )

    # EN articles
    art = en["articles"]
    art["article2p1"] = (
        "Life sciences advance when rigorous technology is applied to evidence, interpretation, and clinical utility."
    )
    art["article1p2"] = (
        "From 1989 to 1994, I founded and led Astra Corp, a manufacturer of digital transceiver satellite systems. "
        "From 1994 to 1996, as CEO of Elitan United Inc., I led IT strategy and infrastructure during a period of rapid expansion."
    )

    # EN press
    en["press"]["y2023title"] = "Healthcare Tech Outlook Feature"

    for lang, home_patch in LANG_HOME.items():
        if lang not in data:
            continue
        block = data[lang]
        block.setdefault("home", {}).update(home_patch)
        block.setdefault("footer", {})["desc"] = FOOTER_DESC
        if "career" in block.get("nav", {}):
            block["nav"]["career"] = NAV_CAREER
        if lang in INSIGHTS_EYEBROW:
            block.setdefault("insights", {})["eyebrow"] = INSIGHTS_EYEBROW[lang]
        # Normalize dates / labels in home blocks
        home = block.get("home", {})
        if "quote2author" in home:
            home["quote2author"] = "Entrepreneur Magazine · 2001"
        if "award1desc" in home and "2001" not in home["award1desc"]:
            home["award1desc"] = "Entrepreneur Magazine · 2001"
        if home.get("careerEyebrow") == "Selected Career":
            home["careerEyebrow"] = "Selected Record"
        if home.get("heroAlt", "").endswith("Strategic Technologist"):
            home["heroAlt"] = "Michael Kofman"

    # All langs: footer desc, nav career, insights eyebrow Thought Leadership
    for lang, block in data.items():
        if lang == "en":
            continue
        block.setdefault("footer", {})["desc"] = FOOTER_DESC
        if "career" in block.get("nav", {}):
            block["nav"]["career"] = NAV_CAREER
        ins = block.get("insights", {})
        if ins.get("eyebrow") == "Thought Leadership":
            ins["eyebrow"] = INSIGHTS_EYEBROW.get(lang, "Perspectives")
        home = block.get("home", {})
        if home.get("careerEyebrow") == "Selected Career":
            home["careerEyebrow"] = "Selected Record"
        if "award1desc" in home and "1999" in home["award1desc"]:
            home["award1desc"] = "Entrepreneur Magazine · 2001"
        if home.get("heroAlt", "").endswith("Strategic Technologist"):
            home["heroAlt"] = "Michael Kofman"
        if home.get("recEyebrow") == "Record":
            home["recEyebrow"] = block.get("nav", {}).get("recognition", "Recognition")


def patch_page_content() -> None:
    path = ROOT / "js" / "page-content.js"
    text = path.read_text(encoding="utf-8")

    en_ventures = {
        'v1highlight": "Top 10 U.S. Precision Medicine Company — 2023"':
            'v1highlight": "Healthcare Tech Outlook feature — 2023"',
        'v1p1": "Bio-mathematical medicine, genomic data, and clinical intelligence — AI, machine learning, and DNA technologies applied to responsible health outcomes."':
            'v1p1": "Bio-mathematical medicine, genomic data, and clinical intelligence — AI, machine learning, and DNA technologies applied to clinical and research workflows."',
        'v2p2": "Collaborated with Harvard Medical School and Stanford Biomath on genetic reports adopted by leading laboratories worldwide."':
            'v2p2": "Collaborated with Harvard Medical School and Stanford Biomath on genetic reporting formats used in laboratory workflows."',
    }
    for old, new in en_ventures.items():
        text = text.replace(old, new)

    en_career = {
        's1desc": "Dual-sided CEO/CTO management across public and private companies, from startup to IPO and beyond."':
            's1desc": "CEO/CTO leadership across public and private companies, from early stage through scale."',
        't3desc": "Led DNA testing and analysis, automation of genetic profiling, and comprehensive human genetic research. Initiated genetic testing projects in Ukraine, Russia, and the Baltic countries. Collaborated with Harvard Medical School and Stanford Biomath to develop understandable genetic reports adopted by leading laboratories worldwide."':
            't3desc": "Led DNA testing and analysis, automation of genetic profiling, and human genetic research. Initiated genetic testing projects in Ukraine, Russia, and the Baltic countries. Collaborated with Harvard Medical School and Stanford Biomath on genetic reporting formats used in laboratory workflows."',
        't2desc": "Directed technology strategy and delivery for classified and high-sensitivity programs involving U.S. government agencies, allied defense systems, and state-owned enterprises. Headed complex technical projects for government-owned companies across multiple sectors. Following September 11, 2001, led large-scale government initiatives centered on big data, secure communications, predictive analytics, and national-level data integration — including the design, construction, and operation of high-throughput data centers across the United States and Europe. Interfaced with military program officers, technology vendors, and regulatory entities."':
            't2desc": "Directed technology strategy and delivery for government, defense, and state-owned enterprise programs — including secure infrastructure, data integration, and high-throughput data centers in the U.S. and Europe."',
        't4desc": "Directed national infrastructure rollouts across Canada, Italy, Switzerland, Ukraine, and the Baltic Republics. Oversaw 1,000+ engineering and deployment staff across telecom operations including switching systems, broadband expansion, and cross-border connectivity. Implemented core systems for network redundancy, uptime optimization, and intelligent routing."':
            't4desc": "Directed national infrastructure rollouts across Canada, Italy, Switzerland, Ukraine, and the Baltic Republics. Oversaw large engineering and deployment teams across telecom operations including switching systems, broadband expansion, and cross-border connectivity."',
        't9desc": "Founded one of Europe\'s largest manufacturers of digital transceiver satellite systems. Led research, operating system development, network software applications, and overall technical strategy, earning international recognition."':
            't9desc": "Founded Astra Corp, a manufacturer of digital transceiver satellite systems. Led research, operating system development, network software applications, and technical strategy."',
    }
    for old, new in en_career.items():
        text = text.replace(old, new)

    # All-lang recognition a1desc — strip promotional suffixes
    text = re.sub(
        r'"a1desc": "Entrepreneur Magazine[^"]*"',
        '"a1desc": "Entrepreneur Magazine · 2001"',
        text,
    )

    ip_old = (
        'Received a patent in the field of digital satellite high-definition television (HDTV) systems. '
        "The patent was subsequently acquired by Sony Corporation, validating the innovation's commercial significance."
    )
    ip_new = (
        "Patent in digital satellite high-definition television (HDTV) systems, "
        "subsequently acquired by Sony Corporation."
    )
    text = text.replace(ip_old, ip_new)
    text = text.replace('"ip1role": "Subsequently Acquired by Sony"', '"ip1role": "Patent acquired by Sony Corporation"')

    press_old = (
        "Digital Invest Inc. featured as one of America's leading companies in precision medicine and digital health, "
        "recognized for innovative approaches to transforming medicine through AI, ML, and DNA technologies."
    )
    press_new = "Healthcare Tech Outlook feature on Digital Invest Inc. and precision medicine (2023)."
    text = text.replace(press_old, press_new)

    press2_old = (
        "Named among the top precision medicine solutions companies, highlighting Digital Invest's role in "
        "advancing bio-mathematical approaches to modern healthcare."
    )
    press2_new = "Listed among precision medicine solutions companies · Digital Invest Inc."
    text = text.replace(press2_old, press2_new)

    path.write_text(text, encoding="utf-8")


def patch_html_fallbacks() -> None:
    replacements = [
        (
            "Entrepreneur Magazine, 1999 — 2001 — leadership and breakthrough achievements in platform innovation and infrastructure.",
            "Entrepreneur Magazine · 2001",
        ),
        (
            "Entrepreneur Magazine · 1999 — 2001",
            "Entrepreneur Magazine · 2001",
        ),
        (
            '<span class="insights-date">1999 — 2001</span>',
            '<span class="insights-date">2001</span>',
        ),
        (
            "Received a patent in the field of digital satellite high-definition television (HDTV) systems. The patent was subsequently acquired by Sony Corporation, validating the innovation's commercial significance.",
            "Patent in digital satellite high-definition television (HDTV) systems, subsequently acquired by Sony Corporation.",
        ),
        (
            "Subsequently Acquired by Sony",
            "Patent acquired by Sony Corporation",
        ),
        (
            "Digital Invest Inc. featured as one of America's leading companies in precision medicine and digital health, recognized for innovative approaches to transforming medicine through AI, ML, and DNA technologies.",
            "Healthcare Tech Outlook feature on Digital Invest Inc. and precision medicine (2023).",
        ),
        (
            "Named among the top precision medicine solutions companies, highlighting Digital Invest's role in advancing bio-mathematical approaches to modern healthcare.",
            "Listed among precision medicine solutions companies · Digital Invest Inc.",
        ),
        (
            "CEO · Board Advisor · Strategic Technologist",
            "Technology Executive · Founder · Board Advisor",
        ),
        (
            '<h3 data-i18n="thesis.b1title">Principle</h3>\n            <p data-i18n="thesis.b1text">Text</p>',
            '<h3 data-i18n="thesis.b1title">Strategy Must Produce Choices</h3>\n            <p data-i18n="thesis.b1text">A strategy is not a catalog of aspirations. It defines where to compete, what capabilities to build, what not to pursue, and how success will be measured.</p>',
        ),
    ]
    for html_path in ROOT.glob("*.html"):
        text = html_path.read_text(encoding="utf-8")
        orig = text
        for old, new in replacements:
            text = text.replace(old, new)
        if html_path.name == "deck.html":
            text = re.sub(
                r'\s*<div class="deck-stat-row">.*?</div>\s*',
                "\n",
                text,
                flags=re.S,
            )
        if text != orig:
            html_path.write_text(text, encoding="utf-8")
            print("html:", html_path.name)


def patch_thesis_fallbacks() -> None:
    path = ROOT / "thesis.html"
    text = path.read_text(encoding="utf-8")
    # Replace remaining Principle/Text placeholders using en thesis keys - read from translations
    data = load_translations()
    th = data["en"]["thesis"]
    for i in range(1, 8):
        text = text.replace(
            f'<h3 data-i18n="thesis.b{i}title">Principle</h3>\n            <p data-i18n="thesis.b{i}text">Text</p>',
            f'<h3 data-i18n="thesis.b{i}title">{th[f"b{i}title"]}</h3>\n            <p data-i18n="thesis.b{i}text">{th[f"b{i}text"]}</p>',
        )
    path.write_text(text, encoding="utf-8")
    print("html: thesis.html (principles)")


def main() -> None:
    data = load_translations()
    patch_translations(data)
    save_translations(data)
    patch_page_content()
    patch_html_fallbacks()
    patch_thesis_fallbacks()
    print("precision_pass ok")


if __name__ == "__main__":
    main()
