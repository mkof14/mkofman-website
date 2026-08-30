#!/usr/bin/env python3
"""Tighten site copy: remove boilerplate, dedupe, sync translations."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LANGS = ["en", "es", "de", "fr", "ru", "uk", "zh", "ar", "he"]

BOILERPLATE_BIO = (
    "Michael Kofman is the CEO of Digital Invest Inc. and founder of AGRON Inc. "
    "He serves on the Digital Invest Board of Directors. A technological visionary, "
    "he is renowned for his dynamic approach to understanding the ever-evolving needs "
    "of today's complex market. His expertise spans executive acumen, strategic analysis "
    "of emerging technologies and markets, information security and privacy, research, "
    "science and development, administration, and investment."
)

BIO_P1 = {
    "en": (
        "Michael Kofman is CEO of Digital Invest Inc. and founder of AGRON Inc. "
        "He serves on the Digital Invest board. His work spans company building, "
        "technology strategy, security, research, and investment in the U.S. and Europe."
    ),
    "es": (
        "Michael Kofman es CEO de Digital Invest Inc. y fundador de AGRON Inc. "
        "Forma parte del consejo de Digital Invest. Su trabajo abarca la creación de "
        "empresas, estrategia tecnológica, seguridad, investigación e inversión en "
        "Estados Unidos y Europa."
    ),
    "de": (
        "Michael Kofman ist CEO von Digital Invest Inc. und Gründer von AGRON Inc. "
        "Er gehört dem Vorstand von Digital Invest an. Seine Arbeit umfasst "
        "Unternehmensaufbau, Technologiestrategie, Sicherheit, Forschung und "
        "Investitionen in den USA und Europa."
    ),
    "fr": (
        "Michael Kofman est PDG de Digital Invest Inc. et fondateur d'AGRON Inc. "
        "Il siège au conseil de Digital Invest. Son travail couvre la création "
        "d'entreprises, la stratégie technologique, la sécurité, la recherche et "
        "l'investissement aux États-Unis et en Europe."
    ),
    "ru": (
        "Майкл Кофман — генеральный директор Digital Invest Inc. и основатель AGRON Inc., "
        "член совета директоров Digital Invest. Его работа охватывает создание компаний, "
        "технологическую стратегию, безопасность, исследования и инвестиции в США и Европе."
    ),
    "uk": (
        "Майкл Кофман — генеральний директор Digital Invest Inc. і засновник AGRON Inc., "
        "член ради директорів Digital Invest. Його робота охоплює створення компаній, "
        "технологічну стратегію, безпеку, дослідження та інвестиції в США та Європі."
    ),
    "zh": (
        "Michael Kofman 是 Digital Invest Inc. 首席执行官兼 AGRON Inc. 创始人，"
        "担任 Digital Invest 董事会成员。其工作涵盖在美国和欧洲的公司创建、"
        "技术战略、安全、研究与投资。"
    ),
    "ar": (
        "Michael Kofman هو الرئيس التنفيذي لـ Digital Invest Inc. ومؤسس AGRON Inc. "
        "وعضو مجلس إدارة Digital Invest. يشمل عمله بناء الشركات والاستراتيجية "
        "التقنية والأمن والبحث والاستثمار في الولايات المتحدة وأوروبا."
    ),
    "he": (
        "Michael Kofman הוא מנכ\"ל Digital Invest Inc. ומייסד AGRON Inc. "
        "וחבר בדירקטוריון Digital Invest. עבודתו כוללת הקמת חברות, אסטרטגיה "
        "טכנולוגית, אבטחה, מחקר והשקעות בארה\"ב ובאירופה."
    ),
}

HOME = {
    "en": {
        "heroTitle1": "Built to Endure.",
        "heroTitle2": "Led with Judgment.",
        "quote4text": (
            "Engineering precision paired with business strategy — from satellite systems "
            "to $19.5B infrastructure to precision medicine."
        ),
        "aboutTitle": "Companies Built to Last",
        "aboutLead1": (
            "CEO of Digital Invest Inc. and founder of AGRON Inc. He has founded and "
            "led companies across the U.S. and Europe."
        ),
        "aboutLead2": (
            "From 9 Net Avenue ($19.5B peak valuation) to Digital Invest in precision "
            "medicine and AGRON in robotics — four decades in infrastructure, health, "
            "and defense."
        ),
        "expertiseEyebrow": "Focus Areas",
        "expertiseLead": (
            "Four decades building, advising, and investing across infrastructure, "
            "health, and robotics."
        ),
        "recLead": (
            "Industry awards and peer recognition across entrepreneurship, "
            "medicine, and engineering."
        ),
    },
    "es": {
        "heroTitle1": "Hecho para perdurar.",
        "heroTitle2": "Liderado con criterio.",
        "quote4text": (
            "Precisión de ingeniería y estrategia empresarial — desde sistemas "
            "satelitales hasta infraestructura de $19,5 mil millones y medicina de precisión."
        ),
        "aboutTitle": "Empresas hechas para durar",
        "aboutLead1": (
            "CEO de Digital Invest Inc. y fundador de AGRON Inc. Ha fundado y "
            "dirigido empresas en Estados Unidos y Europa."
        ),
        "aboutLead2": (
            "Desde 9 Net Avenue (valoración pico de $19,5 mil millones) hasta Digital "
            "Invest en medicina de precisión y AGRON en robótica — cuatro décadas en "
            "infraestructura, salud y defensa."
        ),
        "expertiseEyebrow": "Áreas de enfoque",
        "expertiseLead": (
            "Cuatro décadas construyendo, asesorando e invirtiendo en infraestructura, "
            "salud y robótica."
        ),
        "recLead": (
            "Premios del sector y reconocimiento entre pares en emprendimiento, "
            "medicina e ingeniería."
        ),
    },
    "de": {
        "heroTitle1": "Gebaut für die Dauer.",
        "heroTitle2": "Geführt mit Urteilsvermögen.",
        "quote4text": (
            "Ingenieurpräzision und Geschäftsstrategie — von Satellitensystemen "
            "über $19,5 Mrd. Infrastruktur bis zur Präzisionsmedizin."
        ),
        "aboutTitle": "Unternehmen, die Bestand haben",
        "aboutLead1": (
            "CEO von Digital Invest Inc. und Gründer von AGRON Inc. Er hat Unternehmen "
            "in den USA und Europa gegründet und geführt."
        ),
        "aboutLead2": (
            "Von 9 Net Avenue ($19,5 Mrd. Spitzenbewertung) über Digital Invest in der "
            "Präzisionsmedizin bis AGRON in der Robotik — vier Jahrzehnte in Infrastruktur, "
            "Gesundheit und Verteidigung."
        ),
        "expertiseEyebrow": "Schwerpunkte",
        "expertiseLead": (
            "Vier Jahrzehnte Aufbau, Beratung und Investment in Infrastruktur, "
            "Gesundheit und Robotik."
        ),
        "recLead": (
            "Branchenauszeichnungen und Anerkennung in Unternehmertum, Medizin "
            "und Ingenieurwesen."
        ),
    },
    "fr": {
        "heroTitle1": "Construit pour durer.",
        "heroTitle2": "Dirigé avec discernement.",
        "quote4text": (
            "Précision d'ingénierie et stratégie commerciale — des systèmes "
            "satellites à une infrastructure de 19,5 milliards $ et à la médecine de précision."
        ),
        "aboutTitle": "Des entreprises faites pour durer",
        "aboutLead1": (
            "PDG de Digital Invest Inc. et fondateur d'AGRON Inc. Il a fondé et "
            "dirigé des entreprises aux États-Unis et en Europe."
        ),
        "aboutLead2": (
            "De 9 Net Avenue (valorisation pic de 19,5 milliards $) à Digital Invest "
            "en médecine de précision et AGRON en robotique — quatre décennies dans "
            "l'infrastructure, la santé et la défense."
        ),
        "expertiseEyebrow": "Domaines d'intervention",
        "expertiseLead": (
            "Quatre décennies de création, de conseil et d'investissement dans "
            "l'infrastructure, la santé et la robotique."
        ),
        "recLead": (
            "Prix du secteur et reconnaissance par les pairs en entrepreneuriat, "
            "médecine et ingénierie."
        ),
    },
    "ru": {
        "heroTitle1": "Строить надолго.",
        "heroTitle2": "Руководить с весом.",
        "quote4text": (
            "Инженерная точность и бизнес-стратегия — от спутниковых систем "
            "до инфраструктуры на $19,5 млрд и precision medicine."
        ),
        "aboutTitle": "Компании, рассчитанные на долгий срок",
        "aboutLead1": (
            "CEO Digital Invest Inc. и основатель AGRON Inc. Основал и руководил "
            "компаниями в США и Европе."
        ),
        "aboutLead2": (
            "От 9 Net Avenue (пик $19,5 млрд) до Digital Invest в precision medicine "
            "и AGRON в робототехнике — четыре десятилетия в инфраструктуре, "
            "здравоохранении и обороне."
        ),
        "expertiseEyebrow": "Направления",
        "expertiseLead": (
            "Четыре десятилетия создания компаний, консультирования и инвестиций "
            "в инфраструктуру, здравоохранение и робототехнику."
        ),
        "recLead": (
            "Отраслевые награды и признание в предпринимательстве, медицине "
            "и инженерии."
        ),
    },
    "uk": {
        "heroTitle1": "Будувати на довгі роки.",
        "heroTitle2": "Керувати з розумінням.",
        "quote4text": (
            "Інженерна точність і бізнес-стратегія — від супутникових систем "
            "до інфраструктури на $19,5 млрд і precision medicine."
        ),
        "aboutTitle": "Компанії, розраховані на тривалий час",
        "aboutLead1": (
            "CEO Digital Invest Inc. і засновник AGRON Inc. Заснував і очолював "
            "компанії в США та Європі."
        ),
        "aboutLead2": (
            "Від 9 Net Avenue (пік $19,5 млрд) до Digital Invest у precision medicine "
            "та AGRON у робототехніці — чотири десятиліття в інфраструктурі, "
            "охороні здоров'я та обороні."
        ),
        "expertiseEyebrow": "Напрямки",
        "expertiseLead": (
            "Чотири десятиліття створення компаній, консультування та інвестицій "
            "в інфраструктуру, охорону здоров'я та робототехніку."
        ),
        "recLead": (
            "Галузеві нагороди та визнання в підприємництві, медицині "
            "та інженерії."
        ),
    },
    "zh": {
        "heroTitle1": "基业长青。",
        "heroTitle2": "审慎领导。",
        "quote4text": (
            "工程精度与商业战略并重——从卫星系统到195亿美元基础设施，"
            "再到精准医疗。"
        ),
        "aboutTitle": "经得起时间考验的公司",
        "aboutLead1": (
            "Digital Invest Inc. 首席执行官兼 AGRON Inc. 创始人。"
            "在美国和欧洲创立并领导多家公司。"
        ),
        "aboutLead2": (
            "从 9 Net Avenue（峰值估值195亿美元）到 Digital Invest 精准医疗"
            "和 AGRON 机器人——四十年深耕基础设施、医疗与国防。"
        ),
        "expertiseEyebrow": "重点领域",
        "expertiseLead": (
            "四十年在基础设施、医疗和机器人领域的创业、咨询与投资。"
        ),
        "recLead": (
            "在创业、医学和工程领域获得行业奖项与同行认可。"
        ),
    },
    "ar": {
        "heroTitle1": "مبني ليدوم.",
        "heroTitle2": "قيادة بحكمة.",
        "quote4text": (
            "دقة هندسية مع استراتيجية أعمال — من أنظمة الأقمار الصناعية "
            "إلى بنية تحتية بقيمة 19.5 مليار دولار والطب الدقيق."
        ),
        "aboutTitle": "شركات مصممة للبقاء",
        "aboutLead1": (
            "الرئيس التنفيذي لـ Digital Invest Inc. ومؤسس AGRON Inc. "
            "أسس وقاد شركات في الولايات المتحدة وأوروبا."
        ),
        "aboutLead2": (
            "من 9 Net Avenue (ذروة تقييم 19.5 مليار دولار) إلى Digital Invest "
            "في الطب الدقيق وAGRON في الروبوتات — أربعة عقود في البنية التحتية "
            "والصحة والدفاع."
        ),
        "expertiseEyebrow": "مجالات التركيز",
        "expertiseLead": (
            "أربعة عقود في بناء الشركات والاستشارة والاستثمار في البنية "
            "التحتية والصحة والروبوتات."
        ),
        "recLead": (
            "جوائز صناعية وتقدير من الأقران في ريادة الأعمال والطب والهندسة."
        ),
    },
    "he": {
        "heroTitle1": "נבנה להישאר.",
        "heroTitle2": "מונחה בשיקול דעת.",
        "quote4text": (
            "דיוק הנדסי עם אסטרטגיה עסקית — ממערכות לוויין "
            "לתשתית של 19.5 מיליארד דולר ורפואת דיוק."
        ),
        "aboutTitle": "חברות שנבנו לטווח ארוך",
        "aboutLead1": (
            "מנכ\"ל Digital Invest Inc. ומייסד AGRON Inc. "
            "ייסד והוביל חברות בארה\"ב ובאירופה."
        ),
        "aboutLead2": (
            "מ-9 Net Avenue (שווי שיא 19.5 מיליארד דולר) ל-Digital Invest "
            "ברפואת דיוק ו-AGRON ברובוטיקה — ארבעה עשורים בתשתית, "
            "בריאות וביטחון."
        ),
        "expertiseEyebrow": "תחומי מיקוד",
        "expertiseLead": (
            "ארבעה עשורים של בנייה, ייעוץ והשקעה בתשתית, "
            "בריאות ורובוטיקה."
        ),
        "recLead": (
            "פרסי תעשייה והכרה בקרב עמיתים ביזמות, רפואה והנדסה."
        ),
    },
}

CONSULTING = {
    "en": {
        "heroLead": (
            "Thirty-five years founding and advising companies in the U.S. and Europe — "
            "data infrastructure, govtech, precision medicine, and robotics."
        ),
        "introLead": (
            "CEO of Digital Invest Inc. and board director. Focus: emerging technology, "
            "security, research, and capital allocation."
        ),
    },
    "es": {
        "heroLead": (
            "Treinta y cinco años fundando y asesorando empresas en EE. UU. y Europa — "
            "infraestructura de datos, govtech, medicina de precisión y robótica."
        ),
        "introLead": (
            "CEO de Digital Invest Inc. y miembro del consejo. Enfoque: tecnología "
            "emergente, seguridad, investigación y asignación de capital."
        ),
    },
    "de": {
        "heroLead": (
            "Fünfunddreißig Jahre Gründung und Beratung von Unternehmen in den USA "
            "und Europa — Dateninfrastruktur, GovTech, Präzisionsmedizin und Robotik."
        ),
        "introLead": (
            "CEO von Digital Invest Inc. und Vorstandsmitglied. Schwerpunkte: "
            "Emerging Technology, Sicherheit, Forschung und Kapitalallokation."
        ),
    },
    "fr": {
        "heroLead": (
            "Trente-cinq ans à fonder et conseiller des entreprises aux États-Unis "
            "et en Europe — infrastructure de données, govtech, médecine de précision "
            "et robotique."
        ),
        "introLead": (
            "PDG de Digital Invest Inc. et membre du conseil. Axes : technologies "
            "émergentes, sécurité, recherche et allocation de capital."
        ),
    },
    "ru": {
        "heroLead": (
            "Тридцать пять лет создания и консультирования компаний в США и Европе — "
            "инфраструктура данных, govtech, precision medicine и робототехника."
        ),
        "introLead": (
            "CEO Digital Invest Inc., член совета директоров. Фокус: emerging-технологии, "
            "безопасность, исследования и распределение капитала."
        ),
    },
    "uk": {
        "heroLead": (
            "Тридцять п'ять років створення та консультування компаній у США та Європі — "
            "інфраструктура даних, govtech, precision medicine та робототехніка."
        ),
        "introLead": (
            "CEO Digital Invest Inc., член ради директорів. Фокус: emerging-технології, "
            "безпека, дослідження та розподіл капіталу."
        ),
    },
    "zh": {
        "heroLead": (
            "三十五年在美国和欧洲创立并顾问公司——"
            "数据基础设施、政府科技、精准医疗和机器人。"
        ),
        "introLead": (
            "Digital Invest Inc. 首席执行官兼董事会成员。"
            "重点：新兴技术、安全、研究与资本配置。"
        ),
    },
    "ar": {
        "heroLead": (
            "خمس وثلاثون سنة في تأسيس الشركات والاستشارة في الولايات المتحدة "
            "وأوروبا — البنية التحتية للبيانات والحكومة الرقمية والطب الدقيق "
            "والروبوتات."
        ),
        "introLead": (
            "الرئيس التنفيذي لـ Digital Invest Inc. وعضو مجلس الإدارة. "
            "التركيز: التقنيات الناشئة والأمن والبحث وتخصيص رأس المال."
        ),
    },
    "he": {
        "heroLead": (
            "שלושים וחמש שנים של הקמת חברות וייעוץ בארה\"ב ובאירופה — "
            "תשתיות נתונים, govtech, רפואת דיוק ורובוטיקה."
        ),
        "introLead": (
            "מנכ\"ל Digital Invest Inc. וחבר דירקטוריון. מיקוד: טכנולוגיות מתפתחות, "
            "אבטחה, מחקר והקצאת הון."
        ),
    },
}

ABOUT = {
    "en": {"title": "Built Over Three Decades", "lead": "Entrepreneur and executive across engineering, infrastructure, digital health, and robotics."},
    "es": {"title": "Construido en tres décadas", "lead": "Emprendedor y ejecutivo en ingeniería, infraestructura, salud digital y robótica."},
    "de": {"title": "Drei Jahrzehnte Erfahrung", "lead": "Unternehmer und Führungskraft in Ingenieurwesen, Infrastruktur, Digital Health und Robotik."},
    "fr": {"title": "Trois décennies de parcours", "lead": "Entrepreneur et dirigeant en ingénierie, infrastructure, santé numérique et robotique."},
    "ru": {"title": "Три десятилетия опыта", "lead": "Предприниматель и executive в инженерии, инфраструктуре, digital health и робототехнике."},
    "uk": {"title": "Три десятиліття досвіду", "lead": "Підприємець і executive в інженерії, інфраструктурі, digital health і робототехніці."},
    "zh": {"title": "三十年历程", "lead": "工程、基础设施、数字医疗和机器人领域的企业家与高管。"},
    "ar": {"title": "ثلاثة عقود من الخبرة", "lead": "رائد أعمال وتنفيذي في الهندسة والبنية التحتية والصحة الرقمية والروبوتات."},
    "he": {"title": "שלושה עשורים של ניסיון", "lead": "יזם ומנהל בתחומי הנדסה, תשתית, בריאות דיגיטלית ורובוטיקה."},
}

VENTURES = {
    "en": {"title": "Companies Founded & Led", "lead": "From precision medicine and robotics to global data infrastructure — founded, scaled, and led across the U.S. and Europe."},
    "es": {"title": "Empresas fundadas y lideradas", "lead": "Desde medicina de precisión y robótica hasta infraestructura global de datos — fundadas, escaladas y dirigidas en EE. UU. y Europa."},
    "de": {"title": "Gegründete und geführte Unternehmen", "lead": "Von Präzisionsmedizin und Robotik bis zur globalen Dateninfrastruktur — gegründet, skaliert und geführt in den USA und Europa."},
    "fr": {"title": "Entreprises fondées et dirigées", "lead": "De la médecine de précision et la robotique à l'infrastructure mondiale de données — fondées, développées et dirigées aux États-Unis et en Europe."},
    "ru": {"title": "Основанные и возглавляемые компании", "lead": "От precision medicine и робототехники до глобальной data infrastructure — создание, масштабирование и руководство в США и Европе."},
    "uk": {"title": "Засновані та очолювані компанії", "lead": "Від precision medicine і робототехніки до глобальної data infrastructure — створення, масштабування та керівництво в США та Європі."},
    "zh": {"title": "创立并领导的公司", "lead": "从精准医疗和机器人到全球数据基础设施——在美国和欧洲创立、扩展并领导。"},
    "ar": {"title": "شركات أسستها وقادها", "lead": "من الطب الدقيق والروبوتات إلى البنية التحتية العالمية للبيانات — تأسيس وتوسيع وقيادة في الولايات المتحدة وأوروبا."},
    "he": {"title": "חברות שהקים והוביל", "lead": "מרפואת דיוק ורובוטיקה ועד תשתיות נתונים גלובליות — הקמה, צמיחה והובלה בארה\"ב ובאירופה."},
}

RECOGNITION = {
    "en": {"title": "Awards & Recognition", "lead": "Honors spanning entrepreneurship, precision medicine, engineering, and executive leadership."},
    "es": {"title": "Premios y reconocimientos", "lead": "Distinciones en emprendimiento, medicina de precisión, ingeniería y liderazgo ejecutivo."},
    "de": {"title": "Auszeichnungen & Anerkennung", "lead": "Ehrungen in Unternehmertum, Präzisionsmedizin, Ingenieurwesen und Führung."},
    "fr": {"title": "Prix et reconnaissance", "lead": "Distinctions en entrepreneuriat, médecine de précision, ingénierie et leadership exécutif."},
    "ru": {"title": "Награды и признание", "lead": "Награды в предпринимательстве, precision medicine, инженерии и executive-лидерстве."},
    "uk": {"title": "Нагороди та визнання", "lead": "Відзнаки в підприємництві, precision medicine, інженерії та executive-лідерстві."},
    "zh": {"title": "奖项与认可", "lead": "涵盖创业、精准医疗、工程和领导力的荣誉。"},
    "ar": {"title": "الجوائز والتقدير", "lead": "تكريم في ريادة الأعمال والطب الدقيق والهندسة والقيادة التنفيذية."},
    "he": {"title": "פרסים והכרה", "lead": "הוקרה ביזמות, רפואת דיוק, הנדסה ומנהיגות."},
}

FOOTER = {
    "en": "CEO, technologist, and founder. Digital health, data infrastructure, robotics.",
    "es": "CEO, tecnólogo y fundador. Salud digital, infraestructura de datos, robótica.",
    "de": "CEO, Technologe und Gründer. Digital Health, Dateninfrastruktur, Robotik.",
    "fr": "PDG, technologue et fondateur. Santé numérique, infrastructure de données, robotique.",
    "ru": "CEO, технолог и основатель. Digital health, инфраструктура данных, робототехника.",
    "uk": "CEO, технолог і засновник. Digital health, інфраструктура даних, робототехніка.",
    "zh": "首席执行官、技术专家和创始人。数字医疗、数据基础设施、机器人。",
    "ar": "الرئيس التنفيذي والتقني والمؤسس. الصحة الرقمية والبنية التحتية للبيانات والروبوتات.",
    "he": "מנכ\"ל, טכנולוג ומייסד. בריאות דיגיטלית, תשתיות נתונים, רובוטיקה.",
}

QUOTE1 = {
    "en": "Featured among America's leading companies in precision medicine and digital health.",
    "es": "Destacado entre las principales empresas de medicina de precisión y salud digital de EE. UU.",
    "de": "Ausgewiesen als eines der führenden Unternehmen der USA in Präzisionsmedizin und Digital Health.",
    "fr": "Figurant parmi les principales entreprises américaines en médecine de précision et santé numérique.",
    "ru": "Digital Invest Inc. — среди ведущих компаний США в precision medicine и digital health.",
    "uk": "Digital Invest Inc. — серед провідних компаній США в precision medicine та digital health.",
    "zh": "入选美国精准医疗与数字健康领域的领先公司。",
    "ar": "من بين الشركات الأمريكية الرائدة في الطب الدقيق والصحة الرقمية.",
    "he": "מוזכר בין החברות המובילות בארה\"ב ברפואת דיוק ובריאות דיגיטלית.",
}

INSIGHTS = {
    "en": {"heroTitle": "Executive Perspectives"},
    "es": {"heroTitle": "Perspectivas ejecutivas"},
    "de": {"heroTitle": "Executive Perspectives"},
    "fr": {"heroTitle": "Perspectives exécutives"},
    "ru": {"heroTitle": "Executive Perspectives"},
    "uk": {"heroTitle": "Executive Perspectives"},
    "zh": {"heroTitle": "高管视角"},
    "ar": {"heroTitle": "وجهات نظر تنفيذية"},
    "he": {"heroTitle": "פרספקטивות מנהיגות"},
}

CONSULTING_TITLES = {
    "en": {"heroTitle": "Strategic Advisory"},
    "es": {"heroTitle": "Asesoría estratégica"},
    "de": {"heroTitle": "Strategische Beratung"},
    "fr": {"heroTitle": "Conseil stratégique"},
    "ru": {"heroTitle": "Стратегическое консультирование"},
    "uk": {"heroTitle": "Стратегічне консультування"},
    "zh": {"heroTitle": "战略顾问"},
    "ar": {"heroTitle": "استشارات استراتيجية"},
    "he": {"heroTitle": "ייעוץ אסטרטגי"},
}

META_HOME = {
    "es": "Sitio oficial de Michael Kofman — CEO, fundador y asesor de consejos en tecnología y salud digital.",
    "de": "Offizielle Website von Michael Kofman — CEO, Gründer und Board-Berater in Technologie und Digital Health.",
    "fr": "Site officiel de Michael Kofman — PDG, fondateur et conseiller de conseils en technologie et santé numérique.",
    "ru": "Официальный сайт Michael Kofman — CEO, основатель и советник советов директоров в технологиях и digital health.",
    "uk": "Офіційний сайт Michael Kofman — CEO, засновник і радник рад директорів у технологіях і digital health.",
    "zh": "Michael Kofman 官方网站——技术与数字医疗领域的首席执行官、创始人和董事会顾问。",
    "ar": "الموقع الرسمي لـ Michael Kofman — الرئيس التنفيذي والمؤسس ومستشار مجالس الإدارة في التكنولوجيا والصحة الرقمية.",
    "he": "האתר הרשמי של Michael Kofman — מנכ\"ל, מייסד ויועץ דירקטוריון בטכנולוגיה ובריאות דיגיטלית.",
}

META_ABOUT = {
    "es": "Biografía de Michael Kofman — CEO de Digital Invest Inc., fundador de AGRON Inc.",
    "de": "Biografie von Michael Kofman — CEO von Digital Invest Inc., Gründer von AGRON Inc.",
    "fr": "Biographie de Michael Kofman — PDG de Digital Invest Inc., fondateur d'AGRON Inc.",
    "ru": "Биография Michael Kofman — CEO Digital Invest Inc., основатель AGRON Inc.",
    "uk": "Біографія Michael Kofman — CEO Digital Invest Inc., засновник AGRON Inc.",
    "zh": "Michael Kofman 传记——Digital Invest Inc. 首席执行官，AGRON Inc. 创始人。",
    "ar": "سيرة Michael Kofman — الرئيس التنفيذي لـ Digital Invest Inc. ومؤسس AGRON Inc.",
    "he": "ביוגרפיה של Michael Kofman — מנכ\"ל Digital Invest Inc., מייסד AGRON Inc.",
}

MEDIA_KIT = {
    "en": {
        "bioMedium": (
            "Michael Kofman is CEO of Digital Invest Inc. and serves on its board. "
            "An entrepreneur, board member, and advisor, he has founded companies in the "
            "U.S. and Europe across data infrastructure, digital health, and robotics. "
            "His work spans technology strategy, security, research, and investment."
        ),
        "bioLong": (
            "Michael Kofman is CEO of Digital Invest Inc. and serves on its board. "
            "He founded 9 Net Avenue Inc., acquired at a peak market value of $19.5 billion, "
            "and leads Digital Invest in precision medicine. He has directed technology "
            "strategy for government and defense programs, founded XIBI Group Inc. and "
            "DataPeer Inc., and led Biotechnology Group Inc. Collaborated with Harvard "
            "Medical School and Stanford Biomath on genetic reporting. Author of technical "
            "papers on satellite and optical systems; patent in digital satellite HDTV "
            "acquired by Sony. In 2026 he founded AGRON Inc. for aerial-ground robotics "
            "and maritime intelligence. Education: Doctor of Technical Sciences (2009), "
            "Ph.D. in Information Technology (2004), Ukrainian State Marine Technical University."
        ),
    },
    "ru": {
        "bioMedium": (
            "Michael Kofman — CEO Digital Invest Inc. и член совета директоров. "
            "Предприниматель, член советов и советник; основал компании в США и Европе "
            "в data infrastructure, digital health и робототехнике. "
            "Работа охватывает технологическую стратегию, безопасность, исследования и инвестиции."
        ),
        "bioLong": (
            "Michael Kofman — CEO Digital Invest Inc. и член совета директоров. "
            "Основал 9 Net Avenue Inc. (пиковая капитализация $19,5 млрд) и руководит "
            "Digital Invest в precision medicine. Опыт в govtech и defense, XIBI Group Inc., "
            "DataPeer Inc., Biotechnology Group Inc. Сотрудничество с Harvard Medical School "
            "и Stanford Biomath. Автор технических работ; патент HDTV, приобретённый Sony. "
            "В 2026 году основал AGRON Inc. для aerial-ground robotics и maritime intelligence. "
            "Образование: доктор технических наук (2009), Ph.D. в IT (2004), "
            "Ukrainian State Marine Technical University."
        ),
    },
    "uk": {
        "bioMedium": (
            "Michael Kofman — CEO Digital Invest Inc. і член ради директорів. "
            "Підприємець, член рад і радник; заснував компанії в США та Європі "
            "в data infrastructure, digital health і робототехніці. "
            "Робота охоплює технологічну стратегію, безпеку, дослідження та інвестиції."
        ),
        "bioLong": (
            "Michael Kofman — CEO Digital Invest Inc. і член ради директорів. "
            "Заснував 9 Net Avenue Inc. (пікова капіталізація $19,5 млрд) і очолює "
            "Digital Invest у precision medicine. Досвід у govtech і defense, XIBI Group Inc., "
            "DataPeer Inc., Biotechnology Group Inc. Співпраця з Harvard Medical School "
            "та Stanford Biomath. Автор технічних робіт; патент HDTV, придбаний Sony. "
            "У 2026 році заснував AGRON Inc. для aerial-ground robotics і maritime intelligence. "
            "Освіта: доктор технічних наук (2009), Ph.D. з IT (2004), "
            "Ukrainian State Marine Technical University."
        ),
    },
    "es": {
        "bioMedium": (
            "Michael Kofman es CEO de Digital Invest Inc. y miembro de su consejo. "
            "Emprendedor, miembro de juntas y asesor; ha fundado empresas en EE. UU. y Europa "
            "en infraestructura de datos, salud digital y robótica. "
            "Su trabajo abarca estrategia tecnológica, seguridad, investigación e inversión."
        ),
        "bioLong": (
            "Michael Kofman es CEO de Digital Invest Inc. y miembro de su consejo. "
            "Fundó 9 Net Avenue Inc., adquirida con una valoración pico de $19,5 mil millones, "
            "y dirige Digital Invest en medicina de precisión. Ha liderado estrategia tecnológica "
            "para programas gubernamentales y de defensa, fundó XIBI Group Inc. y DataPeer Inc., "
            "y dirigió Biotechnology Group Inc. Colaboró con Harvard Medical School y Stanford "
            "Biomath. Autor de trabajos técnicos; patente HDTV adquirida por Sony. "
            "En 2026 fundó AGRON Inc. para robótica aero-terrestre e inteligencia marítima."
        ),
    },
    "de": {
        "bioMedium": (
            "Michael Kofman ist CEO von Digital Invest Inc. und Vorstandsmitglied. "
            "Als Unternehmer, Board-Mitglied und Berater hat er Unternehmen in den USA und "
            "Europa in Dateninfrastruktur, Digital Health und Robotik gegründet. "
            "Seine Arbeit umfasst Technologiestrategie, Sicherheit, Forschung und Investment."
        ),
        "bioLong": (
            "Michael Kofman ist CEO von Digital Invest Inc. und Vorstandsmitglied. "
            "Er gründete 9 Net Avenue Inc. (Spitzenbewertung $19,5 Mrd.) und leitet "
            "Digital Invest in der Präzisionsmedizin. Erfahrung in GovTech und Defense, "
            "XIBI Group Inc., DataPeer Inc., Biotechnology Group Inc. Zusammenarbeit mit "
            "Harvard Medical School und Stanford Biomath. Autor technischer Arbeiten; "
            "HDTV-Patent von Sony übernommen. 2026 gründete er AGRON Inc. für "
            "Luft-Boden-Robotik und maritime Intelligence."
        ),
    },
    "fr": {
        "bioMedium": (
            "Michael Kofman est PDG de Digital Invest Inc. et membre de son conseil. "
            "Entrepreneur, administrateur et conseiller, il a fondé des entreprises aux "
            "États-Unis et en Europe dans l'infrastructure de données, la santé numérique "
            "et la robotique. Son travail couvre stratégie technologique, sécurité, "
            "recherche et investissement."
        ),
        "bioLong": (
            "Michael Kofman est PDG de Digital Invest Inc. et membre de son conseil. "
            "Il a fondé 9 Net Avenue Inc. (valorisation pic de 19,5 milliards $) et dirige "
            "Digital Invest en médecine de précision. Expérience en govtech et défense, "
            "XIBI Group Inc., DataPeer Inc., Biotechnology Group Inc. Collaboration avec "
            "Harvard Medical School et Stanford Biomath. Auteur de travaux techniques; "
            "brevet HDTV acquis par Sony. En 2026, il a fondé AGRON Inc. pour la robotique "
            "aéro-terrestre et le renseignement maritime."
        ),
    },
}


def parse_js_const(path: Path) -> dict:
    raw = path.read_text(encoding="utf-8")
    start, end = raw.find("{"), raw.rfind("}")
    return json.loads(raw[start : end + 1])


def write_js_const(path: Path, var_name: str, data: dict) -> None:
    path.write_text(
        f"const {var_name} = {json.dumps(data, ensure_ascii=False, indent=2)};\n",
        encoding="utf-8",
    )


def deep_update(target: dict, patch: dict) -> None:
    for key, value in patch.items():
        if isinstance(value, dict) and isinstance(target.get(key), dict):
            deep_update(target[key], value)
        else:
            target[key] = value


def apply_translations(translations: dict) -> None:
    old_boilerplate = (
        "Michael Kofman is a technological visionary renowned for his dynamic approach "
        "to understanding the ever-evolving needs of today's complex market. "
        "An entrepreneur, board member, and advisor for both public and private companies, "
        "he has successfully established several companies in the United States and Europe."
    )

    for lang in LANGS:
        t = translations.setdefault(lang, {})
        if lang in HOME:
            home = t.setdefault("home", {})
            deep_update(home, HOME[lang])
            if lang in QUOTE1:
                home["quote1text"] = QUOTE1[lang]
        if lang in CONSULTING:
            deep_update(t.setdefault("consulting", {}), CONSULTING[lang])
        if lang in CONSULTING_TITLES:
            deep_update(t.setdefault("consulting", {}), CONSULTING_TITLES[lang])
        if lang in INSIGHTS:
            deep_update(t.setdefault("insights", {}), INSIGHTS[lang])
        if lang in ABOUT:
            deep_update(t.setdefault("about", {}), ABOUT[lang])
        if lang in VENTURES:
            deep_update(t.setdefault("ventures", {}), VENTURES[lang])
        if lang in RECOGNITION:
            deep_update(t.setdefault("recognition", {}), RECOGNITION[lang])
        if lang in FOOTER:
            t.setdefault("footer", {})["desc"] = FOOTER[lang]
        if lang in MEDIA_KIT:
            deep_update(t.setdefault("mediaKit", {}), MEDIA_KIT[lang])
        if lang in META_HOME:
            t.setdefault("meta", {}).setdefault("home", {})["description"] = META_HOME[lang]
        if lang in META_ABOUT:
            t.setdefault("meta", {}).setdefault("about", {})["description"] = META_ABOUT[lang]

        # Replace leftover English boilerplate in aboutLead1
        home = t.get("home", {})
        if home.get("aboutLead1") == old_boilerplate and lang in HOME:
            home["aboutLead1"] = HOME[lang]["aboutLead1"]

    # EN-specific meta/footer
    en = translations["en"]
    en.setdefault("meta", {}).setdefault("home", {})["description"] = (
        "Official site of Michael Kofman — CEO, founder, and board advisor "
        "in technology and digital health."
    )
    en["meta"].setdefault("about", {})["description"] = (
        "Biography of Michael Kofman — CEO of Digital Invest Inc., founder of AGRON Inc."
    )
    en["footer"]["desc"] = FOOTER["en"]


def apply_page_content(page_content: dict) -> None:
    for lang in LANGS:
        block = page_content.setdefault(lang, {})
        about = block.setdefault("about", {})
        about["bioP1"] = BIO_P1[lang]

        # Fix mixed RU bio if old partial translation remains
        if BOILERPLATE_BIO in about.get("bioP1", ""):
            about["bioP1"] = BIO_P1[lang]


def main() -> None:
    trans_path = ROOT / "js" / "translations.js"
    content_path = ROOT / "js" / "page-content.js"

    translations = parse_js_const(trans_path)
    page_content = parse_js_const(content_path)

    apply_translations(translations)
    apply_page_content(page_content)

    write_js_const(trans_path, "TRANSLATIONS", translations)
    write_js_const(content_path, "PAGE_CONTENT", page_content)
    print("Copy audit applied to translations.js and page-content.js")


if __name__ == "__main__":
    main()
