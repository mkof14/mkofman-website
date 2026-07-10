#!/usr/bin/env python3
"""Add new translations and patch HTML pages for site upgrade."""
import json
import os
import re

ROOT = os.path.join(os.path.dirname(__file__), "..")

NEW_TRANSLATIONS = {
    "en": {
        "ui": {"sending": "Sending…", "formError": "Could not send. Please email directly."},
        "nav": {
            "speaking": "Speaking",
            "caseStudies": "Case Studies",
            "mediaKit": "Media Kit",
            "groupMain": "Main",
            "groupServices": "Services",
            "groupWork": "Work",
        },
        "cta": {
            "eyebrow": "Work Together",
            "title": "Request Advisory or a Speaking Engagement",
            "lead": "For advisory roles, board positions, speaking engagements, and strategic partnerships.",
            "button": "Get in Touch",
        },
        "home": {
            "heroSub": "CEO, board advisor, and strategic technologist for public and private companies in technology, data storage, and digital health.",
            "primaryCta": "Request Advisory",
            "secondaryCta": "View Case Studies",
            "featuredEyebrow": "As Featured In",
            "caseStudiesEyebrow": "Proven Outcomes",
            "caseStudiesTitle": "Case Studies",
            "caseStudiesLead": "Founding, scaling, and leading companies from inception through acquisition and IPO.",
            "caseStudiesLink": "View All Case Studies →",
            "cs1title": "9 Net Avenue Inc.",
            "cs1desc": "Built one of the world's largest Data Storage companies — acquired at a peak market value of $19.5 billion.",
            "cs2title": "Digital Invest Inc.",
            "cs2desc": "Founded and scaled from inception through IPO — Top 10 U.S. Precision Medicine Company, 2023.",
        },
        "meta": {
            "speaking": {"title": "Speaking — Michael Kofman", "description": "Invite Michael Kofman to speak on executive leadership, technology strategy, digital health, and board governance."},
            "caseStudies": {"title": "Case Studies — Michael Kofman", "description": "Case studies from Michael Kofman's career — 9 Net Avenue Inc. and Digital Invest Inc."},
            "mediaKit": {"title": "Media Kit — Michael Kofman", "description": "Official biographies, photos, and contact information for press and event organizers."},
            "article1": {"title": "From Engineering to Global Infrastructure — Michael Kofman", "description": "Michael Kofman on a career path from satellite engineering to founding global data infrastructure companies."},
            "article2": {"title": "Precision Medicine and Technology — Michael Kofman", "description": "Michael Kofman on combining life sciences with AI, ML, and DNA technologies in modern medicine."},
        },
        "speaking": {
            "eyebrow": "Speaking Engagements",
            "title": "Invite Michael Kofman to Speak",
            "lead": "Available for speaking engagements on executive leadership, technology strategy, digital health, data infrastructure, and corporate governance.",
            "topicsEyebrow": "Speaking Topics",
            "topicsTitle": "Areas of Expertise",
            "topicsLead": "Topics draw on decades of experience founding and leading companies in the United States and Europe.",
            "processEyebrow": "How to Invite",
            "processTitle": "Booking Process",
            "process1title": "Send an Inquiry",
            "process1desc": "Use the contact form or email mkofman@mkofman.com with event details, audience, and preferred topics.",
            "process2title": "Confirm Scope",
            "process2desc": "Discuss format — keynote, panel, board session, or executive roundtable — and logistics.",
            "process3title": "Deliver Value",
            "process3desc": "Presentations are grounded in real outcomes from ventures across data storage, govtech, and precision medicine.",
            "cta": "Request a Speaking Engagement",
        },
        "caseStudies": {
            "eyebrow": "Case Studies",
            "title": "Building Companies That Scale",
            "lead": "Selected outcomes from founding and leading companies across data infrastructure and digital health.",
            "cs1eyebrow": "Data Infrastructure · 1996 — 2000",
            "cs1title": "9 Net Avenue Inc.",
            "cs1challenge": "Challenge",
            "cs1challengeText": "Build and scale a Data Storage company in a rapidly consolidating technology market.",
            "cs1action": "Approach",
            "cs1actionText": "Founded 9 Net Avenue Inc. in 1996. The company quickly became one of the world's largest Data Storage companies.",
            "cs1result": "Outcome",
            "cs1resultText": "By 2000, acquired by Concentric Networks (NASDAQ: CNTX), then XO Communications (NASDAQ: XOXO), reaching a peak market value of $19.5 billion. Following the acquisition, gained extensive experience working with public companies, serving on boards of directors, and participating in strategic decision-making at the highest executive level.",
            "cs2eyebrow": "Digital Health · 2021 — Present",
            "cs2title": "Digital Invest Inc.",
            "cs2challenge": "Challenge",
            "cs2challengeText": "Transform outdated approaches in medicine using science, DNA technologies, AI, and ML through a new bio-mathematical platform.",
            "cs2action": "Approach",
            "cs2actionText": "Founded and scaled Digital Invest Inc. from inception through a successful IPO. Led the full public offering process — legal structuring, financial compliance, investor roadshows, and SEC coordination. Directed design, construction, and operations of multiple data centers in the U.S. and Europe.",
            "cs2result": "Outcome",
            "cs2resultText": "Achieved consistent financial growth, positioning the company among Top 10 Precision Medicine Companies in the U.S. (2023). Digital Invest comprises diverse innovative projects, including Human Digital Model, BioMath Life, and Aero-Ground Robotics Operations Network.",
        },
        "mediaKit": {
            "eyebrow": "Press & Events",
            "title": "Media Kit",
            "lead": "Official biographies, imagery, and contact details for press, conferences, and board inquiries.",
            "bioEyebrow": "Biographies",
            "bioTitle": "Official Bios",
            "bioShortLabel": "50 Words",
            "bioShort": "Michael Kofman is CEO of Digital Invest Inc. and a board member, advisor, and founder of companies in technology and digital health across the U.S. and Europe.",
            "bioMediumLabel": "150 Words",
            "bioMedium": "Michael Kofman is the CEO of Digital Invest Inc. and serves on its Board of Directors. A technological visionary, he is renowned for his dynamic approach to understanding the ever-evolving needs of today's complex market. As an entrepreneur, board member, and advisor for both public and private companies, he has successfully established several companies in the United States and Europe. His expertise spans executive acumen, strategic analysis of emerging technologies and markets, information security and privacy, research, science and development, administration, and investment.",
            "bioLongLabel": "500 Words",
            "bioLong": "Michael Kofman is the CEO of Digital Invest Inc. and serves on its Board of Directors. A technological visionary, he is renowned for his dynamic approach to understanding the ever-evolving needs of today's complex market. His expertise spans executive acumen, strategic analysis of emerging technologies and markets, information security and privacy, research, science and development, administration, and investment. As an entrepreneur, board member, and advisor for both public and private companies, Michael Kofman has successfully established several companies in the United States and Europe. He founded 9 Net Avenue Inc., acquired at a peak market value of $19.5 billion, and leads Digital Invest Inc. in data storage and advanced technology innovation. He has directed technology strategy for government and defense programs, founded XIBI Group Inc. and DataPeer Inc. in data storage, and played a significant role in Biotechnology Group Inc. Collaborated with Harvard Medical School and Stanford Biomath on genetic reporting. Author of technical papers on satellite and optical systems; patent in digital satellite HDTV acquired by Sony. Education: Doctor of Technical Sciences (2009), Ph.D. in Information Technology (2004), Ukrainian State Marine Technical University.",
            "photosEyebrow": "Photography",
            "photosTitle": "Approved Images",
            "photosLead": "High-resolution portraits available upon request at mkofman@mkofman.com.",
            "contactEyebrow": "Press Contact",
            "contactTitle": "Media Inquiries",
            "contactLead": "For interviews, speaking invitations, and press requests.",
        },
        "articles": {
            "backLink": "← Back to Insights",
            "article1date": "Executive Perspective",
            "article1title": "From Engineering to Global Data Infrastructure",
            "article1p1": "My career began at the Nikolaev Shipbuilding Plant in Ukraine, developing satellite transceiver systems for transmitting classified information to military ships. I was recognized as an electronics engineer of the highest level — the 6th category at a plant of 93,000 employees.",
            "article1p2": "From 1989 to 1994, I founded and led Astra Corp, one of Europe's largest manufacturers of digital transceiver satellite systems. From 1994 to 1996, as CEO of Elitan United Inc., I helped scale the company from nine to over 4,000 employees worldwide.",
            "article1p3": "In 1996, I founded 9 Net Avenue Inc., which quickly became one of the world's largest Data Storage companies. By 2000, it was acquired by Concentric Networks (NASDAQ: CNTX) and XO Communications (NASDAQ: XOXO), reaching a peak market value of $19.5 billion.",
            "article1p4": "From 2001 to 2019, I directed technology strategy for government, defense, and state-owned enterprise programs — leading large-scale initiatives in big data, secure infrastructure, and high-throughput data centers across the United States and Europe.",
            "article2date": "Digital Health",
            "article2title": "Precision Medicine and the Convergence of Science and Technology",
            "article2p1": "I am a firm believer in the potential of combining life sciences with the latest technological advancements. At Biotechnology Group Inc. (2008–2014), we focused on DNA testing and analysis, process automation for creating genetic profiles, and comprehensive human genetic research.",
            "article2p2": "Under my leadership, successful genetic testing projects were initiated in Ukraine, Russia, and the Baltic countries. In collaboration with Harvard Medical School and Stanford Biomath, I played a crucial role in developing easily understandable genetic reports for both doctors and patients.",
            "article2p3": "With Digital Invest Inc., founded in 2021, we are dedicated to the bio-mathematical sphere — transforming outdated approaches in medicine using science, DNA technologies, AI, and ML. The company was scaled from inception through a successful IPO and recognized among America's Top 10 Best Companies in Precision Medicine and Digital Health in 2023.",
            "article2p4": "Digital Invest comprises diverse innovative projects, including Human Digital Model, BioMath Life, and Aero-Ground Robotics Operations Network — each advancing the integration of data science and life sciences.",
        },
        "recognition": {
            "moreLink": "View patents, publications, and press features on Insights →",
        },
        "insights": {
            "articlesEyebrow": "Perspectives",
            "articlesTitle": "Executive Perspectives",
        },
    },
    "ru": {
        "ui": {"sending": "Отправка…", "formError": "Не удалось отправить. Напишите на email напрямую."},
        "nav": {"speaking": "Выступления", "caseStudies": "Кейсы", "mediaKit": "Медиа-кит", "groupMain": "Основное", "groupServices": "Услуги", "groupWork": "Работа"},
        "cta": {"eyebrow": "Сотрудничество", "title": "Запросить advisory или выступление", "lead": "Для advisory-ролей, советов директоров, выступлений и стратегических партнёрств.", "button": "Связаться"},
        "home": {
            "heroSub": "CEO, советник советов директоров и стратегический технолог для публичных и частных компаний в технологиях, Data Storage и digital health.",
            "primaryCta": "Запросить advisory",
            "secondaryCta": "Смотреть кейсы",
            "featuredEyebrow": "Упоминания в СМИ",
            "caseStudiesEyebrow": "Результаты",
            "caseStudiesTitle": "Кейсы",
            "caseStudiesLead": "Основание, масштабирование и руководство компаниями — от старта до M&A и IPO.",
            "caseStudiesLink": "Все кейсы →",
            "cs1title": "9 Net Avenue Inc.",
            "cs1desc": "Построена одна из крупнейших в мире компаний Data Storage — приобретена при пиковой капитализации $19,5 млрд.",
            "cs2title": "Digital Invest Inc.",
            "cs2desc": "Основана и масштабирована от старта до IPO — Топ-10 precision medicine в США, 2023.",
        },
        "meta": {
            "speaking": {"title": "Выступления — Michael Kofman", "description": "Пригласите Michael Kofman выступить об executive-лидерстве, технологической стратегии и digital health."},
            "caseStudies": {"title": "Кейсы — Michael Kofman", "description": "Кейсы из карьеры Michael Kofman — 9 Net Avenue Inc. и Digital Invest Inc."},
            "mediaKit": {"title": "Медиа-кит — Michael Kofman", "description": "Официальные биографии, фото и контакты для прессы и организаторов мероприятий."},
            "article1": {"title": "От инженерии к глобальной инфраструктуре — Michael Kofman", "description": "Путь от спутниковой инженерии до основания глобальных компаний data infrastructure."},
            "article2": {"title": "Precision medicine и технологии — Michael Kofman", "description": "Объединение life sciences с ИИ, ML и ДНК-технологиями в современной медицине."},
        },
        "speaking": {
            "eyebrow": "Выступления",
            "title": "Пригласить Michael Kofman",
            "lead": "Доступен для выступлений об executive-лидерстве, технологической стратегии, digital health, data infrastructure и корпоративном управлении.",
            "topicsEyebrow": "Темы",
            "topicsTitle": "Области экспертизы",
            "topicsLead": "Темы основаны на десятилетиях опыта основания и руководства компаниями в США и Европе.",
            "processEyebrow": "Как пригласить",
            "processTitle": "Процесс",
            "process1title": "Отправьте запрос",
            "process1desc": "Используйте форму контактов или email mkofman@mkofman.com с деталями мероприятия.",
            "process2title": "Согласуйте формат",
            "process2desc": "Ключевая речь, панель, сессия совета директоров или executive roundtable.",
            "process3title": "Практическая ценность",
            "process3desc": "Выступления основаны на реальных результатах в data storage, govtech и precision medicine.",
            "cta": "Запросить выступление",
        },
        "caseStudies": {
            "eyebrow": "Кейсы",
            "title": "Компании, которые масштабируются",
            "lead": "Избранные результаты из основания и руководства компаниями в data infrastructure и digital health.",
            "cs1eyebrow": "Data Infrastructure · 1996 — 2000",
            "cs1title": "9 Net Avenue Inc.",
            "cs1challenge": "Задача",
            "cs1challengeText": "Построить и масштабировать компанию Data Storage на быстро консолидирующемся рынке.",
            "cs1action": "Подход",
            "cs1actionText": "Основана 9 Net Avenue Inc. в 1996 году. Компания быстро стала одной из крупнейших в мире в сфере Data Storage.",
            "cs1result": "Результат",
            "cs1resultText": "К 2000 году приобретена Concentric Networks (NASDAQ: CNTX), затем XO Communications (NASDAQ: XOXO), с пиковой капитализацией $19,5 млрд. После приобретения — опыт работы в публичных компаниях и на советах директоров.",
            "cs2eyebrow": "Digital Health · 2021 — настоящее время",
            "cs2title": "Digital Invest Inc.",
            "cs2challenge": "Задача",
            "cs2challengeText": "Трансформировать устаревшие подходы в медицине с помощью науки, ДНК-технологий, ИИ и ML.",
            "cs2action": "Подход",
            "cs2actionText": "Основана и масштабирована Digital Invest Inc. от старта до успешного IPO. Руководство полным процессом публичного размещения.",
            "cs2result": "Результат",
            "cs2resultText": "Топ-10 precision medicine в США (2023). Проекты: Human Digital Model, BioMath Life, Aero-Ground Robotics Operations Network.",
        },
        "mediaKit": {
            "eyebrow": "Пресса и мероприятия",
            "title": "Медиа-кит",
            "lead": "Официальные биографии, изображения и контакты для прессы и конференций.",
            "bioEyebrow": "Биографии",
            "bioTitle": "Официальные bio",
            "bioShortLabel": "50 слов",
            "bioShort": "Michael Kofman — CEO Digital Invest Inc., член советов директоров, советник и основатель компаний в технологиях и digital health в США и Европе.",
            "bioMediumLabel": "150 слов",
            "bioMedium": "Michael Kofman — генеральный директор Digital Invest Inc. и член её совета директоров. Технологический визионер, предприниматель, член советов директоров и советник публичных и частных компаний в США и Европе. Экспертиза: executive-менеджмент, emerging-технологии, информационная безопасность, исследования, наука и разработки, администрирование и инвестиции.",
            "bioLongLabel": "500 слов",
            "bioLong": "Michael Kofman — CEO Digital Invest Inc. и член совета директоров. Основал 9 Net Avenue Inc. (пиковая капитализация $19,5 млрд). Руководит Digital Invest Inc. в data storage и передовых технологиях. Опыт в govtech и defense, XIBI Group Inc., DataPeer Inc., Biotechnology Group Inc. Сотрудничество с Harvard Medical School и Stanford Biomath. Автор технических работ; патент HDTV, приобретённый Sony. Образование: доктор технических наук (2009), Ph.D. в IT (2004), Ukrainian State Marine Technical University.",
            "photosEyebrow": "Фотографии",
            "photosTitle": "Одобренные изображения",
            "photosLead": "Портреты высокого разрешения — по запросу на mkofman@mkofman.com.",
            "contactEyebrow": "Пресс-контакт",
            "contactTitle": "Медиа-запросы",
            "contactLead": "Интервью, приглашения на выступления и пресс-запросы.",
        },
        "articles": {
            "backLink": "← Назад к Insights",
            "article1date": "Executive perspective",
            "article1title": "От инженерии к глобальной data infrastructure",
            "article1p1": "Карьера началась на судостроительном заводе в Николаеве — спутниковые трансиверы для военных кораблей. 6-я категория инженера на заводе с 93 000 сотрудников.",
            "article1p2": "1989–1994: Astra Corp — один из крупнейших в Европе производителей спутниковых систем. 1994–1996: CEO Elitan United Inc. — рост с 9 до 4 000+ сотрудников.",
            "article1p3": "1996: 9 Net Avenue Inc. — одна из крупнейших компаний Data Storage. К 2000 году — приобретение Concentric Networks и XO Communications, пик $19,5 млрд.",
            "article1p4": "2001–2019: технологическая стратегия для govtech и defense — big data, защищённая инфраструктура, дата-центры в США и Европе.",
            "article2date": "Digital Health",
            "article2title": "Precision medicine и конвергенция науки и технологий",
            "article2p1": "Biotechnology Group Inc. (2008–2014): ДНК-тестирование, автоматизация генетических профилей, исследования человеческой генетики.",
            "article2p2": "Проекты в Украине, России и Балтии. Сотрудничество с Harvard Medical School и Stanford Biomath над генетическими отчётами.",
            "article2p3": "Digital Invest Inc. (2021): биоматематическая сфера, ИИ, ML, ДНК. IPO. Топ-10 precision medicine в США, 2023.",
            "article2p4": "Проекты: Human Digital Model, BioMath Life, Aero-Ground Robotics Operations Network.",
        },
        "recognition": {"moreLink": "Патенты, публикации и пресса — на странице Insights →"},
        "insights": {"articlesEyebrow": "Перспективы", "articlesTitle": "Executive perspectives"},
    },
}

# Other langs: use English as base (i18n falls back to en)
FALLBACK_LANGS = ["es", "de", "fr", "uk", "zh", "ar", "he"]


def deep_merge(target, source):
    for k, v in source.items():
        if isinstance(v, dict) and isinstance(target.get(k), dict):
            deep_merge(target[k], v)
        else:
            target[k] = v


def patch_translations():
    path = os.path.join(ROOT, "js", "translations.js")
    text = open(path, encoding="utf-8").read()
    data = json.loads(text.replace("const TRANSLATIONS = ", "").rstrip(";\n"))
    for lang in data:
        if lang in NEW_TRANSLATIONS:
            deep_merge(data[lang], NEW_TRANSLATIONS[lang])
        elif lang in FALLBACK_LANGS:
            deep_merge(data[lang], NEW_TRANSLATIONS["en"])
    with open(path, "w", encoding="utf-8") as f:
        f.write("const TRANSLATIONS = ")
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.write(";\n")
    print("patched translations.js")


def patch_scripts():
    for name in os.listdir(ROOT):
        if not name.endswith(".html"):
            continue
        path = os.path.join(ROOT, name)
        html = open(path, encoding="utf-8").read()
        if "js/site-config.js" not in html:
            html = html.replace(
                '<script src="js/translations.js"></script>',
                '<script src="js/site-config.js"></script>\n  <script src="js/translations.js"></script>',
            )
        for script in ["forms.js", "og-meta.js", "cta.js"]:
            if f"js/{script}" not in html:
                html = html.replace(
                    '<script src="js/main.js"></script>',
                    f'<script src="js/{script}"></script>\n  <script src="js/main.js"></script>',
                )
        open(path, "w", encoding="utf-8").write(html)
    print("patched script tags")


def main():
    patch_translations()
    patch_scripts()


if __name__ == "__main__":
    main()
