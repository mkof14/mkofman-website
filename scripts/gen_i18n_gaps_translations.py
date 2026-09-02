#!/usr/bin/env python3
"""Generate scripts/i18n_gaps_translations.json from embedded translation data."""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from i18n_remaining_data import REMAINING
from i18n_large_sections import LARGE
from i18n_ru_uk_fixes import FIXES

OUTPUT = Path(__file__).resolve().parent / "i18n_gaps_translations.json"
LANGS = ("es", "de", "fr", "ru", "uk", "zh", "ar", "he")


def t(section: dict) -> dict:
    return {lang: section[lang] for lang in LANGS}


# fmt: off
DATA = {
"about": t({
"es": {
    "archiveEyebrow": "Del archivo",
    "archiveLead": "Material auténtico sobre creación de empresas, infraestructura y liderazgo.",
    "contactLabel": "Contacto",
    "educationVal": "Doctor en Ciencias Técnicas\nPh.D. en Tecnologías de la Información\nMaestrías — Electrónica, Sistemas Satelitales Digitales y Economía",
    "languagesVal": "Inglés, ruso, ucraniano",
    "locationVal": "Charlotte, North Carolina",
    "photo9netCaption": "Fundador y CEO — empresa de hosting e infraestructura de internet, adquirida por Concentric Networks en 2000.",
    "photo9netTitle": "9 Net Avenue",
    "photoServerTitle": "Infraestructura de datos",
    "photoTodayCaption": "Digital Invest Inc., AGRON Inc. y trabajo de asesoría.",
    "photoTodayTitle": "Hoy",
    "recordLink": "The Record →",
    "roleVal": "CEO · Digital Invest Inc. · Fundador · AGRON Inc.",
    "secBackgroundTitle": "Formación",
    "secBusinessTitle": "Negocios",
    "secCurrentTitle": "Trabajo actual",
    "secIntroTitle": "Introducción",
    "universityVal": "Universidad Técnica Naval Estatal de Ucrania",
},
"de": {
    "archiveEyebrow": "Aus dem Archiv",
    "archiveLead": "Authentisches Material aus Unternehmensaufbau, Infrastruktur und Führung.",
    "contactLabel": "Kontakt",
    "educationVal": "Doctor of Technical Sciences\nPh.D. in Information Technology\nMasterabschlüsse — Elektronik, Digitale Satellitensysteme und Wirtschaft",
    "languagesVal": "Englisch, Russisch, Ukrainisch",
    "locationVal": "Charlotte, North Carolina",
    "photo9netCaption": "Gründer & CEO — Hosting- und Internet-Infrastrukturunternehmen, 2000 von Concentric Networks übernommen.",
    "photo9netTitle": "9 Net Avenue",
    "photoServerTitle": "Dateninfrastruktur",
    "photoTodayCaption": "Digital Invest Inc., AGRON Inc. und Advisory-Arbeit.",
    "photoTodayTitle": "Heute",
    "recordLink": "The Record →",
    "roleVal": "CEO · Digital Invest Inc. · Gründer · AGRON Inc.",
    "secBackgroundTitle": "Hintergrund",
    "secBusinessTitle": "Business",
    "secCurrentTitle": "Aktuelle Arbeit",
    "secIntroTitle": "Einführung",
    "universityVal": "Staatliche Marine-Technische Universität der Ukraine",
},
"fr": {
    "archiveEyebrow": "Des archives",
    "archiveLead": "Documents authentiques sur la création d'entreprises, l'infrastructure et le leadership.",
    "contactLabel": "Contact",
    "educationVal": "Doctor of Technical Sciences\nPh.D. in Information Technology\nMasters — Électronique, Systèmes satellitaires numériques et Économie",
    "languagesVal": "Anglais, russe, ukrainien",
    "locationVal": "Charlotte, North Carolina",
    "photo9netCaption": "Fondateur et CEO — entreprise d'hébergement et d'infrastructure internet, acquise par Concentric Networks en 2000.",
    "photo9netTitle": "9 Net Avenue",
    "photoServerTitle": "Infrastructure de données",
    "photoTodayCaption": "Digital Invest Inc., AGRON Inc. et travail de conseil.",
    "photoTodayTitle": "Aujourd'hui",
    "recordLink": "The Record →",
    "roleVal": "CEO · Digital Invest Inc. · Fondateur · AGRON Inc.",
    "secBackgroundTitle": "Parcours",
    "secBusinessTitle": "Business",
    "secCurrentTitle": "Travail actuel",
    "secIntroTitle": "Introduction",
    "universityVal": "Université technique navale d'État d'Ukraine",
},
"ru": {
    "archiveEyebrow": "Из архива",
    "archiveLead": "Подлинные материалы о создании компаний, инфраструктуре и лидерстве.",
    "contactLabel": "Контакты",
    "educationVal": "Доктор технических наук\nPh.D. в области информационных технологий\nМагистерские степени — электроника, цифровые спутниковые системы и экономика",
    "languagesVal": "Английский, русский, украинский",
    "locationVal": "Charlotte, North Carolina",
    "photo9netCaption": "Основатель и CEO — компания хостинга и интернет-инфраструктуры, приобретённая Concentric Networks в 2000 году.",
    "photo9netTitle": "9 Net Avenue",
    "photoServerTitle": "Инфраструктура данных",
    "photoTodayCaption": "Digital Invest Inc., AGRON Inc. и advisory-работа.",
    "photoTodayTitle": "Сегодня",
    "recordLink": "The Record →",
    "roleVal": "CEO · Digital Invest Inc. · Основатель · AGRON Inc.",
    "secBackgroundTitle": "Образование и background",
    "secBusinessTitle": "Бизнес",
    "secCurrentTitle": "Текущая работа",
    "secIntroTitle": "Введение",
    "universityVal": "Украинский государственный морской технический университет",
},
"uk": {
    "archiveEyebrow": "З архіву",
    "archiveLead": "Автентичні матеріали про створення компаній, інфраструктуру та лідерство.",
    "contactLabel": "Контакти",
    "educationVal": "Доктор технічних наук\nPh.D. з інформаційних технологій\nМагістерські ступені — електроніка, цифрові супутникові системи та економіка",
    "languagesVal": "Англійська, російська, українська",
    "locationVal": "Charlotte, North Carolina",
    "photo9netCaption": "Засновник і CEO — компанія хостингу та інтернет-інфраструктури, придбана Concentric Networks у 2000 році.",
    "photo9netTitle": "9 Net Avenue",
    "photoServerTitle": "Інфраструктура даних",
    "photoTodayCaption": "Digital Invest Inc., AGRON Inc. та advisory-робота.",
    "photoTodayTitle": "Сьогодні",
    "recordLink": "The Record →",
    "roleVal": "CEO · Digital Invest Inc. · Засновник · AGRON Inc.",
    "secBackgroundTitle": "Освіта та background",
    "secBusinessTitle": "Бізнес",
    "secCurrentTitle": "Поточна робота",
    "secIntroTitle": "Вступ",
    "universityVal": "Український державний морський технічний університет",
},
"zh": {
    "archiveEyebrow": "档案精选",
    "archiveLead": "来自企业创建、基础设施和领导力的真实资料。",
    "contactLabel": "联系",
    "educationVal": "技术科学博士\n信息技术博士\n硕士学位——电子学、数字卫星系统和经济学",
    "languagesVal": "英语、俄语、乌克兰语",
    "locationVal": "Charlotte, North Carolina",
    "photo9netCaption": "创始人兼CEO——托管与互联网基础设施公司，2000年被Concentric Networks收购。",
    "photo9netTitle": "9 Net Avenue",
    "photoServerTitle": "数据基础设施",
    "photoTodayCaption": "Digital Invest Inc.、AGRON Inc.及顾问工作。",
    "photoTodayTitle": "今日",
    "recordLink": "The Record →",
    "roleVal": "CEO · Digital Invest Inc. · 创始人 · AGRON Inc.",
    "secBackgroundTitle": "背景",
    "secBusinessTitle": "商业",
    "secCurrentTitle": "当前工作",
    "secIntroTitle": "简介",
    "universityVal": "乌克兰国立海洋技术大学",
},
"ar": {
    "archiveEyebrow": "من الأرشيف",
    "archiveLead": "مواد أصيلة عن بناء الشركات والبنية التحتية والقيادة.",
    "contactLabel": "تواصل",
    "educationVal": "دكتوراه في العلوم التقنية\nPh.D. في تكنولوجيا المعلومات\nدرجات ماجستير — إلكترونيات، أنظمة الأقمار الصناعية الرقمية والاقتصاد",
    "languagesVal": "الإنجليزية، الروسية، الأوكرانية",
    "locationVal": "Charlotte, North Carolina",
    "photo9netCaption": "المؤسس والرئيس التنفيذي — شركة استضافة وبنية تحتية للإنترنت، استحوذت عليها Concentric Networks عام 2000.",
    "photo9netTitle": "9 Net Avenue",
    "photoServerTitle": "البنية التحتية للبيانات",
    "photoTodayCaption": "Digital Invest Inc. وAGRON Inc. وعمل استشاري.",
    "photoTodayTitle": "اليوم",
    "recordLink": "The Record →",
    "roleVal": "CEO · Digital Invest Inc. · المؤسس · AGRON Inc.",
    "secBackgroundTitle": "الخلفية",
    "secBusinessTitle": "الأعمال",
    "secCurrentTitle": "العمل الحالي",
    "secIntroTitle": "مقدمة",
    "universityVal": "الجامعة التقنية البحرية الحكومية الأوكرانية",
},
"he": {
    "archiveEyebrow": "מהארכיון",
    "archiveLead": "חומר אותנטי מבניית חברות, תשתיות ומנהיגות.",
    "contactLabel": "יצירת קשר",
    "educationVal": "דוקטור למדעי הטכניקה\nPh.D. בטכנולוגיות מידע\nתארים שני — אלקטרוניקה, מערכות לוויין דיגיטליות וכלכלה",
    "languagesVal": "אנגלית, רוסית, אוקראינית",
    "locationVal": "Charlotte, North Carolina",
    "photo9netCaption": "מייסד ו-CEO — חברת אירוח ותשתית אינטרנט, נרכשה על ידי Concentric Networks ב-2000.",
    "photo9netTitle": "9 Net Avenue",
    "photoServerTitle": "תשתית נתונים",
    "photoTodayCaption": "Digital Invest Inc., AGRON Inc. ועבודת ייעוץ.",
    "photoTodayTitle": "היום",
    "recordLink": "The Record →",
    "roleVal": "CEO · Digital Invest Inc. · מייסד · AGRON Inc.",
    "secBackgroundTitle": "רקע",
    "secBusinessTitle": "עסקים",
    "secCurrentTitle": "עבודה נוכחית",
    "secIntroTitle": "הקדמה",
    "universityVal": "האוניברסיטה הטכנית הימית הממלכתית של אוקראינה",
},
}),
"articles": t({
"es": {"article1date": "Perspectiva ejecutiva", "article1p3": "En 1996 fundé 9 Net Avenue Inc., empresa de hosting e infraestructura de internet. En 2000 fue adquirida por Concentric Networks (NASDAQ: CNTX) y posteriormente formó parte de XO Communications (NASDAQ: XOXO).", "article2date": "Salud digital"},
"de": {"article1date": "Executive Perspective", "article1p3": "1996 gründete ich 9 Net Avenue Inc., ein Hosting- und Internet-Infrastrukturunternehmen. 2000 wurde es von Concentric Networks (NASDAQ: CNTX) übernommen und später Teil von XO Communications (NASDAQ: XOXO).", "article2date": "Digital Health"},
"fr": {"article1date": "Perspective exécutive", "article1p3": "En 1996, j'ai fondé 9 Net Avenue Inc., entreprise d'hébergement et d'infrastructure internet. En 2000, elle a été acquise par Concentric Networks (NASDAQ: CNTX), puis est devenue partie de XO Communications (NASDAQ: XOXO).", "article2date": "Santé numérique"},
"ru": {"article1date": "Executive Perspective", "article1p3": "В 1996 году я основал 9 Net Avenue Inc. — компанию хостинга и интернет-инфраструктуры. В 2000 году она была приобретена Concentric Networks (NASDAQ: CNTX), а затем стала частью XO Communications (NASDAQ: XOXO).", "article2date": "Digital Health"},
"uk": {"article1date": "Executive Perspective", "article1p3": "У 1996 році я заснував 9 Net Avenue Inc. — компанію хостингу та інтернет-інфраструктури. У 2000 році її придбала Concentric Networks (NASDAQ: CNTX), а згодом вона стала частиною XO Communications (NASDAQ: XOXO).", "article2date": "Digital Health"},
"zh": {"article1date": "高管视角", "article1p3": "1996年，我创立了9 Net Avenue Inc.，一家托管与互联网基础设施公司。2000年被Concentric Networks（NASDAQ: CNTX）收购，随后成为XO Communications（NASDAQ: XOXO）的一部分。", "article2date": "数字健康"},
"ar": {"article1date": "منظور تنفيذي", "article1p3": "في عام 1996، أسست 9 Net Avenue Inc.، شركة استضافة وبنية تحتية للإنترنت. في عام 2000 استحوذت عليها Concentric Networks (NASDAQ: CNTX) وأصبحت لاحقاً جزءاً من XO Communications (NASDAQ: XOXO).", "article2date": "الصحة الرقمية"},
"he": {"article1date": "פרספקטיבה מנהלית", "article1p3": "ב-1996 ייסדתי את 9 Net Avenue Inc., חברת אירוח ותשתית אינטרנט. ב-2000 נרכשה על ידי Concentric Networks (NASDAQ: CNTX) והפכה לאחר מכן לחלק מ-XO Communications (NASDAQ: XOXO).", "article2date": "בריאות דיגיטלית"},
}),
"board": t({
"es": {"body": "Abierto a conversaciones de asesoría estratégica con organizaciones de tecnología, salud e infraestructura — basándome en experiencia operativa directa en creación de empresas, estrategia tecnológica y ejecución en etapas de crecimiento.", "contactLink": "Para consultas de asesoría", "eyebrow": "Asesoría", "title": "Asesoría"},
"de": {"body": "Offen für strategische Advisory-Gespräche mit Technologie-, Gesundheits- und Infrastrukturorganisationen — auf Basis direkter Operating-Erfahrung in Unternehmensaufbau, Technologiestrategie und Wachstumsphasen.", "contactLink": "Für Advisory-Anfragen", "eyebrow": "Advisory", "title": "Advisory"},
"fr": {"body": "Ouvert aux conversations de conseil stratégique avec des organisations technologiques, de santé et d'infrastructure — s'appuyant sur une expérience opérationnelle directe en création d'entreprises, stratégie technologique et exécution en phase de croissance.", "contactLink": "Pour les demandes de conseil", "eyebrow": "Conseil", "title": "Conseil"},
"ru": {"body": "Открыт к стратегическим advisory-диалогам с технологическими, медицинскими и инфраструктурными организациями — на основе прямого operating-опыта в создании компаний, технологической стратегии и росте.", "contactLink": "По вопросам advisory", "eyebrow": "Advisory", "title": "Advisory"},
"uk": {"body": "Відкритий до стратегічних advisory-діалогів із технологічними, медичними та інфраструктурними організаціями — на основі прямого operating-досвіду у створенні компаній, технологічній стратегії та зростанні.", "contactLink": "Щодо advisory-запитів", "eyebrow": "Advisory", "title": "Advisory"},
"zh": {"body": "欢迎与科技、医疗和基础设施机构进行战略顾问对话——基于企业创建、技术战略和成长期执行的一手运营经验。", "contactLink": "顾问咨询", "eyebrow": "顾问", "title": "顾问"},
"ar": {"body": "منفتح على محادثات استشارية استراتيجية مع منظمات التكنولوجيا والرعاية الصحية والبنية التحتية — استناداً إلى خبرة تشغيلية مباشرة في بناء الشركات واستراتيجية التكنولوجيا والتنفيذ في مراحل النمو.", "contactLink": "للاستفسارات الاستشارية", "eyebrow": "استشارات", "title": "استشارات"},
"he": {"body": "פתוח לשיחות ייעוץ אסטרטגי עם ארגוני טכנולוגיה, בריאות ותשתיות — על בסיס ניסיון תפעולי ישיר בבניית חברות, אסטרטגיה טכנולוגית וביצוע בשלבי צמיחה.", "contactLink": "לפניות ייעוץ", "eyebrow": "ייעוץ", "title": "ייעוץ"},
}),
"deck": t({
"es": {"contact": "Discusión confidencial: contacte a Michael Kofman en mkofman.com", "title": "Michael Kofman"},
"de": {"contact": "Vertrauliches Gespräch: Michael Kofman über mkofman.com kontaktieren", "title": "Michael Kofman"},
"fr": {"contact": "Discussion confidentielle : contacter Michael Kofman via mkofman.com", "title": "Michael Kofman"},
"ru": {"contact": "Конфиденциальное обсуждение: связаться с Michael Kofman через mkofman.com", "title": "Michael Kofman"},
"uk": {"contact": "Конфіденційна розмова: зв'язатися з Michael Kofman через mkofman.com", "title": "Michael Kofman"},
"zh": {"contact": "保密讨论：通过 mkofman.com 联系 Michael Kofman", "title": "Michael Kofman"},
"ar": {"contact": "مناقشة سرية: تواصل مع Michael Kofman عبر mkofman.com", "title": "Michael Kofman"},
"he": {"contact": "דיון סודי: צרו קשר עם Michael Kofman דרך mkofman.com", "title": "Michael Kofman"},
}),
"footer": t({
"es": {"navigation": "Navegación", "privacy": "Política de privacidad"},
"de": {"navigation": "Navigation", "privacy": "Datenschutz"},
"fr": {"navigation": "Navigation", "privacy": "Politique de confidentialité"},
"ru": {"navigation": "Навигация", "privacy": "Политика конфиденциальности"},
"uk": {"navigation": "Навігація", "privacy": "Політика конфіденційності"},
"zh": {"navigation": "导航", "privacy": "隐私政策"},
"ar": {"navigation": "التنقل", "privacy": "سياسة الخصوصية"},
"he": {"navigation": "ניווט", "privacy": "מדיניות פרטיות"},
}),
"briefAi": t({
"es": {"desc": "La IA empresarial crea valor cuando la propiedad, los datos, el flujo de trabajo y la gobernanza maduran juntos.", "eyebrow": "Informe ejecutivo", "p1": "Muchas iniciativas de IA comienzan con una demostración convincente y se estancan antes de producción. Lo que falta rara vez es solo el modelo. El valor sostenible requiere un resultado de negocio definido, un responsable, datos fiables y un flujo de trabajo que la gente realmente use.", "p2": "Los líderes deben distinguir automatización, predicción y apoyo a decisiones. Cada una exige distintos requisitos de precisión, explicabilidad, revisión humana y riesgo. Una plantilla de gobernanza única no encaja en todos los casos.", "p3": "La medición debe incluir más que el rendimiento técnico. Adopción, tiempo de ciclo, tasas de error, impacto en clientes, exposición de seguridad y coste de supervisión determinan si una capacidad de IA es económicamente e institucionalmente sólida.", "p4": "El enfoque ganador es un portfolio gestionado: escalar casos probados, detener los débiles pronto y mantener límites explícitos para decisiones de alta consecuencia. La estrategia de IA es, en última instancia, estrategia operativa.", "title": "Estrategia de IA más allá del piloto"},
"de": {"desc": "Unternehmens-KI schafft Wert, wenn Ownership, Daten, Workflow und Governance gemeinsam reifen.", "eyebrow": "Executive Brief", "p1": "Viele KI-Initiativen beginnen mit einer überzeugenden Demo und stocken vor dem Produktivbetrieb. Selten fehlt allein das Modell. Nachhaltiger Wert erfordert ein definiertes Geschäftsergebnis, klare Verantwortung, verlässliche Daten und einen Workflow, den Menschen tatsächlich nutzen.", "p2": "Führungskräfte sollten Automatisierung, Vorhersage und Entscheidungsunterstützung unterscheiden. Jede Kategorie hat unterschiedliche Anforderungen an Genauigkeit, Erklärbarkeit, menschliche Prüfung und Risiko. Eine Governance-Vorlage passt nicht für jeden Use Case.", "p3": "Messung muss mehr als technische Leistung umfassen. Adoption, Durchlaufzeit, Fehlerraten, Kundeneffekt, Sicherheitsrisiko und Aufsichtskosten bestimmen, ob eine KI-Fähigkeit wirtschaftlich und institutionell tragfähig ist.", "p4": "Der erfolgreiche Ansatz ist ein gemanagtes Portfolio: bewährte Use Cases skalieren, schwache früh stoppen und explizite Grenzen für hochkonsequente Entscheidungen setzen. KI-Strategie ist letztlich Operating-Strategie.", "title": "KI-Strategie jenseits des Pilots"},
"fr": {"desc": "L'IA d'entreprise crée de la valeur lorsque la propriété, les données, les workflows et la gouvernance mûrissent ensemble.", "eyebrow": "Note exécutive", "p1": "Beaucoup d'initiatives IA commencent par une démonstration convaincante et s'arrêtent avant la production. Ce qui manque est rarement le modèle seul. Une valeur durable exige un résultat métier défini, un responsable, des données fiables et un workflow réellement adopté.", "p2": "Les dirigeants doivent distinguer automatisation, prédiction et aide à la décision. Chacune impose des exigences différentes en précision, explicabilité, revue humaine et risque. Un modèle de gouvernance unique ne convient pas à tous les cas.", "p3": "La mesure doit inclure plus que la performance technique. Adoption, délais, taux d'erreur, impact client, exposition sécurité et coût de supervision déterminent si une capacité IA est économiquement et institutionnellement solide.", "p4": "L'approche gagnante est un portefeuille géré : scaler les cas prouvés, arrêter tôt les faibles et maintenir des limites explicites pour les décisions à haute conséquence. La stratégie IA est ultimement une stratégie opérationnelle.", "title": "Stratégie IA au-delà du pilote"},
"ru": {"desc": "Корпоративный ИИ создаёт ценность, когда ownership, данные, workflow и governance созревают вместе.", "eyebrow": "Executive Brief", "p1": "Многие AI-инициативы начинаются с убедительной демонстрации и останавливаются до production. Недостающим элементом редко бывает одна только модель. Устойчивая ценность требует определённого business outcome, ответственного владельца, надёжных данных и workflow, которым люди действительно пользуются.", "p2": "Лидерам следует различать automation, prediction и decision support. У каждого — разные требования к точности, explainability, human review и риску. Единый governance-шаблон не подходит для всех use cases.", "p3": "Измерение должно включать больше, чем техническую производительность. Adoption, cycle time, error rates, customer impact, security exposure и cost of supervision определяют, является ли AI-capability экономически и institutionally sound.", "p4": "Выигрышный подход — managed portfolio: масштабировать proven use cases, рано останавливать слабые и поддерживать explicit boundaries для high-consequence decisions. AI strategy — это ultimately operating strategy.", "title": "Стратегия ИИ за пределами пилота"},
"uk": {"desc": "Корпоративний ШІ створює цінність, коли ownership, дані, workflow і governance дозрівають разом.", "eyebrow": "Executive Brief", "p1": "Багато AI-ініціатив починаються з переконливої демонстрації й зупиняються до production. Бракує рідко лише моделі. Стійка цінність потребує визначеного business outcome, відповідального власника, надійних даних і workflow, яким люди справді користуються.", "p2": "Лідерам варто розрізняти automation, prediction і decision support. Кожен має різні вимоги до точності, explainability, human review і ризику. Єдиний governance-шаблон не підходить для всіх use cases.", "p3": "Вимірювання має включати більше, ніж технічну продуктивність. Adoption, cycle time, error rates, customer impact, security exposure і cost of supervision визначають, чи є AI-capability економічно та institutionally sound.", "p4": "Переможний підхід — managed portfolio: масштабувати proven use cases, рано зупиняти слабкі та підтримувати explicit boundaries для high-consequence decisions. AI strategy — це ultimately operating strategy.", "title": "Стратегія ШІ за межами пілота"},
"zh": {"desc": "企业AI在所有权、数据、工作流和治理共同成熟时才能创造价值。", "eyebrow": "高管简报", "p1": "许多AI计划始于令人信服的演示，却在投产前停滞。缺失的很少只是模型本身。可持续价值需要明确的业务成果、负责人、可靠的数据以及人们真正会使用的工作流。", "p2": "领导者应区分自动化、预测和决策支持。各自对准确性、可解释性、人工审查和风险有不同要求。单一治理模板无法适用于所有用例。", "p3": "衡量标准必须超越技术性能。采用率、周期时间、错误率、客户影响、安全暴露和监督成本决定AI能力是否在经济和制度上站得住脚。", "p4": "制胜方法是管理型组合：扩展已验证的用例，及早停止弱项，并为高后果决策设定明确边界。AI战略本质上是运营战略。", "title": "超越试点的AI战略"},
"ar": {"desc": "يخلق الذكاء الاصطناعي المؤسسي قيمة عندما تنضج الملكية والبيانات وسير العمل والحوكمة معاً.", "eyebrow": "ملخص تنفيذي", "p1": "تبدأ كثير من مبادرات الذكاء الاصطناعي بعرض مقنع وتتوقف قبل الإنتاج. العنصر المفقود نادراً ما يكون النموذج وحده. القيمة المستدامة تتطلب نتيجة أعمال محددة ومالكاً مسؤولاً وبيانات موثوقة وسير عمل يستخدمه الناس فعلاً.", "p2": "يجب على القادة التمييز بين الأتمتة والتنبؤ ودعم القرار. لكل منها متطلبات مختلفة للدقة والقابلية للتفسير والمراجعة البشرية والمخاطر. قالب حوكمة واحد لا يناسب كل حالة.", "p3": "يجب أن تشمل القياس أكثر من الأداء التقني. التبني ووقت الدورة ومعدلات الخطأ وتأثير العملاء والتعرض الأمني وتكلفة الإشراف تحدد ما إذا كانت قدرة الذكاء الاصطناعي سليمة اقتصادياً ومؤسسياً.", "p4": "النهج الفائز هو محفظة مُدارة: توسيع حالات الاستخدام المثبتة وإيقاف الضعيفة مبكراً والحفاظ على حدود صريحة للقرارات عالية العواقب. استراتيجية الذكاء الاصطناعي هي في النهاية استرategia تشغيل.", "title": "استراتيجية الذكاء الاصطناعي beyond the pilot"},
"he": {"desc": "בינה מלאכותית ארגונית יוצרת ערך כשבעלות, נתונים, תהליכי עבודה וממשל מתבגרים יחד.", "eyebrow": "תקציר מנהלים", "p1": "הרבה יוזמות AI מתחילות בהדגמה משכנעת ונתקעות לפני production. החסר לעיתים רחוקות הוא המודל בלבד. ערך בר-קיימא דורש תוצאה עסקית מוגדרת, בעלים אחראי, נתונים אמינים ו-workflow שאנשים באמת משתמשים בו.", "p2": "מנהיגים צריכים להבחין בין automation, prediction ו-decision support. לכל אחד דרישות שונות לדיוק, explainability, ביקורת אנושית וסיכון. תבנית governance אחת לא מתאימה לכל use case.", "p3": "מדידה חייבת לכלול יותר מביצועים טכניים. adoption, cycle time, error rates, customer impact, security exposure ו-cost of supervision קובעים אם יכולת AI sound כלכלית ומוסדית.", "p4": "הגישה המנצחת היא managed portfolio: scale proven use cases, stop weak ones early, maintain explicit boundaries ל-high-consequence decisions. AI strategy היא ultimately operating strategy.", "title": "אסטרטגיית AI מעבר לפיילוט"},
}),
"briefGenetic": t({
"es": {"desc": "El valor de la información genómica depende de la interpretación, la evidencia y la integración responsable en la atención.", "eyebrow": "Informe ejecutivo", "p1": "Los datos genéticos son abundantes; el significado clínicamente útil es escaso. Un resultado se vuelve valioso solo cuando se interpreta en contexto, se conecta con evidencia validada y se presenta de forma que apoye una decisión real.", "p2": "Esa traducción requiere colaboración entre biología molecular, medicina, estadística, ingeniería de software y comunicación con pacientes. Una debilidad en cualquier capa puede convertir sofisticación técnica en confusión clínica.", "p3": "La privacidad y el consentimiento son requisitos arquitectónicos, no notas legales al pie. Los sistemas deben limitar la exposición innecesaria, hacer visible la procedencia de los datos y preservar la agencia del paciente cuando la información se mueve entre laboratorios, plataformas y equipos de atención.", "p4": "La medicina de precisión avanzará mediante integración medida: mejor evidencia, modelos transparentes, flujos de trabajo interoperables y resultados que clínicos y pacientes puedan evaluar. La confianza es parte del producto.", "title": "De datos genéticos a decisiones clínicas"},
"de": {"desc": "Der Wert genomischer Information hängt von Interpretation, Evidenz und verantwortungsvoller Integration in die Versorgung ab.", "eyebrow": "Executive Brief", "p1": "Genetische Daten sind reichlich vorhanden; klinisch nützliche Bedeutung ist selten. Ein Ergebnis wird erst wertvoll, wenn es im Kontext interpretiert, mit validierter Evidenz verbunden und so aufbereitet wird, dass es eine echte Entscheidung unterstützt.", "p2": "Diese Übersetzung erfordert Zusammenarbeit zwischen Molekularbiologie, Medizin, Statistik, Software Engineering und Patientenkommunikation. Schwäche in einer Schicht kann technische Raffinesse in klinische Verwirrung verwandeln.", "p3": "Datenschutz und Einwilligung sind architektonische Anforderungen, keine juristischen Fußnoten. Systeme müssen unnötige Exposition begrenzen, Datenherkunft sichtbar machen und Patientenagency wahren, wenn Informationen zwischen Laboren, Plattformen und Care Teams wandern.", "p4": "Precision Medicine wird durch gemessene Integration voranschreiten: bessere Evidenz, transparente Modelle, interoperable Workflows und Outcomes, die Kliniker und Patienten bewerten können. Vertrauen ist Teil des Produkts.", "title": "Von genetischen Daten zu klinischen Entscheidungen"},
"fr": {"desc": "La valeur de l'information génomique dépend de l'interprétation, des preuves et d'une intégration responsable dans les soins.", "eyebrow": "Note exécutive", "p1": "Les données génétiques sont abondantes ; la signification cliniquement utile est rare. Un résultat devient précieux seulement s'il est interprété en contexte, relié à des preuves validées et présenté de façon à soutenir une vraie décision.", "p2": "Cette traduction exige une collaboration entre biologie moléculaire, médecine, statistiques, ingénierie logicielle et communication patient. Une faiblesse dans une couche peut transformer la sophistication technique en confusion clinique.", "p3": "Confidentialité et consentement sont des exigences architecturales, pas des notes juridiques. Les systèmes doivent limiter l'exposition inutile, rendre la provenance visible et préserver l'autonomie du patient lorsque l'information circule entre laboratoires, plateformes et équipes de soins.", "p4": "La médecine de précision avancera par une intégration mesurée : meilleures preuves, modèles transparents, workflows interopérables et résultats évaluables par cliniciens et patients. La confiance fait partie du produit.", "title": "Des données génétiques aux décisions cliniques"},
"ru": {"desc": "Ценность геномной информации зависит от интерпретации, доказательной базы и ответственной интеграции в клиническую практику.", "eyebrow": "Executive Brief", "p1": "Генетических данных много; clinically useful meaning — редкость. Результат становится ценным только когда интерпретирован в контексте, связан с validated evidence и представлен в форме, поддерживающей реальное решение.", "p2": "Такой перевод требует collaboration между molecular biology, medicine, statistics, software engineering и patient communication. Слабость на любом уровне превращает техническую sophistication в clinical confusion.", "p3": "Privacy и consent — architectural requirements, а не legal footnotes. Системы должны ограничивать unnecessary exposure, делать data provenance visible и сохранять patient agency при движении информации между laboratories, platforms и care teams.", "p4": "Precision medicine будет продвигаться через measured integration: лучшие evidence, transparent models, interoperable workflows и outcomes, которые clinicians и patients могут evaluate. Trust — часть продукта.", "title": "От генетических данных к клиническим решениям"},
"uk": {"desc": "Цінність геномної інформації залежить від інтерпретації, доказової бази та відповідальної інтеграції в клінічну практику.", "eyebrow": "Executive Brief", "p1": "Генетичних даних багато; clinically useful meaning — рідкість. Результат стає цінним лише коли інтерпретований у контексті, пов'язаний із validated evidence і поданий у формі, що підтримує реальне рішення.", "p2": "Такий переклад потребує collaboration між molecular biology, medicine, statistics, software engineering і patient communication. Слабкість на будь-якому рівні перетворює technical sophistication на clinical confusion.", "p3": "Privacy і consent — architectural requirements, а не legal footnotes. Системи мають обмежувати unnecessary exposure, робити data provenance visible і зберігати patient agency під час руху інформації між laboratories, platforms і care teams.", "p4": "Precision medicine просуватиметься через measured integration: кращі evidence, transparent models, interoperable workflows і outcomes, які clinicians і patients можуть evaluate. Trust — частина продукту.", "title": "Від генетичних даних до клінічних рішень"},
"zh": {"desc": "基因组信息的价值取决于解读、证据和负责任地融入临床护理。", "eyebrow": "高管简报", "p1": "遗传数据 abundant，临床有用的含义 scarce。结果只有在上下文中解读、与已验证证据关联并以支持真实决策的形式呈现时才有价值。", "p2": "这种转化需要分子生物学、医学、统计学、软件工程和患者沟通之间的协作。任何一层的薄弱都可能将技术 sophistication 变成临床 confusion。", "p3": "隐私和同意是架构要求，而非法律脚注。系统必须限制不必要的暴露，使数据来源可见，并在信息在实验室、平台和护理团队之间流动时 preserve 患者自主权。", "p4": "精准医学将通过 measured integration 前进：更好的证据、透明模型、互操作工作流以及临床医生和患者可以评估的结果。信任是产品的一部分。", "title": "从遗传数据到临床决策"},
"ar": {"desc": "تعتمد قيمة المعلومات الجينومية على التفسير والأدلة والدمج المسؤول في الرعاية.", "eyebrow": "ملخص تنفيذي", "p1": "البيانات الجينية وفيرة؛ المعنى مفيد سريرياً نادر. تصبح النتيجة قيمة فقط عند تفسيرها في السياق وربطها بأدلة م validated وتقديمها بشكل يدعم قراراً حقيقياً.", "p2": "يتطلب هذا الترجمة تعاوناً بين علم الأحياء الجزيئي والطب والإحصاء وهندسة البرمجيات وتواصل المرضى. ضعف في أي طبقة قد يحول الت sophistication التقنية إلى confusion سريري.", "p3": "الخصوصية والموافقة متطلبات معمارية وليست حواشي قانونية. يجب أن تحد الأنظمة من التعرض غير الضروري وتجعل مصدر البيانات مرئياً وتحافظ على agency المريض.", "p4": "ستتقدم الطب الدقيق عبر تكامل measured: أدلة أفضل ونماذج شفافة وسير عمل interoperable ونتائج يمكن للclinicians والمرضى evaluate. الثقة جزء من المنتج.", "title": "من البيانات الجينية إلى القرارات السريرية"},
"he": {"desc": "ערך המידע הגénomi תלוי בפרשנות, ראיות ואינטגרציה אחראית לטיפול.", "eyebrow": "תקציר מנהלים", "p1": "נתונים גenetיים abundant; clinically useful meaning scarce. תוצאה הופכת לערכית רק כשמinterpreted בהקשר, connected ל-validated evidence ו-presented בצורה שתומכת בהחלטה אמיתית.", "p2": "translation זה דורש collaboration בין molecular biology, medicine, statistics, software engineering ו-patient communication. חולשה בשכבה כלשהי עלולה להפוך technical sophistication ל-clinical confusion.", "p3": "privacy ו-consent הם architectural requirements, לא legal footnotes. מערכות חייבות להגביל unnecessary exposure, להפוך data provenance visible ולשמר patient agency.", "p4": "precision medicine will advance through measured integration: evidence טוב יותר, transparent models, interoperable workflows ו-outcomes שclinicians ו-patients יכולים evaluate. trust הוא חלק מהמוצר.", "title": "מנתונים גenetיים להחלטות קlinיות"},
}),
"briefIpo": t({
"es": {"desc": "Los mercados públicos no solo cambian la estructura de capital; cambian el contrato operativo.", "eyebrow": "Informe ejecutivo", "p1": "Una oferta pública inicial suele describirse como un evento de financiación. En la práctica, es una transición institucional. Pronósticos, controles, divulgación, gobernanza y comunicación ejecutiva deben ser repetibles antes de la cotización, no improvisados después.", "p2": "La preparación comienza con la calidad de las decisiones. La dirección necesita métricas fiables, propiedad clara y un ritmo operativo que explique rendimiento y variaciones. Una empresa que no reconcilia su narrativa interna luchará por comunicar una externa creíble.", "p3": "El papel del consejo también cambia. Los directores deben equilibrar crecimiento y supervisión, comprender riesgos tecnológicos y de mercado materiales, y asegurar que los incentivos apoyen valor duradero, no un solo trimestre.", "p4": "Las empresas públicas más sólidas preservan velocidad emprendedora mientras añaden disciplina institucional. El objetivo no es burocracia; es ejecución confiable a un nivel superior de responsabilidad.", "title": "Lo que cambia un IPO"},
"de": {"desc": "Öffentliche Märkte verändern nicht nur die Kapitalstruktur; sie verändern den Operating-Vertrag.", "eyebrow": "Executive Brief", "p1": "Ein Börsengang wird oft als Finanzierungsereignis beschrieben. In der Praxis ist er ein institutioneller Übergang. Forecasting, Controls, Disclosure, Governance und Executive Communication müssen vor dem Listing wiederholbar sein, nicht danach improvisiert.", "p2": "Readiness beginnt mit Entscheidungsqualität. Management braucht verlässliche Metriken, klare Ownership und einen Operating-Rhythmus, der Performance und Varianz erklären kann. Wer die interne Narrative nicht in Einklang bringt, wird extern keine glaubwürdige kommunizieren.", "p3": "Die Rolle des Boards verändert sich ebenfalls. Directors müssen Wachstum und Oversight balancieren, materielle Technologie- und Marktrisiken verstehen und sicherstellen, dass Anreize dauerhaften Wert statt eines einzelnen Quartals unterstützen.", "p4": "Die stärksten Public Companies bewahren unternehmerische Geschwindigkeit und fügen institutionelle Disziplin hinzu. Ziel ist nicht Bürokratie, sondern vertrauenswürdige Execution auf höherem Accountability-Niveau.", "title": "Was ein IPO verändert"},
"fr": {"desc": "Les marchés publics ne changent pas seulement la structure du capital ; ils changent le contrat opérationnel.", "eyebrow": "Note exécutive", "p1": "Une introduction en bourse est souvent décrite comme un événement de financement. En pratique, c'est une transition institutionnelle. Prévisions, contrôles, divulgation, gouvernance et communication exécutive doivent être reproductibles avant la cotation, pas improvisés après.", "p2": "La préparation commence par la qualité des décisions. La direction a besoin de métriques fiables, d'une propriété claire et d'un rythme opérationnel capable d'expliquer performance et écarts. Une entreprise qui ne réconcilie pas son récit interne peinera à en communiquer un externe crédible.", "p3": "Le rôle du conseil change aussi. Les administrateurs doivent équilibrer croissance et supervision, comprendre les risques technologiques et de marché matériels, et veiller à ce que les incitations soutiennent une valeur durable plutôt qu'un seul trimestre.", "p4": "Les entreprises cotées les plus solides préservent la vitesse entrepreneuriale tout en ajoutant une discipline institutionnelle. L'objectif n'est pas la bureaucratie, mais une exécution fiable à un niveau supérieur de responsabilité.", "title": "Ce qu'un IPO change"},
"ru": {"desc": "Публичные рынки меняют не только capital structure; они меняют operating contract.", "eyebrow": "Executive Brief", "p1": "IPO часто описывают как financing event. На практике это institutional transition. Forecasting, controls, disclosure, governance и executive communication должны стать repeatable до listing, а не improvised после.", "p2": "Readiness начинается с decision quality. Management нужны reliable metrics, clear ownership и operating cadence, способный объяснить performance и variance. Компания, не reconciling internal narrative, будет struggle с credible external one.", "p3": "Роль board тоже меняется. Directors должны balance growth и oversight, понимать material technology и market risks и ensure, что incentives support durable value, а не single quarter.", "p4": "Сильнейшие public companies сохраняют entrepreneurial speed, добавляя institutional discipline. Objective — не bureaucracy; это trustworthy execution на более высоком уровне accountability.", "title": "Что меняет IPO"},
"uk": {"desc": "Публічні ринки змінюють не лише capital structure; вони змінюють operating contract.", "eyebrow": "Executive Brief", "p1": "IPO часто описують як financing event. На практиці це institutional transition. Forecasting, controls, disclosure, governance і executive communication мають стати repeatable до listing, а не improvised після.", "p2": "Readiness починається з decision quality. Management потрібні reliable metrics, clear ownership і operating cadence, здатний пояснити performance і variance. Компанія, що не reconciling internal narrative, буде struggle з credible external one.", "p3": "Роль board теж змінюється. Directors мають balance growth і oversight, розуміти material technology і market risks і ensure, що incentives support durable value, а не single quarter.", "p4": "Найсильніші public companies зберігають entrepreneurial speed, додаючи institutional discipline. Objective — не bureaucracy; це trustworthy execution на вищому рівні accountability.", "title": "Що змінює IPO"},
"zh": {"desc": "公开市场不仅改变资本结构，还改变运营契约。", "eyebrow": "高管简报", "p1": "IPO常被描述为融资事件。实际上是制度转型。预测、控制、披露、治理和高管沟通必须在上市前可重复，而非事后即兴。", "p2": "准备始于决策质量。管理层需要可靠指标、明确所有权和能解释绩效与偏差的运营节奏。无法调和内部叙事的公司将难以传达可信的外部叙事。", "p3": "董事会角色也改变。董事须平衡增长与监督，理解重大技术和市场风险，并确保激励支持持久价值而非单一季度。", "p4": "最强的上市公司在增加制度纪律的同时保持创业速度。目标不是官僚主义，而是在更高问责水平上的可信执行。", "title": "IPO带来的变化"},
"ar": {"desc": "الأسواق العامة لا تغير هيكل رأس المال فحسب؛ بل تغير العقد التشغيلي.", "eyebrow": "ملخص تنفيذي", "p1": "يُ described الاكتتاب العام غالباً كحدث تمويل. عملياً، هو transition مؤسسي. يجب أن تصبح forecasting وcontrols وdisclosure وgovernance وexecutive communication repeatable قبل listing.", "p2": "تبدأ readiness بجودة القرار. يحتاج management إلى reliable metrics وclear ownership وoperating cadence. شركة لا ت reconcili internal narrative ست struggle في external one.", "p3": "يتغير دور board أيضاً. يجب على directors balance growth وoversight وفهم material risks وensure incentives support durable value.", "p4": "أ strongest public companies تحافظ على entrepreneurial speed مع institutional discipline. الهدف trustworthy execution على مستوى accountability أعلى.", "title": "ما يغيره الاكتتاب العام"},
"he": {"desc": "שווקים ציבוריים לא רק משנים capital structure; הם משנים operating contract.", "eyebrow": "תקציר מנהלים", "p1": "IPO מתואר לעיתים כ-financing event. בפועל, institutional transition. forecasting, controls, disclosure, governance ו-executive communication חייבים repeatable לפני listing.", "p2": "readiness מתחיל ב-decision quality. management צריך reliable metrics, clear ownership ו-operating cadence. חברה שלא reconciling internal narrative ת struggle עם external one.", "p3": "תפקיד board משתנה. directors חייבים balance growth ו-oversight, understand material risks, ensure incentives support durable value.", "p4": "strongest public companies שומרות entrepreneurial speed עם institutional discipline. objective — trustworthy execution ברמת accountability גבוהה יותר.", "title": "מה IPO משנה"},
}),
}
# fmt: on

DATA = {**DATA, **REMAINING, **LARGE}
for section, lang_map in FIXES.items():
    for lang in ("ru", "uk"):
        if lang in lang_map:
            DATA[section][lang].update(lang_map[lang])


def build() -> dict:
    result = {lang: {} for lang in LANGS}
    for section, lang_map in DATA.items():
        for lang in LANGS:
            result[lang][section] = lang_map[lang]
    return result


def main() -> None:
    out = build()
    OUTPUT.write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    total = sum(len(v) for s in out["es"].values() for v in [s])
    key_count = sum(len(keys) for keys in out["es"].values())
    print(f"Wrote {OUTPUT} — {key_count} keys × {len(LANGS)} langs")


if __name__ == "__main__":
    main()
