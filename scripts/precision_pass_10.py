#!/usr/bin/env python3
"""Final 10/10 precision pass — factual cleanup, i18n, shared chrome."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LANGS = ["en", "es", "de", "fr", "ru", "uk", "zh", "ar", "he"]

HOME_FOOTER = """    <footer class="site-footer site-footer--home">
    <div class="container">
      <div class="footer-grid footer-grid--home">
        <div class="footer-brand">
          <div class="logo-name">Michael Kofman</div>
          <p data-i18n="home.footerHomeDesc">Technology executive, founder, and board advisor.</p>
        </div>
        <div class="footer-col">
          <h4 data-i18n="footer.navigation">Navigation</h4>
          <ul>
            <li><a href="about.html" data-i18n="nav.about">About</a></li>
            <li><a href="career.html" data-i18n="nav.career">The Record</a></li>
            <li><a href="ventures.html" data-i18n="nav.ventures">Ventures</a></li>
            <li><a href="insights.html" data-i18n="nav.insights">Insights</a></li>
            <li><a href="contact.html" data-i18n="nav.contact">Contact</a></li>
          </ul>
        </div>
        <div class="footer-col">
          <h4 data-i18n="footer.connect">Connect</h4>
          <ul>
            <li><a href="mailto:mkofman@mkofman.com">mkofman@mkofman.com</a></li>
            <li><a href="https://www.linkedin.com/in/michael-kofman-0509176/" target="_blank" rel="noopener">LinkedIn</a></li>
          </ul>
        </div>
      </div>
      <div class="footer-bottom">
        <a href="privacy.html" class="footer-privacy" data-i18n="footer.privacy">Privacy Policy</a>
        <span data-i18n="footer.copyright">&copy; 2026 Michael Kofman. All Rights Reserved.</span>
        <div class="footer-social">
          <a href="https://www.linkedin.com/in/michael-kofman-0509176/" target="_blank" rel="noopener" aria-label="LinkedIn">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor"><path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433a2.062 2.062 0 01-2.063-2.065 2.064 2.064 0 112.063 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z"/></svg>
          </a>
        </div>
      </div>
    </div>
  </footer>"""

INTERNAL_NAV = """                        <header class="site-header">
    <div class="container header-inner">
      <a href="index.html" class="logo">
        <span class="logo-name">Michael Kofman</span>
      </a>
      <div class="header-right">
        <nav class="main-nav" aria-label="Primary">
        <a href="index.html" data-i18n="nav.home">Home</a>
        <a href="about.html" data-i18n="nav.about">About</a>
        <a href="board.html" data-i18n="nav.board">Board & Advisory</a>
        <a href="insights.html" data-i18n="nav.insights">Insights</a>
        <a href="ventures.html" data-i18n="nav.ventures">Ventures</a>
        <a href="career.html" data-i18n="nav.career">The Record</a>
        <a href="recognition.html" data-i18n="nav.recognition">Recognition</a>
        <a href="contact.html" data-i18n="nav.contact">Contact</a>
        </nav>
          <div class="header-controls">
            <button class="theme-toggle" type="button" data-i18n-aria="ui.toggleTheme" aria-label="Toggle theme">
              <svg class="icon-sun" width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="5"/><path d="M12 1v2M12 21v2M4.22 4.22l1.42 1.42M18.36 18.36l1.42 1.42M1 12h2M21 12h2M4.22 19.78l1.42-1.42M18.36 5.64l1.42-1.42"/></svg>
              <svg class="icon-moon" width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 12.79A9 9 0 1111.21 3 7 7 0 0021 12.79z"/></svg>
            </button>
            <div class="lang-switcher">
              <button class="lang-trigger" type="button" data-i18n-aria="ui.selectLanguage" aria-label="Select language">
                <span class="lang-flag">🇺🇸</span>
                <svg width="9" height="9" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M6 9l6 6 6-6"/></svg>
              </button>
              <ul class="lang-panel" role="listbox"></ul>
            </div>
          </div>
          <button class="nav-toggle" type="button" data-i18n-aria="ui.toggleNav" aria-label="Toggle navigation">
            <span></span><span></span><span></span>
          </button>
      </div>
    </div>
    <nav class="main-nav main-nav-mobile" aria-label="Mobile">
      <a href="index.html" data-i18n="nav.home">Home</a>
      <a href="about.html" data-i18n="nav.about">About</a>
      <a href="ventures.html" data-i18n="nav.ventures">Ventures</a>
      <a href="career.html" data-i18n="nav.career">The Record</a>
      <a href="recognition.html" data-i18n="nav.recognition">Recognition</a>
      <a href="insights.html" data-i18n="nav.insights">Insights</a>
      <a href="board.html" data-i18n="nav.board">Board & Advisory</a>
      <a href="contact.html" data-i18n="nav.contact">Contact</a>
    </nav>
  </header>"""

T1DESC = {
    "en": "Founded Digital Invest Inc. in 2021. Leads bio-mathematical medicine, genomic intelligence, and clinical data platforms. Featured in Healthcare Tech Outlook (2023).",
    "es": "Fundó Digital Invest Inc. en 2021. Dirige medicina biomatemática, inteligencia genómica y plataformas de datos clínicos. Healthcare Tech Outlook (2023).",
    "de": "Digital Invest Inc. 2021 gegründet. Biomathematische Medizin, Genom-Intelligenz und klinische Datenplattformen. Healthcare Tech Outlook (2023).",
    "fr": "Digital Invest Inc., fondée en 2021. Médecine biomathématique, intelligence génomique et plateformes de données cliniques. Healthcare Tech Outlook (2023).",
    "ru": "Digital Invest Inc. основана в 2021. Биоматематическая медицина, геномная аналитика и клинические платформы. Healthcare Tech Outlook (2023).",
    "uk": "Digital Invest Inc. заснована у 2021. Біоматематична медицина, геномна аналітика та клінічні платформи. Healthcare Tech Outlook (2023).",
    "zh": "Digital Invest Inc. 创立于 2021 年，专注生物数学医学、基因组智能和临床数据平台。Healthcare Tech Outlook（2023）。",
    "ar": "Digital Invest Inc.، تأسست 2021. طب biomathematical وبيانات genomics ومنصات clínico. Healthcare Tech Outlook (2023).",
    "he": "Digital Invest Inc. הוקמה ב-2021. רפואה ביו-מתמטית, אינטליגנציה גנומית ופלטפורמות נתונים קlinיים. Healthcare Tech Outlook (2023).",
}

V2HIGHLIGHT = {
    "en": "Harvard Medical School & Stanford Biomath — genetic reporting collaboration",
    "es": "Harvard Medical School y Stanford Biomath — colaboración en informes genéticos",
    "de": "Harvard Medical School & Stanford Biomath — Zusammenarbeit zu genetischen Berichten",
    "fr": "Harvard Medical School et Stanford Biomath — collaboration sur les rapports génétiques",
    "ru": "Harvard Medical School и Stanford Biomath — сотрудничество по генетическим отчётам",
    "uk": "Harvard Medical School і Stanford Biomath — співпраця з генетичними звітами",
    "zh": "Harvard Medical School 与 Stanford Biomath — 遗传报告合作",
    "ar": "Harvard Medical School و Stanford Biomath — تعاون في التقارير الجينية",
    "he": "Harvard Medical School ו-Stanford Biomath — שיתוף פעולה בדיווח genético",
}

CAREER_LEAD = {
    "en": "Technology, companies, and operating experience across successive periods of technological change.",
    "es": "Tecnología, empresas y experiencia operativa a través de periodos sucesivos de cambio tecnológico.",
    "de": "Technologie, Unternehmen und operative Erfahrung über aufeinanderfolgende Technologieperioden.",
    "fr": "Technologie, entreprises et expérience opérationnelle à travers des périodes de changement technologique.",
    "ru": "Технологии, компании и операционный опыт в последовательные периоды технологических изменений.",
    "uk": "Технології, компанії та операційний досвід у послідовні періоди технологічних змін.",
    "zh": "技术、公司与 successive 技术变革时期的运营经验。",
    "ar": "التكنولوجيا والشركات والخبرة التشغيلية عبر فترات متتالية من التغير التكنولوجي.",
    "he": "טכנולוגיה, חברות וניסיון תפעולי לאורך תקופות של שינוי טכנולוגי.",
}

ARCHIVE_TITLE = {
    "en": "From the Archive",
    "es": "Del archivo",
    "de": "Aus dem Archiv",
    "fr": "De l'archive",
    "ru": "Из архива",
    "uk": "З архіву",
    "zh": "来自档案",
    "ar": "من الأرشيف",
    "he": "מהארכיון",
}

CS2_ACTION = {
    "en": "Founded Digital Invest Inc. in 2021. Leads bio-mathematical medicine, genomic intelligence, and clinical data platforms.",
    "es": "Fundé Digital Invest Inc. en 2021. Dirijo medicina biomatemática, inteligencia genómica y plataformas de datos clínicos.",
    "de": "Digital Invest Inc. 2021 gegründet. Schwerpunkt: biomathematische Medizin, Genom-Intelligenz und klinische Datenplattformen.",
    "fr": "Digital Invest Inc. fondée en 2021. Médecine biomathématique, intelligence génomique et plateformes de données cliniques.",
    "ru": "Основана Digital Invest Inc. в 2021. Биоматематическая медицина, геномная аналитика и клинические платформы данных.",
    "uk": "Засновано Digital Invest Inc. у 2021. Біоматематична медицина, геномна аналітика та клінічні платформи даних.",
    "zh": "2021 年创立 Digital Invest Inc.，领导生物数学医学、基因组智能和临床数据平台。",
    "ar": "تأسست Digital Invest Inc. عام 2021. الطب biomathematical والذكاء genomics ومنصات البيانات clínico.",
    "he": "Digital Invest Inc. הוקמה ב-2021. רפואה ביו-מתמטית, אינטליגנציה גנומית ופלטפורמות נתונים clínico.",
}

CS2_RESULT = {
    "en": "Healthcare Tech Outlook feature (2023). Projects include Human Digital Model and BioMath Life.",
    "es": "Healthcare Tech Outlook (2023). Proyectos: Human Digital Model y BioMath Life.",
    "de": "Healthcare Tech Outlook (2023). Projekte: Human Digital Model und BioMath Life.",
    "fr": "Healthcare Tech Outlook (2023). Projets : Human Digital Model et BioMath Life.",
    "ru": "Healthcare Tech Outlook (2023). Проекты: Human Digital Model и BioMath Life.",
    "uk": "Healthcare Tech Outlook (2023). Проєкти: Human Digital Model і BioMath Life.",
    "zh": "Healthcare Tech Outlook（2023）。项目包括 Human Digital Model 和 BioMath Life。",
    "ar": "Healthcare Tech Outlook (2023). مشاريع: Human Digital Model و BioMath Life.",
    "he": "Healthcare Tech Outlook (2023). פרויקטים: Human Digital Model ו-BioMath Life.",
}

ARTICLE2P3 = {
    "en": "With Digital Invest Inc., founded in 2021, we work in bio-mathematical medicine — applying science, DNA technologies, AI, and ML to clinical intelligence. Healthcare Tech Outlook featured the company in 2023.",
    "es": "Con Digital Invest Inc., fundada en 2021, trabajamos en medicina biomatemática — ciencia, tecnologías de ADN, IA y ML aplicadas a inteligencia clínica. Healthcare Tech Outlook (2023).",
    "de": "Mit Digital Invest Inc., gegründet 2021, arbeiten wir in biomathematischer Medizin — Wissenschaft, DNA-Technologien, KI und ML in klinischer Intelligenz. Healthcare Tech Outlook (2023).",
    "fr": "Avec Digital Invest Inc., fondée en 2021, nous travaillons en médecine biomathématique — science, technologies ADN, IA et ML appliquées à l'intelligence clinique. Healthcare Tech Outlook (2023).",
    "ru": "С Digital Invest Inc., основанной в 2021, работаем в биоматематической медицине — наука, ДНК-технологии, ИИ и ML в клинической аналитике. Healthcare Tech Outlook (2023).",
    "uk": "З Digital Invest Inc., заснованою у 2021, працюємо в біоматематичній медицині — наука, ДНК-технології, ШІ та ML у кlinічній аналітиці. Healthcare Tech Outlook (2023).",
    "zh": "Digital Invest Inc. 创立于 2021 年，从事生物数学医学 — 将科学、DNA 技术、AI 和 ML 应用于临床智能。Healthcare Tech Outlook（2023）。",
    "ar": "مع Digital Invest Inc.، تأسست 2021، نعمل في الطب biomathematical — علم وتقنيات DNA وAI وML في الذكاء clínico. Healthcare Tech Outlook (2023).",
    "he": "עם Digital Invest Inc., שהוקמה ב-2021, עובדים ברפואה ביו-מתמטית — מדע, טכנולוגיות DNA, AI ו-ML באינטליגנציה clínico. Healthcare Tech Outlook (2023).",
}

EXP1DESC = {
    "en": "Founded and led multiple technology companies in the United States and Europe.",
    "es": "Fundó y dirigió múltiples empresas tecnológicas en Estados Unidos y Europa.",
    "de": "Gründete und führte mehrere Technologieunternehmen in den USA und Europa.",
    "fr": "A fondé et dirigé plusieurs entreprises technologiques aux États-Unis et en Europe.",
    "ru": "Основал и руководил несколькими технологическими компаниями в США и Европе.",
    "uk": "Заснував і керував кількома технологічними компаніями в США та Європі.",
    "zh": "在美国和欧洲创办并领导多家科技公司。",
    "ar": "أسس وقاد عدة شركات تقنية في الولايات المتحدة وأوروبا.",
    "he": "ייסד והנהיג מספר חברות טכנולוגיה בארצות הברית ובאירופה.",
}

CASESTUDIES_LEAD = {
    "en": "Founding, scaling, and leading companies from early stage through acquisition.",
    "es": "Fundación, escalamiento y liderazgo de empresas desde etapas tempranas hasta adquisición.",
    "de": "Gründung, Skalierung und Führung von Unternehmen von der Frühphase bis zur Übernahme.",
    "fr": "Création, développement et direction d'entreprises de leur lancement jusqu'à l'acquisition.",
    "ru": "Основание, масштабирование и руководство компаниями — от ранней стадии до сделок M&A.",
    "uk": "Заснування, масштабування та керівництво компаніями — від ранньої стадії до угод M&A.",
    "zh": "从早期阶段到被收购，持续创办、扩张并领导企业。",
    "ar": "تأسيس وتوسيع وقيادة شركات من المراحل المبكرة حتى الاستحواذ.",
    "he": "הקמה, הרחבה והובלת חברות משלב מוקדם ועד רכישה.",
}

TOPICS_LEAD = {
    "en": "Topics draw on documented operating experience across technology, health, and infrastructure.",
    "es": "Los temas se basan en experiencia operativa documentada en tecnología, salud e infraestructura.",
    "de": "Themen basieren auf dokumentierter operativer Erfahrung in Technologie, Gesundheit und Infrastruktur.",
    "fr": "Les thèmes s'appuient sur une expérience opérationnelle documentée en technologie, santé et infrastructure.",
    "ru": "Темы основаны на задокументированном операционном опыте в технологиях, здравоохранении и инфраструктуре.",
    "uk": "Теми базуються на задокументованому операційному досвіді в технологіях, охороні здоров'я та інфраструктурі.",
    "zh": "主题基于在科技、医疗和基础设施领域的 documented 运营经验。",
    "ar": "تعتمد الموضوعات على خبرة تشغيلية موثقة في التكنولوجيا والصحة والبنية التحتية.",
    "he": "הנושאים מבוססים על ניסיון תפעולי מתועד בטכנולוגיה, בריאות ותשתיות.",
}

INSIGHTS_META = {
    "en": "Original writing and executive briefs from Michael Kofman.",
    "es": "Escritos originales y briefs ejecutivos de Michael Kofman.",
    "de": "Originelle Texte und Executive Briefs von Michael Kofman.",
    "fr": "Écrits originaux et briefs exécutifs de Michael Kofman.",
    "ru": "Оригинальные тексты и executive briefs Michael Kofman.",
    "uk": "Оригінальні тексти та executive briefs Michael Kofman.",
    "zh": "Michael Kofman 的原创文章与 executive briefs。",
    "ar": "كتابات أصلية وbriefs تنفيذية من Michael Kofman.",
    "he": "כתיבה מקורית ו-executive briefs מאת Michael Kofman.",
}

DI_IPO_RE = re.compile(
    r"Digital Invest[^\"]{0,200}(?:IPO|public offering|Börsengang|salida a bolsa|"
    r"introduction en bourse|публичн|طرح عام|成功 IPO|IPO מוצלח|успешн|успішн)",
    re.IGNORECASE,
)


def load_json_js(path: Path) -> dict:
    raw = path.read_text(encoding="utf-8")
    return json.loads(raw[raw.find("{") : raw.rfind("}") + 1])


def write_json_js(path: Path, var_name: str, data: dict) -> None:
    path.write_text(
        f"const {var_name} = " + json.dumps(data, ensure_ascii=False, indent=2) + ";\n",
        encoding="utf-8",
    )


def strip_di_ipo(text: str) -> str:
    if DI_IPO_RE.search(text):
        return ""
    return text


def patch_page_content() -> None:
    path = ROOT / "js" / "page-content.js"
    pc = load_json_js(path)
    for lang in LANGS:
        if lang not in pc:
            continue
        career = pc[lang].setdefault("career", {})
        for key in list(career.keys()):
            if re.match(r"s[1-4](?:title|desc)", key):
                del career[key]
        if lang in T1DESC:
            career["t1desc"] = T1DESC[lang]
        ventures = pc[lang].setdefault("ventures", {})
        if lang in V2HIGHLIGHT:
            ventures["v2highlight"] = V2HIGHLIGHT[lang]
        for key, val in list(ventures.items()):
            if isinstance(val, str):
                cleaned = strip_di_ipo(val)
                if cleaned == "" and "Digital Invest" in val:
                    ventures[key] = T1DESC.get(lang, T1DESC["en"])
                elif cleaned != val:
                    ventures[key] = cleaned
        for section in pc[lang].values():
            if not isinstance(section, dict):
                continue
            for key, val in list(section.items()):
                if isinstance(val, str) and strip_di_ipo(val) == "" and "Digital Invest" in val:
                    if key == "t1desc":
                        section[key] = T1DESC.get(lang, T1DESC["en"])
                    elif key.endswith("desc") or key.endswith("p1") or key.endswith("p3"):
                        section[key] = T1DESC.get(lang, T1DESC["en"])
    write_json_js(path, "PAGE_CONTENT", pc)
    print("patched page-content.js")


def patch_translations() -> None:
    path = ROOT / "js" / "translations.js"
    data = load_json_js(path)
    for lang in LANGS:
        if lang not in data:
            continue
        data[lang].setdefault("career", {})["lead"] = CAREER_LEAD.get(lang, CAREER_LEAD["en"])
        data[lang].setdefault("about", {})["archiveTitle"] = ARCHIVE_TITLE.get(lang, ARCHIVE_TITLE["en"])
        data[lang].setdefault("insights", {})["topicsLead"] = TOPICS_LEAD.get(lang, TOPICS_LEAD["en"])
        meta = data[lang].setdefault("meta", {})
        if "insights" in meta:
            meta["insights"]["description"] = INSIGHTS_META.get(lang, INSIGHTS_META["en"])
        cs = data[lang].setdefault("caseStudies", {})
        cs["caseStudiesLead"] = CASESTUDIES_LEAD.get(lang, CASESTUDIES_LEAD["en"])
        if lang in CS2_ACTION:
            cs["cs2actionText"] = CS2_ACTION[lang]
            cs["cs2resultText"] = CS2_RESULT[lang]
        home = data[lang].setdefault("home", {})
        if lang in EXP1DESC:
            home["exp1desc"] = EXP1DESC[lang]
        articles = data[lang].setdefault("articles", {})
        if lang in ARTICLE2P3:
            articles["article2p3"] = ARTICLE2P3[lang]
        ventures_meta = meta.get("ventures", {})
        if isinstance(ventures_meta, dict) and "description" in ventures_meta:
            desc = ventures_meta["description"]
            if "transformative" in desc.lower():
                ventures_meta["description"] = desc.replace("transformative Geschäfte", "Unternehmen").replace("transformative businesses", "companies")
        # Remove stale career skill keys
        career = data[lang].get("career", {})
        for key in list(career.keys()):
            if re.match(r"s[1-4](?:title|desc)", key):
                del career[key]
        # Scrub any remaining DI+IPO strings
        def scrub_obj(obj):
            if isinstance(obj, dict):
                for k, v in obj.items():
                    if isinstance(v, str) and strip_di_ipo(v) == "" and "Digital Invest" in v:
                        if k == "t1desc":
                            obj[k] = T1DESC.get(lang, T1DESC["en"])
                        elif k in ("cs2actionText", "article2p3", "v1p1"):
                            obj[k] = CS2_ACTION.get(lang, ARTICLE2P3.get(lang, T1DESC["en"]))
                        elif k == "exp1desc":
                            obj[k] = EXP1DESC.get(lang, EXP1DESC["en"])
                    elif isinstance(v, (dict, list)):
                        scrub_obj(v)
            elif isinstance(obj, list):
                for item in obj:
                    scrub_obj(item)
        scrub_obj(data[lang])
        if lang in V2HIGHLIGHT:
            data[lang].setdefault("ventures", {})["v2highlight"] = V2HIGHLIGHT[lang]
        # Sync deck/home duplicate keys
        home = data[lang].setdefault("home", {})
        home["caseStudiesLead"] = CASESTUDIES_LEAD.get(lang, CASESTUDIES_LEAD["en"])
        if lang in EXP1DESC:
            home["exp1desc"] = EXP1DESC[lang]
    write_json_js(path, "TRANSLATIONS", data)
    print("patched translations.js")


def patch_html_files() -> None:
    footer_re = re.compile(r'<footer class="site-footer[^"]*">.*?</footer>', re.DOTALL)
    header_re = re.compile(
        r'<header class="site-header(?: site-header--split)?">.*?</header>',
        re.DOTALL,
    )
    for html in ROOT.glob("*.html"):
        text = html.read_text(encoding="utf-8")
        if html.name != "index.html":
            text, _ = footer_re.subn(HOME_FOOTER, text, count=1)
            text, _ = header_re.subn(INTERNAL_NAV, text, count=1)
        text = text.replace(
            "Harvard Medical School & Stanford Biomath Partner",
            V2HIGHLIGHT["en"],
        )
        text = text.replace(
            "Board advisory, strategic technology leadership, and building the next generation of digital health and infrastructure companies.",
            "Digital Invest Inc., AGRON Inc., and board advisory work.",
        )
        text = text.replace("Selected Photographs", "From the Archive")
        text = text.replace("Moments Across the Journey", "From the Archive")
        if html.name == "insights.html":
            text = re.sub(
                r'<meta name="description" content="[^"]*">',
                '<meta name="description" content="Original writing and executive briefs from Michael Kofman.">',
                text,
                count=1,
            )
            text = re.sub(
                r'<meta property="og:description" content="[^"]*">',
                '<meta property="og:description" content="Original writing and executive briefs from Michael Kofman.">',
                text,
                count=1,
            )
            text = re.sub(
                r'<meta name="twitter:description" content="[^"]*">',
                '<meta name="twitter:description" content="Original writing and executive briefs from Michael Kofman.">',
                text,
                count=1,
            )
        html.write_text(text, encoding="utf-8")
        print(f"html {html.name}")


def patch_app_js() -> None:
    for rel in ("js/app.js", "js/features.js"):
        path = ROOT / rel
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8")
        text = text.replace("initCalendly();", "// initCalendly disabled")
        path.write_text(text, encoding="utf-8")
        print(f"patched {rel}")


def patch_locale_patches() -> None:
    path = ROOT / "scripts" / "locale_patches.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    bg_fix = {
        "en": "Doctor of Technical Sciences and Ph.D. in Information Technology. Author of technical papers on satellite and optical systems; patent in digital satellite HDTV subsequently acquired by Sony.",
        "es": "Doctor en Ciencias Técnicas y Ph.D. en Tecnologías de la Información. Autor de trabajos técnicos; patente HDTV satelital adquirida por Sony.",
        "de": "Doctor of Technical Sciences und Ph.D. in Information Technology. Autor technischer Arbeiten; Patent digitales Satelliten-HDTV, übernommen von Sony.",
        "fr": "Doctor of Technical Sciences et Ph.D. in Information Technology. Auteur de travaux techniques; brevet HDTV satellitaire acquis par Sony.",
        "ru": "Доктор технических наук и Ph.D. в IT. Автор технических работ; патент digital satellite HDTV, приобретённый Sony.",
        "uk": "Доктор технічних наук і Ph.D. в IT. Автор технічних робіт; патент digital satellite HDTV, придбаний Sony.",
        "zh": "技术科学博士和信息技术博士。技术论文作者；数字卫星 HDTV 专利被 Sony 收购。",
        "ar": "Doctor of Technical Sciences و Ph.D. in Information Technology. مؤلف أوراق تقنية؛ براءة HDTV فضائية acquired by Sony.",
        "he": "Doctor of Technical Sciences ו-Ph.D. in Information Technology. מחבר מאמרים טכניים; פטנט HDTV לווייני נרכש על ידי Sony.",
    }
    for lang in LANGS:
        patch = data.setdefault(lang, {})
        if lang in V2HIGHLIGHT:
            patch.setdefault("ventures", {})["v2highlight"] = V2HIGHLIGHT[lang]
        if lang in T1DESC:
            patch.setdefault("career", {})["t1desc"] = T1DESC[lang]
        if lang in bg_fix:
            patch.setdefault("about", {})["secBackgroundP1"] = bg_fix[lang]
        patch.setdefault("career", {})["lead"] = CAREER_LEAD.get(lang, CAREER_LEAD["en"])
        patch.setdefault("about", {})["archiveTitle"] = ARCHIVE_TITLE.get(lang, ARCHIVE_TITLE["en"])
        patch.setdefault("board", {})["title"] = "Board & Advisory"
        patch.setdefault("board", {})["lead"] = (
            "Selected board and strategic advisory engagements."
            if lang == "en"
            else patch.get("board", {}).get("lead", "Board & Advisory")
        )
        patch.setdefault("caseStudies", {})["cs2actionText"] = CS2_ACTION.get(lang, CS2_ACTION["en"])
        patch.setdefault("articles", {})["article2p3"] = ARTICLE2P3.get(lang, ARTICLE2P3["en"])
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print("patched locale_patches.json")


def main() -> None:
    patch_page_content()
    patch_translations()
    patch_html_files()
    patch_app_js()
    patch_locale_patches()
    print("precision pass 10 complete")


if __name__ == "__main__":
    main()
