#!/usr/bin/env python3
"""Add AGRON Inc. across site; remove Digital Invest ecosystem diagram."""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

FOOTER_AGRON = (
    '            <li><a href="https://agron1.com" target="_blank" rel="noopener">AGRON Inc.</a></li>\n'
)

AGRON_VENTURE_CARD = """
        <article class="venture-card fade-in" id="agron" data-tags="defense infrastructure">
          <span class="venture-status" data-i18n="ventures.statusActive">Active</span>
          <div class="venture-card-header">
            <div class="venture-year" data-period-start="2026" data-period-end="present" data-i18n="ventures.v0year">2026 — Present</div>
            <h3><a href="https://agron1.com" target="_blank" rel="noopener">AGRON Inc.</a></h3>
            <div class="venture-role" data-i18n="ventures.v0role">Founder</div>
          </div>
          <div class="venture-card-body">
            <p data-i18n="ventures.v0p1">Founded AGRON Inc. in 2026 to lead the AGRON Ecosystem — an Aerial-Ground Robotics Operations Network spanning UAV and Counter-UAS consulting, technology assessment, capability development, training infrastructure, product validation, geospatial systems (ISDRI), and AGRON Maritime Intelligence + Security for yachts, marinas, and private maritime infrastructure.</p>
            <span class="venture-highlight" data-i18n="ventures.v0highlight">Aerial-Ground Robotics Operations Network · agron1.com</span>
          </div>
        </article>

"""

CAREER_AGRON = """
        <div class="timeline-item" data-tags="defense infrastructure">
          <div class="timeline-year" data-i18n="career.t0year">2026 — Present</div>
          <div class="timeline-title">AGRON Inc.</div>
          <div class="timeline-role" data-i18n="career.t0role">Founder</div>
          <div class="timeline-desc" data-i18n="career.t0desc">
            Founded AGRON Inc. to build the AGRON Ecosystem — consulting, assessment, capability development, training infrastructure, and product support for UAV and Counter-UAS programmes, plus AGRON Maritime Intelligence + Security for yachts, marinas, and private maritime infrastructure. Connects aerial and ground robotics, governed mission execution, and network infrastructure linking teams, assets, and operational data.
          </div>
        </div>

"""

ABOUT_AGRON = """
          <h3 data-i18n="about.secAgronTitle">Robotics, UAV & Maritime Intelligence</h3>
          <p data-i18n="about.secAgronP1">In 2026, Mr. Kofman founded AGRON Inc. to build the AGRON Ecosystem — a corporate operating architecture for aerial and ground robotics, governed mission execution, and network infrastructure connecting teams, assets, and operational data. The ecosystem delivers consulting, assessment, capability development, and training for UAV and Counter-UAS organizations, alongside maritime intelligence and security services at agron1.com.</p>

"""

CASE_AGRON = """
  <section id="agron" class="section section-cream">
    <div class="container container-narrow">
      <article class="venture-card fade-in">
        <div class="venture-card-header">
          <div class="venture-year" data-i18n="caseStudies.cs3eyebrow">Robotics & UAV · 2026 — Present</div>
          <h2 data-i18n="caseStudies.cs3title">AGRON Inc.</h2>
        </div>
        <div class="venture-card-body">
          <h3 data-i18n="caseStudies.cs3challenge">Challenge</h3>
          <p data-i18n="caseStudies.cs3challengeText">Organizations building UAV and Counter-UAS capability need independent assessment, structured training, and operational architecture — not isolated platforms or ad-hoc piloting.</p>
          <h3 data-i18n="caseStudies.cs3action">Approach</h3>
          <p data-i18n="caseStudies.cs3actionText">Founded AGRON Inc. in 2026 to lead the AGRON Ecosystem — consulting, assessment and validation, capability development, training infrastructure, product development support, geospatial systems through ISDRI, and AGRON Maritime Intelligence + Security for yachts, marinas, and private maritime infrastructure.</p>
          <h3 data-i18n="caseStudies.cs3result">Outcome</h3>
          <p data-i18n="caseStudies.cs3resultText">A connected professional services ecosystem spanning five service domains and multiple companies — Global Drone Academy, AGRON, ISDRI, and GUARD — with programmes delivered across 10+ countries and 10,000+ UAV operators, instructors, and specialists trained.</p>
          <p><a href="https://agron1.com" target="_blank" rel="noopener" class="text-link">agron1.com →</a></p>
        </div>
      </article>
    </div>
  </section>

"""

INDEX_CS3 = """
        <article class="insights-post fade-in">
          <h3 data-i18n="home.cs3title">AGRON Inc.</h3>
          <p data-i18n="home.cs3desc">Founded in 2026 — the AGRON Ecosystem for UAV capability development, geospatial systems, and maritime intelligence.</p>
          <a href="case-studies.html#agron" class="text-link">Read Case Study →</a>
        </article>
"""

PAGE_CONTENT_V0 = {
    "v0year": "2026 — Present",
    "v0role": "Founder",
    "v0p1": (
        "Founded AGRON Inc. in 2026 to lead the AGRON Ecosystem — an Aerial-Ground Robotics Operations Network "
        "spanning UAV and Counter-UAS consulting, technology assessment, capability development, training infrastructure, "
        "product validation, geospatial systems (ISDRI), and AGRON Maritime Intelligence + Security for yachts, marinas, "
        "and private maritime infrastructure."
    ),
    "v0highlight": "Aerial-Ground Robotics Operations Network · agron1.com",
}

PAGE_CONTENT_T0 = {
    "t0year": "2026 — Present",
    "t0title": "AGRON Inc.",
    "t0role": "Founder",
    "t0desc": (
        "Founded AGRON Inc. to build the AGRON Ecosystem — consulting, assessment, capability development, training "
        "infrastructure, and product support for UAV and Counter-UAS programmes, plus AGRON Maritime Intelligence + "
        "Security for yachts, marinas, and private maritime infrastructure. Connects aerial and ground robotics, "
        "governed mission execution, and network infrastructure linking teams, assets, and operational data."
    ),
}

PAGE_CONTENT_ABOUT = {
    "secAgronTitle": "Robotics, UAV & Maritime Intelligence",
    "secAgronP1": (
        "In 2026, Mr. Kofman founded AGRON Inc. to build the AGRON Ecosystem — a corporate operating architecture for "
        "aerial and ground robotics, governed mission execution, and network infrastructure connecting teams, assets, and "
        "operational data. The ecosystem delivers consulting, assessment, capability development, and training for UAV and "
        "Counter-UAS organizations, alongside maritime intelligence and security services at agron1.com."
    ),
    "bioP1": (
        "Michael Kofman is the CEO of Digital Invest Inc. and founder of AGRON Inc. He serves on the Digital Invest Board "
        "of Directors. A technological visionary, he is renowned for his dynamic approach to understanding the "
        "ever-evolving needs of today's complex market. His expertise spans executive acumen, strategic analysis of "
        "emerging technologies and markets, information security and privacy, research, science and development, "
        "administration, and investment."
    ),
    "bioP2": (
        "As an entrepreneur, board member, and advisor for both public and private companies, Michael Kofman has "
        "successfully established several companies in the United States and Europe. In 2026 he founded AGRON Inc. to "
        "lead the Aerial-Ground Robotics Operations Network. He also created Digital Invest, dedicated to the "
        "bio-mathematical sphere and transforming medicine through science, DNA technologies, AI, and ML."
    ),
}

# Per-language overrides for page-content (non-English)
LANG_OVERRIDES: dict[str, dict] = {
    "ru": {
        "ventures": {
            **PAGE_CONTENT_V0,
            "v0year": "2026 — настоящее время",
            "v0role": "Основатель",
            "v0p1": (
                "В 2026 году основал AGRON Inc. для развития экосистемы AGRON — Aerial-Ground Robotics Operations Network: "
                "консалтинг и оценка БПЛА и Counter-UAS, развитие компетенций, обучающая инфраструктура, валидация продуктов, "
                "геопространственные системы (ISDRI) и AGRON Maritime Intelligence + Security для яхт, марин и частной "
                "морской инфраструктуры."
            ),
            "v0highlight": "Aerial-Ground Robotics Operations Network · agron1.com",
        },
        "career": PAGE_CONTENT_T0
        | {
            "t0year": "2026 — настоящее время",
            "t0role": "Основатель",
            "t0desc": (
                "Основал AGRON Inc. для построения экосистемы AGRON — консалтинг, оценка, развитие компетенций, "
                "обучающая инфраструктура и поддержка продуктов для программ БПЛА и Counter-UAS, а также AGRON Maritime "
                "Intelligence + Security. Объединяет воздушную и наземную робототехнику, управляемое выполнение миссий "
                "и сетевую инфраструктуру, связывающую команды, активы и операционные данные."
            ),
        },
        "about": {
            "secAgronTitle": "Робототехника, БПЛА и морская разведка",
            "secAgronP1": (
                "В 2026 году г-н Kofman основал AGRON Inc. для построения экосистемы AGRON — корпоративной архитектуры "
                "воздушной и наземной робототехники, управляемого выполнения миссий и сетевой инфраструктуры. Экосистема "
                "включает консалтинг, оценку, развитие компетенций и обучение для организаций БПЛА и Counter-UAS, а также "
                "морскую разведку и безопасность на agron1.com."
            ),
            "bioP1": PAGE_CONTENT_ABOUT["bioP1"].replace(
                "Michael Kofman is the CEO of Digital Invest Inc. and founder of AGRON Inc.",
                "Michael Kofman — CEO Digital Invest Inc. и основатель AGRON Inc.",
            ),
            "bioP2": (
                "Как предприниматель, член советов директоров и советник публичных и частных компаний, Michael Kofman "
                "основал несколько компаний в США и Европе. В 2026 году он основал AGRON Inc. для развития Aerial-Ground "
                "Robotics Operations Network. Также создал Digital Invest — компанию в биоматематической сфере, "
                "трансформирующую медицину с помощью науки, ДНК-технологий, ИИ и ML."
            ),
        },
    },
    "uk": {
        "ventures": {
            **PAGE_CONTENT_V0,
            "v0year": "2026 — дотепер",
            "v0role": "Засновник",
            "v0p1": (
                "У 2026 році заснув AGRON Inc. для розвитку екосистеми AGRON — Aerial-Ground Robotics Operations Network: "
                "консалтинг і оцінка БПЛА та Counter-UAS, розвиток компетенцій, навчальна інфраструктура, валідація продуктів, "
                "геопросторові системи (ISDRI) та AGRON Maritime Intelligence + Security для яхт, марин і приватної "
                "морської інфраструктури."
            ),
            "v0highlight": "Aerial-Ground Robotics Operations Network · agron1.com",
        },
        "career": PAGE_CONTENT_T0
        | {
            "t0year": "2026 — дотепер",
            "t0role": "Засновник",
            "t0desc": (
                "Заснув AGRON Inc. для побудови екосистеми AGRON — консалтинг, оцінка, розвиток компетенцій, "
                "навчальна інфраструктура та підтримка продуктів для програм БПЛА і Counter-UAS, а також AGRON Maritime "
                "Intelligence + Security. Поєднує повітряну та наземну робототехніку, кероване виконання місій "
                "та мережеву інфраструктуру, що з'єднує команди, активи та операційні дані."
            ),
        },
        "about": {
            "secAgronTitle": "Робототехніка, БПЛА та морська розвідка",
            "secAgronP1": (
                "У 2026 році пан Kofman заснув AGRON Inc. для побудови екосистеми AGRON — корпоративної архітектури "
                "повітряної та наземної робототехніки, керованого виконання місій і мережевої інфраструктури. Екосистема "
                "включає консалтинг, оцінку, розвиток компетенцій і навчання для організацій БПЛА та Counter-UAS, а також "
                "морську розвідку та безпеку на agron1.com."
            ),
            "bioP2": (
                "Як підприємець, член рад директорів і радник публічних і приватних компаній, Michael Kofman "
                "заснував кілька компаній у США та Європі. У 2026 році він заснув AGRON Inc. для розвитку Aerial-Ground "
                "Robotics Operations Network. Також створив Digital Invest — компанію в біоматематичній сфері, "
                "що трансформує медицину за допомогою науки, ДНК-технологій, ШІ та ML."
            ),
        },
    },
}


def patch_ventures_html(html: str) -> str:
    html = re.sub(
        r"\n  <section class=\"section section-white\">.*?ecosystem-map.*?</section>\n  </section>",
        "\n  </section>",
        html,
        count=1,
        flags=re.S,
    )
    if 'id="agron"' not in html:
        html = html.replace(
            '<div class="ventures-grid">\n\n        <article class="venture-card fade-in" data-tags="healthcare infrastructure">',
            f'<div class="ventures-grid">\n{AGRON_VENTURE_CARD}\n        <article class="venture-card fade-in" data-tags="healthcare infrastructure">',
        )
    html = html.replace(
        "from Digital Invest Inc. to 9 Net Avenue Inc.",
        "from AGRON Inc. to 9 Net Avenue Inc.",
    )
    return html


def patch_career_html(html: str) -> str:
    if 'data-i18n="career.t0year"' not in html:
        html = html.replace(
            '      <div class="timeline fade-in">\n\n        <div class="timeline-item" data-tags="healthcare infrastructure">',
            f'      <div class="timeline fade-in">\n{CAREER_AGRON}\n        <div class="timeline-item" data-tags="healthcare infrastructure">',
        )
    return html


def patch_about_html(html: str) -> str:
    if 'data-i18n="about.secAgronTitle"' not in html:
        html = html.replace(
            '          <h3 data-i18n="about.secTechTitle">Technology & Infrastructure</h3>',
            ABOUT_AGRON + '\n          <h3 data-i18n="about.secTechTitle">Technology & Infrastructure</h3>',
        )
    return html


def patch_case_studies_html(html: str) -> str:
    if 'id="agron"' not in html:
        html = html.replace(
            '  <section id="digital-invest"',
            CASE_AGRON + '\n  <section id="digital-invest"',
        )
    for old, new in [
        (
            "Case studies from Michael Kofman's career — 9 Net Avenue Inc. and Digital Invest Inc.",
            "Case studies from Michael Kofman's career — AGRON Inc., 9 Net Avenue Inc., and Digital Invest Inc.",
        ),
        (
            "Selected outcomes from founding and leading companies across data infrastructure and digital health.",
            "Selected outcomes from founding and leading companies across robotics, data infrastructure, and digital health.",
        ),
    ]:
        html = html.replace(old, new)
    return html


def patch_index_html(html: str) -> str:
    html = html.replace(
        '<div class="stat-number">7</div>',
        '<div class="stat-number">8</div>',
    )
    if 'data-i18n="home.cs3title"' not in html:
        html = html.replace(
            '      <div class="insights-grid insights-grid--2">',
            '      <div class="insights-grid insights-grid--3">',
        )
        html = html.replace(
            '          <a href="case-studies.html#digital-invest" class="text-link" data-i18n="home.caseStudiesLink">View All Case Studies →</a>\n        </article>\n      </div>',
            '          <a href="case-studies.html#digital-invest" class="text-link">Read Case Study →</a>\n        </article>\n'
            + INDEX_CS3
            + '      </div>\n      <p class="text-center" style="margin-top:2rem"><a href="case-studies.html" class="text-link" data-i18n="home.caseStudiesLink">View All Case Studies →</a></p>',
        )
    return html


def patch_footers(html: str) -> str:
    if "agron1.com" in html and 'footer.ventures' in html:
        return html
    return html.replace(
        '          <h4 data-i18n="footer.ventures">Ventures</h4>\n          <ul>\n            <li><a href="ventures.html">Digital Invest Inc.</a></li>',
        '          <h4 data-i18n="footer.ventures">Ventures</h4>\n          <ul>\n'
        + FOOTER_AGRON
        + '            <li><a href="ventures.html">Digital Invest Inc.</a></li>',
    )


def patch_page_content() -> None:
    path = ROOT / "js" / "page-content.js"
    text = path.read_text(encoding="utf-8")
    raw = text.split("const PAGE_CONTENT = ", 1)[1].rsplit(";", 1)[0]
    data = json.loads(raw)

    for lang, block in data.items():
        overrides = LANG_OVERRIDES.get(lang, {})
        v = overrides.get("ventures", PAGE_CONTENT_V0)
        c = overrides.get("career", PAGE_CONTENT_T0)
        a = overrides.get("about", PAGE_CONTENT_ABOUT)

        ventures = block.setdefault("ventures", {})
        new_v = {}
        new_v.update(v)
        new_v.update({k: ventures[k] for k in ventures if k.startswith("v") and k != "v0year" and not k.startswith("v0")})
        # preserve v1..v8, prepend v0*
        ordered_v = {k: v[k] for k in sorted(v.keys())}
        for k in sorted(ventures.keys()):
            if k not in ordered_v:
                ordered_v[k] = ventures[k]
        block["ventures"] = ordered_v

        career = block.setdefault("career", {})
        ordered_c = {k: c[k] for k in sorted(c.keys())}
        for k in sorted(career.keys()):
            if k not in ordered_c:
                ordered_c[k] = career[k]
        block["career"] = ordered_c

        about = block.setdefault("about", {})
        about.update(a)

    out = "const PAGE_CONTENT = " + json.dumps(data, ensure_ascii=False, indent=2) + ";\n"
    path.write_text(out, encoding="utf-8")
    print("updated page-content.js")


def patch_translations() -> None:
    path = ROOT / "js" / "translations.js"
    text = path.read_text(encoding="utf-8")

    en_about_lead2 = (
        "From founding one of the world's largest Data Storage companies — acquired at a peak market value of "
        "$19.5 billion — to leading Digital Invest Inc. in precision medicine and founding AGRON Inc. in 2026 to build "
        "the Aerial-Ground Robotics Operations Network, his career spans executive acumen, strategic technology, and "
        "transformative leadership across digital health, data infrastructure, and robotics."
    )

    replacements = [
        (
            r'"aboutLead2": "[^"]*Aero-Ground Robotics Operations Network[^"]*"',
            f'"aboutLead2": {json.dumps(en_about_lead2, ensure_ascii=False)}',
        ),
        (
            '"roleVal": "CEO & Board Member · Digital Invest Inc."',
            '"roleVal": "CEO · Digital Invest Inc. · Founder · AGRON Inc."',
        ),
        (
            '"companyVal": "Digital Invest Inc.\\nCEO & Board Member"',
            '"companyVal": "Digital Invest Inc. & AGRON Inc.\\nFounder & CEO"',
        ),
        (
            "From precision medicine to global telecommunications — a track record of founding, scaling, and leading companies to market-defining success.",
            "From precision medicine and robotics to global telecommunications — a track record of founding, scaling, and leading companies to market-defining success.",
        ),
        (
            "Achieved consistent financial growth, positioning the company among Top 10 Precision Medicine Companies in the U.S. (2023). Digital Invest comprises diverse innovative projects, including Human Digital Model, BioMath Life, and Aero-Ground Robotics Operations Network.",
            "Achieved consistent financial growth, positioning the company among Top 10 Precision Medicine Companies in the U.S. (2023), with projects including Human Digital Model and BioMath Life.",
        ),
        (
            "Case studies from Michael Kofman's career — 9 Net Avenue Inc. and Digital Invest Inc.",
            "Case studies from Michael Kofman's career — AGRON Inc., 9 Net Avenue Inc., and Digital Invest Inc.",
        ),
        (
            "Selected outcomes from founding and leading companies across data infrastructure and digital health.",
            "Selected outcomes from founding and leading companies across robotics, data infrastructure, and digital health.",
        ),
        (
            "Companies founded and led by Michael Kofman — from Digital Invest Inc. to 9 Net Avenue Inc. — building transformative businesses across technology and healthcare.",
            "Companies founded and led by Michael Kofman — from AGRON Inc. to 9 Net Avenue Inc. — building transformative businesses across robotics, technology, and healthcare.",
        ),
    ]

    for old, new in replacements:
        if old.startswith('"') or old.startswith('From ') or old.startswith('Achieved') or old.startswith('Case ') or old.startswith('Selected') or old.startswith('Companies'):
            text = text.replace(old, new)
        else:
            text = re.sub(old, new, text, count=1)

    # Insert caseStudies cs3 and home cs3 after cs2 block (English only marker)
    cs3_block = """
      "cs3eyebrow": "Robotics & UAV · 2026 — Present",
      "cs3title": "AGRON Inc.",
      "cs3challenge": "Challenge",
      "cs3challengeText": "Organizations building UAV and Counter-UAS capability need independent assessment, structured training, and operational architecture — not isolated platforms or ad-hoc piloting.",
      "cs3action": "Approach",
      "cs3actionText": "Founded AGRON Inc. in 2026 to lead the AGRON Ecosystem — consulting, assessment and validation, capability development, training infrastructure, product development support, geospatial systems through ISDRI, and AGRON Maritime Intelligence + Security for yachts, marinas, and private maritime infrastructure.",
      "cs3result": "Outcome",
      "cs3resultText": "A connected professional services ecosystem spanning five service domains and multiple companies — Global Drone Academy, AGRON, ISDRI, and GUARD — with programmes delivered across 10+ countries and 10,000+ UAV operators, instructors, and specialists trained.\""""
    if '"cs3title"' not in text:
        text = text.replace(
            '"cs2resultText": "Achieved consistent financial growth, positioning the company among Top 10 Precision Medicine Companies in the U.S. (2023), with projects including Human Digital Model and BioMath Life."\n    }',
            '"cs2resultText": "Achieved consistent financial growth, positioning the company among Top 10 Precision Medicine Companies in the U.S. (2023), with projects including Human Digital Model and BioMath Life.",'
            + cs3_block
            + "\n    }",
            1,
        )

    home_cs3 = """
      "cs3title": "AGRON Inc.",
      "cs3desc": "Founded in 2026 — the AGRON Ecosystem for UAV capability development, geospatial systems, and maritime intelligence.\""""
    if '"cs3title"' not in text.split('"home":')[1].split('"about":')[0]:
        text = text.replace(
            '"cs2desc": "Founded and scaled from inception through IPO — Top 10 U.S. Precision Medicine Company, 2023.",',
            '"cs2desc": "Founded and scaled from inception through IPO — Top 10 U.S. Precision Medicine Company, 2023.",\n'
            + home_cs3.strip().replace('"cs3title"', '"cs3title"'),
            1,
        )

    # RU/UK aboutLead2
    ru_lead = (
        "От основания одной из крупнейших в мире компаний Data Storage — с пиковой капитализацией $19,5 млрд — "
        "до руководства Digital Invest Inc. в precision medicine и основания AGRON Inc. в 2026 году для построения "
        "Aerial-Ground Robotics Operations Network. Карьера охватывает цифровое здравоохранение, инфраструктуру данных и робототехнику."
    )
    uk_lead = (
        "Від заснування однієї з найбільших у світі компаній Data Storage — з піковою капіталізацією $19,5 млрд — "
        "до керівництва Digital Invest Inc. у precision medicine та заснування AGRON Inc. у 2026 році для побудови "
        "Aerial-Ground Robotics Operations Network. Кар'єра охоплює цифрове здоров'я, інфраструктуру даних і робототехніку."
    )
    text = re.sub(
        r'("ru": \{[\s\S]*?"aboutLead2": )"[^"]*"',
        rf'\1{json.dumps(ru_lead, ensure_ascii=False)}',
        text,
        count=1,
    )
    text = re.sub(
        r'("uk": \{[\s\S]*?"aboutLead2": )"[^"]*"',
        rf'\1{json.dumps(uk_lead, ensure_ascii=False)}',
        text,
        count=1,
    )

    path.write_text(text, encoding="utf-8")
    print("updated translations.js")


def main() -> None:
    patch_page_content()
    patch_translations()

    for html_path in ROOT.glob("*.html"):
        html = html_path.read_text(encoding="utf-8")
        orig = html
        html = patch_footers(html)
        if html_path.name == "ventures.html":
            html = patch_ventures_html(html)
        elif html_path.name == "career.html":
            html = patch_career_html(html)
        elif html_path.name == "about.html":
            html = patch_about_html(html)
        elif html_path.name == "case-studies.html":
            html = patch_case_studies_html(html)
        elif html_path.name == "index.html":
            html = patch_index_html(html)
        if html != orig:
            html_path.write_text(html, encoding="utf-8")
            print(f"patched {html_path.name}")

    print("AGRON patch complete — run build_site.py next")


if __name__ == "__main__":
    main()
