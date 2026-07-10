#!/usr/bin/env python3
"""Patch translations.js with localized home.exp*desc and meta.*.description for non-en langs."""
import json
import os
import re

PATCHES = {
    "es": {
        "home": {
            "exp1desc": "Fundó y escaló múltiples empresas desde su inicio hasta la salida a bolsa, logrando un crecimiento financiero constante y presencia global en los sectores de tecnología y salud.",
            "exp2desc": "Diseñó comunicaciones seguras, motores de analítica predictiva y plataformas de integración de datos a nivel nacional para los sectores gubernamental, militar y de telecomunicaciones.",
            "exp3desc": "Lidera la transformación de la medicina mediante IA, ML y tecnologías de ADN. Colaboró con Harvard Medical School y Stanford Biomath en informes genéticos.",
            "exp4desc": "Participa en juntas directivas y asesora a empresas públicas y privadas sobre dirección estratégica, gobierno corporativo e iniciativas de crecimiento impulsadas por la tecnología.",
        },
        "meta": {
            "home": {"description": "Sitio oficial de Michael Kofman — CEO galardonado, fundador y tecnólogo estratégico."},
            "about": {"description": "Biografía de Michael Kofman — CEO de Digital Invest Inc. — visionario tecnológico y emprendedor galardonado."},
            "ventures": {"description": "Empresas fundadas y dirigidas por Michael Kofman — desde Digital Invest Inc. hasta 9 Net Avenue Inc. — construyendo negocios transformadores en tecnología y salud."},
            "career": {"description": "Línea de tiempo profesional de Michael Kofman — desde ingeniería satelital hasta CEO de empresas globales de tecnología y salud."},
            "recognition": {"description": "Premios, honores y reconocimientos de Michael Kofman — Emprendedor del Año, Who's Who, patentes y distinciones del sector."},
            "contact": {"description": "Contacte a Michael Kofman — CEO de Digital Invest Inc. Para conferencias, roles de asesoría y consultas comerciales."},
        },
    },
    "de": {
        "home": {
            "exp1desc": "Gründete und skalierte mehrere Unternehmen vom Start bis zum Börsengang und erzielte kontinuierliches Finanzwachstum sowie globale Präsenz in Technologie und Gesundheitswesen.",
            "exp2desc": "Entwarf sichere Kommunikationssysteme, prädiktive Analyse-Engines und Datenintegrationsplattformen auf nationaler Ebene für Regierung, Militär und Telekommunikation.",
            "exp3desc": "Führt die Transformation der Medizin durch KI, ML und DNA-Technologien an. Arbeitete mit Harvard Medical School und Stanford Biomath an genetischen Berichten.",
            "exp4desc": "Sitzt in Aufsichtsräten und berät öffentliche und private Unternehmen zu strategischer Ausrichtung, Corporate Governance und technologiegetriebenem Wachstum.",
        },
        "meta": {
            "home": {"description": "Offizielle Website von Michael Kofman — preisgekrönter CEO, Gründer und strategischer Technologe."},
            "about": {"description": "Biografie von Michael Kofman — CEO von Digital Invest Inc. — Technologievisionär und preisgekrönter Unternehmer."},
            "ventures": {"description": "Von Michael Kofman gegründete und geführte Unternehmen — von Digital Invest Inc. bis 9 Net Avenue Inc. — transformative Geschäfte in Technologie und Gesundheitswesen."},
            "career": {"description": "Beruflicher Werdegang von Michael Kofman — von Satelliteningenieurwesen bis CEO globaler Technologie- und Gesundheitsunternehmen."},
            "recognition": {"description": "Auszeichnungen und Ehrungen für Michael Kofman — Unternehmer des Jahres, Who's Who, Patente und Branchenanerkennungen."},
            "contact": {"description": "Kontakt zu Michael Kofman — CEO von Digital Invest Inc. Für Vorträge, Beratungsmandate und geschäftliche Anfragen."},
        },
    },
    "fr": {
        "home": {
            "exp1desc": "A fondé et développé plusieurs entreprises de la création à l'introduction en bourse, assurant une croissance financière constante et une présence mondiale dans la technologie et la santé.",
            "exp2desc": "A conçu des communications sécurisées, des moteurs d'analyse prédictive et des plateformes d'intégration de données à l'échelle nationale pour les secteurs gouvernemental, militaire et télécom.",
            "exp3desc": "Dirige la transformation de la médecine grâce à l'IA, au ML et aux technologies ADN. A collaboré avec Harvard Medical School et Stanford Biomath sur les rapports génétiques.",
            "exp4desc": "Siège au conseil d'administration et conseille des entreprises publiques et privées sur l'orientation stratégique, la gouvernance et la croissance portée par la technologie.",
        },
        "meta": {
            "home": {"description": "Site officiel de Michael Kofman — PDG primé, fondateur et technologue stratégique."},
            "about": {"description": "Biographie de Michael Kofman — PDG de Digital Invest Inc. — visionnaire technologique et entrepreneur primé."},
            "ventures": {"description": "Entreprises fondées et dirigées par Michael Kofman — de Digital Invest Inc. à 9 Net Avenue Inc. — bâtissant des entreprises transformatrices en technologie et santé."},
            "career": {"description": "Parcours professionnel de Michael Kofman — de l'ingénierie satellitaire au poste de PDG d'entreprises technologiques et de santé mondiales."},
            "recognition": {"description": "Prix, distinctions et reconnaissances de Michael Kofman — Entrepreneur de l'année, Who's Who, brevets et distinctions sectorielles."},
            "contact": {"description": "Contacter Michael Kofman — PDG de Digital Invest Inc. Pour conférences, mandats de conseil et demandes commerciales."},
        },
    },
    "ru": {
        "home": {
            "exp1desc": "Основал и масштабировал несколько компаний — от старта до IPO, обеспечив устойчивый финансовый рост и глобальное присутствие в сферах технологий и здравоохранения.",
            "exp2desc": "Разрабатывал защищённые коммуникации, системы предиктивной аналитики и платформы интеграции данных национального уровня для государственного, военного и телекоммуникационного секторов.",
            "exp3desc": "Возглавляет трансформацию медицины с помощью ИИ, ML и ДНК-технологий. Сотрудничал с Harvard Medical School и Stanford Biomath над генетическими отчётами.",
            "exp4desc": "Входит в советы директоров и консультирует публичные и частные компании по стратегическому развитию, корпоративному управлению и технологическому росту.",
        },
        "meta": {
            "home": {"description": "Официальный сайт Михаила Кофмана — отмеченный наградами CEO, основатель и стратегический технолог."},
            "about": {"description": "Биография Михаила Кофмана — CEO Digital Invest Inc. — технологический визионер и предприниматель, отмеченный наградами."},
            "ventures": {"description": "Компании, основанные и возглавляемые Михаилом Кофманом — от Digital Invest Inc. до 9 Net Avenue Inc. — трансформирующие бизнес в технологиях и здравоохранении."},
            "career": {"description": "Профессиональная карьера Михаила Кофмана — от спутниковой инженерии до CEO глобальных технологических и медицинских компаний."},
            "recognition": {"description": "Награды и признание Михаила Кофмана — Предприниматель года, Who's Who, патенты и отраслевые награды."},
            "contact": {"description": "Связаться с Михаилом Кофманом — CEO Digital Invest Inc. Для выступлений, консультаций и деловых запросов."},
        },
    },
    "uk": {
        "home": {
            "exp1desc": "Заснував і масштабував кілька компаній — від старту до IPO, забезпечивши стійке фінансове зростання та глобальну присутність у сферах технологій і охорони здоров'я.",
            "exp2desc": "Проєктував захищені комунікації, системи предиктивної аналітики та платформи інтеграції даних національного рівня для державного, військового та телекомунікаційного секторів.",
            "exp3desc": "Очолює трансформацію медицини за допомогою ШІ, ML і ДНК-технологій. Співпрацював із Harvard Medical School та Stanford Biomath над генетичними звітами.",
            "exp4desc": "У входить до рад директорів і консультує публічні та приватні компанії щодо стратегічного розвитку, корпоративного управління та технологічного зростання.",
        },
        "meta": {
            "home": {"description": "Офіційний сайт Михайла Кофмана — відзначений нагородами CEO, засновник і стратегічний технолог."},
            "about": {"description": "Біографія Михайла Кофмана — CEO Digital Invest Inc. — технологічний візіонер і підприємець, відзначений нагородами."},
            "ventures": {"description": "Компанії, засновані та очолювані Михайлом Кофманом — від Digital Invest Inc. до 9 Net Avenue Inc. — трансформуючі бізнес у технологіях і охороні здоров'я."},
            "career": {"description": "Професійна кар'єра Михайла Кофмана — від супутникової інженерії до CEO глобальних технологічних і медичних компаній."},
            "recognition": {"description": "Нагороди та визнання Михайла Кофмана — Підприємець року, Who's Who, патенти та галузеві відзнаки."},
            "contact": {"description": "Зв'язатися з Михайлом Кофманом — CEO Digital Invest Inc. Для виступів, консультацій і ділових запитів."},
        },
    },
    "zh": {
        "home": {
            "exp1desc": "从创立到成功上市，创办并扩展了多家公司，在科技与医疗领域实现了持续财务增长和全球布局。",
            "exp2desc": "为政府、军事和电信领域设计安全通信、预测分析引擎和国家级数据集成平台。",
            "exp3desc": "通过人工智能、机器学习和DNA技术引领医学变革。曾与哈佛医学院和Stanford Biomath合作开展基因报告项目。",
            "exp4desc": "担任董事会成员，为上市和非上市公司提供战略方向、公司治理和技术驱动增长方面的咨询。",
        },
        "meta": {
            "home": {"description": "Michael Kofman官方网站——屡获殊荣的CEO、创始人和战略技术专家。"},
            "about": {"description": "Michael Kofman传记——Digital Invest Inc. CEO——技术愿景家和屡获殊荣的企业家。"},
            "ventures": {"description": "Michael Kofman创办和领导的企业——从Digital Invest Inc.到9 Net Avenue Inc.——在科技和医疗领域构建变革性业务。"},
            "career": {"description": "Michael Kofman职业历程——从卫星工程到全球科技和医疗公司CEO。"},
            "recognition": {"description": "Michael Kofman获得的奖项与荣誉——年度企业家、Who's Who、专利和行业殊荣。"},
            "contact": {"description": "联系Michael Kofman——Digital Invest Inc. CEO。咨询顾问职位、演讲邀约和商业合作。"},
        },
    },
    "ar": {
        "home": {
            "exp1desc": "أسس وطوّر عدة شركات من البداية حتى الاكتتاب العام، محققاً نمواً مالياً مستداماً وحضوراً عالمياً في قطاعي التكنولوجيا والرعاية الصحية.",
            "exp2desc": "صمم اتصالات آمنة ومحركات تحليلات تنبؤية ومنصات تكامل بيانات على المستوى الوطني للقطاعات الحكومية والعسكرية والاتصالات.",
            "exp3desc": "يقود تحويل الطب من خلال الذكاء الاصطناعي والتعلم الآلي وتقنيات الحمض النووي. تعاون مع Harvard Medical School وStanford Biomath في التقارير الجينية.",
            "exp4desc": "يشغل مقاعد في مجالس الإدارة ويقدم المشورة للشركات العامة والخاصة بشأن التوجه الاستراتيجي والحوكمة ومبادرات النمو التقني.",
        },
        "meta": {
            "home": {"description": "الموقع الرسمي لمايكل كوفمان — الرئيس التنفيذي الحائز على جوائز والمؤسس والتقني الاستراتيجي."},
            "about": {"description": "سيرة مايكل كوفمان — الرئيس التنفيذي لـ Digital Invest Inc. — رؤيوي تقني ورائد أعمال حائز على جوائز."},
            "ventures": {"description": "الشركات التي أسسها مايكل كوفمان وقادها — من Digital Invest Inc. إلى 9 Net Avenue Inc. — لبناء أعمال تحويلية في التكنولوجيا والرعاية الصحية."},
            "career": {"description": "المسار المهني لمايكل كوفمان — من هندسة الأقمار الصناعية إلى رئاسة شركات التكنولوجيا والرعاية الصحية العالمية."},
            "recognition": {"description": "الجوائز والتكريمات لمايكل كوفمان — رائد العام، Who's Who، براءات الاختراع وتقدير القطاع."},
            "contact": {"description": "التواصل مع مايكل كوفمان — الرئيس التنفيذي لـ Digital Invest Inc. للاستشارات والمحاضرات والاستفسارات التجارية."},
        },
    },
    "he": {
        "home": {
            "exp1desc": "ייסד והרחיב מספר חברות מהקמתן ועד הנפקה מוצלחת, תוך צמיחה פיננסית עקבית ונוכחות גלובלית בתחומי הטכנולוגיה והבריאות.",
            "exp2desc": "תכנן תקשורת מאובטחת, מנועי אנליטיקה חיזויית ופלטפורמות אינטגרציית נתונים ברמה לאומית למגזרים ממשלתיים, צבאיים וטלקום.",
            "exp3desc": "מוביל את שינוי הרפואה באמצעות בינה מלאכותית, למידת מכונה וטכנולוגיות DNA. שיתף פעולה עם Harvard Medical School ו-Stanford Biomath בדיווח גנטי.",
            "exp4desc": "חבר בדירקטוריונים ומייעץ לחברות ציבוריות ופרטיות בנושאי כיוון אסטרטגי, ממשל תאגידי ויוזמות צמיחה מונחות טכנולוגיה.",
        },
        "meta": {
            "home": {"description": "האתר הרשמי של מייקל קופמן — מנכ\"ל זוכה פרסים, מייסד וטכנולוג אסטרטגי."},
            "about": {"description": "ביוגרפיה של מייקל קופמן — מנכ\"ל Digital Invest Inc. — חזון טכנולוגי ויזם זוכה פרסים."},
            "ventures": {"description": "חברות שייסד וניהל מייקל קופמן — מ-Digital Invest Inc. ועד 9 Net Avenue Inc. — בניית עסקים משני מציאות בטכנולוגיה ובריאות."},
            "career": {"description": "מסלול הקריירה של מייקל קופמן — מהנדסות לוויינים ועד מנכ\"ל חברות טכנולוגיה ובריאות גלובליות."},
            "recognition": {"description": "פרסים והוקרות למייקל קופמן — יזם השנה, Who's Who, פטנטים והוקרות תעשייתיות."},
            "contact": {"description": "יצירת קשר עם מייקל קופמן — מנכ\"ל Digital Invest Inc. לייעוץ, הרצאות ופניות עסקיות."},
        },
    },
}


def main():
    path = os.path.join(os.path.dirname(__file__), "..", "js", "translations.js")
    with open(path, encoding="utf-8") as f:
        content = f.read()

  # Parse JS object (strip const wrapper)
    match = re.search(r"const TRANSLATIONS = (\{.*\});\s*$", content, re.DOTALL)
    if not match:
        raise SystemExit("Could not parse translations.js")
    data = json.loads(match.group(1))

    for lang, sections in PATCHES.items():
        for section, keys in sections.items():
            if section not in data[lang]:
                data[lang][section] = {}
            for key, val in keys.items():
                if section == "meta":
                    if key not in data[lang]["meta"]:
                        data[lang]["meta"][key] = {}
                    data[lang]["meta"][key]["description"] = val["description"]
                else:
                    data[lang][section][key] = val

    out = "const TRANSLATIONS = " + json.dumps(data, ensure_ascii=False, indent=2) + ";\n"
    with open(path, "w", encoding="utf-8") as f:
        f.write(out)
    print(f"Patched {path}")


if __name__ == "__main__":
    main()
