#!/usr/bin/env python3
"""Build i18n_string_table.json: English source string -> 8 language translations."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from gen_i18n_gaps_translations import build as build_baseline
from i18n_constants import LANGS, T

GAPS_PATH = Path("/tmp/i18n_gaps.json")
OUT_PATH = Path(__file__).resolve().parent / "i18n_string_table.json"

KEEP_ENGLISH = {
    "Michael Kofman", "Digital Invest Inc.", "AGRON Inc.", "9 Net Avenue Inc.", "9 Net Avenue",
    "NASDAQ: CNTX", "NASDAQ: XOXO", "Concentric Networks", "XO Communications", "DataPeer Inc.",
    "DataPeer", "XIBI Group Inc.", "Biotechnology Group Inc.", "Nikolaev Shipbuilding Plant",
    "Elitan United Inc.", "Astra Corp", "Sony", "Formspree", "Plausible", "Google Analytics",
    "LinkedIn", "ISDRI", "Entrepreneur Magazine", "Healthcare Tech Outlook", "Who's Who",
    "Clayton M. Christensen", "Daniel Kahneman", "David Deutsch", "Richard Rumelt", "Thomas S. Kuhn",
    "The Innovator's Dilemma", "Thinking, Fast and Slow", "The Beginning of Infinity",
    "Good Strategy/Bad Strategy", "The Structure of Scientific Revolutions",
    "Top Precision Medicine Solutions", "mkofman.com", "mkofman@mkofman.com", "agron1.com",
    "Charlotte, North Carolina", "CEO & CTO", "CEO & Board Member", "Founder",
    "AGRON Ecosystem", "AGRON Maritime Intelligence + Security",
    "Aerial-Ground Robotics Operations Network",
    "Who's Who in America", "Who's Who in the World",
    "Who's Who in Science & Engineering", "Who's Who in Science and Engineering",
    "State of the Storage Industry", "Email", "Ph.D.", "Doctor of Technical Sciences",
}


def flatten(sectioned: dict) -> dict[str, dict[str, str]]:
    flat: dict[str, dict[str, str]] = {}
    for lang in LANGS:
        for section, keys in sectioned[lang].items():
            if not isinstance(keys, dict):
                continue
            if section == "meta":
                for key, val in keys.items():
                    flat.setdefault(f"meta.{key}", {})[lang] = val
            else:
                for key, val in keys.items():
                    flat.setdefault(f"{section}.{key}", {})[lang] = val
    return flat


def should_keep(en: str) -> bool:
    if en in KEEP_ENGLISH:
        return True
    if en.endswith(" Inc.") or en.endswith(" Corp"):
        return True
    if re.fullmatch(r"[\d\s—–\-·/→]+", en):
        return True
    if re.match(r"^\d{4}\s*[—–-]", en):
        return True
    return False


def load_gaps() -> dict[str, str]:
    gaps = json.loads(GAPS_PATH.read_text(encoding="utf-8"))
    return {f"{sec}.{k}": v for sec, keys in gaps.items() for k, v in keys.items()}


# fmt: off
# Quality translations keyed by exact English source string.
# Western langs filled from baseline where available; ru/uk/ar/he always explicit.
QUALITY: dict[str, dict[str, str]] = {}

def Q(en: str, es: str, de: str, fr: str, ru: str, uk: str, zh: str, ar: str, he: str) -> None:
    QUALITY[en] = T(es, de, fr, ru, uk, zh, ar, he)

# --- UI / short strings ---
Q("Contact", "Contacto", "Kontakt", "Contact", "Контакты", "Контакти", "联系", "تواصل", "יצירת קשר")
Q("Advisory", "Asesoría", "Beratung", "Conseil", "Консалтинг", "Консалтинг", "顾问", "استشارات", "ייעוץ")
Q("Advisory →", "Asesoría →", "Beratung →", "Conseil →", "Консалтинг →", "Консалтинг →", "顾问 →", "استشارات →", "ייעוץ →")
Q("Advisory — Michael Kofman", "Asesoría — Michael Kofman", "Beratung — Michael Kofman", "Conseil — Michael Kofman", "Консалтинг — Michael Kofman", "Консалтинг — Michael Kofman", "顾问 — Michael Kofman", "استشارات — Michael Kofman", "ייעוץ — Michael Kofman")
Q("Business", "Negocios", "Business", "Business", "Бизнес", "Бізнес", "商业", "أعمال", "עסקים")
Q("Message", "Mensaje", "Nachricht", "Message", "Сообщение", "Повідомлення", "留言", "رسالة", "הודעה")
Q("Navigation", "Navegación", "Navigation", "Navigation", "Навигация", "Навігація", "导航", "التنقل", "ניווט")
Q("Introduction", "Introducción", "Einführung", "Introduction", "Введение", "Вступ", "简介", "مقدمة", "הקדמה")
Q("Executive Brief", "Informe ejecutivo", "Executive Brief", "Note exécutive", "Исполнительный бриф", "Виконавчий бриф", "高管简报", "ملخص تنفيذي", "תקציר מנהלים")
Q("Executive Perspective", "Perspectiva ejecutiva", "Executive Perspective", "Perspective exécutive", "Исполнительная перспектива", "Виконавча перспектива", "高管视角", "منظور تنفيذي", "פרספקטיבה מנהלית")
Q("Digital Health", "Salud digital", "Digital Health", "Santé numérique", "Цифровое здравоохранение", "Цифрове охорону здоров'я", "数字健康", "الصحة الرقمية", "בריאות דיגיטלית")
Q("The Record", "El registro", "Der Werdegang", "Le parcours", "Хроника", "Хроніка", "履历", "السجل", "הרישום")
Q("The Record →", "El registro →", "Der Werdegang →", "Le parcours →", "Хроника →", "Хроніка →", "履历 →", "السجل →", "הרישום →")
Q("The Record — Michael Kofman", "El registro — Michael Kofman", "Der Werdegang — Michael Kofman", "Le parcours — Michael Kofman", "Хроника — Michael Kofman", "Хроніка — Michael Kofman", "履历 — Michael Kofman", "السجل — Michael Kofman", "הרישום — Michael Kofman")
Q("Life Sciences & Human Data", "Ciencias de la vida y datos humanos", "Life Sciences & Human Data", "Sciences de la vie & données humaines", "Науки о жизни и данные о человеке", "Науки про життя та дані про людину", "生命科学与人类数据", "علوم الحياة وبيانات الإنسان", "מדעי החיים ונתוני אדם")
Q("Autonomous Systems", "Sistemas autónomos", "Autonome Systeme", "Systèmes autonomes", "Автономные системы", "Автономні системи", "自主系统", "أنظمة مستقلة", "מערכות אוטונומיות")
Q("Technology Companies & Public Markets", "Empresas tecnológicas y mercados públicos", "Technologieunternehmen & öffentliche Märkte", "Entreprises technologiques & marchés publics", "Технологические компании и публичные рынки", "Технологічні компанії та публічні ринки", "科技公司与公开市场", "شركات التكنولوجيا والأسواق العامة", "חברות טכנולוגיה ושווקים ציבוריים")
Q("Board Service", "Servicio en juntas", "Board Service", "Mandats au conseil", "Работа в совете директоров", "Робота в раді директорів", "董事会服务", "خدمة مجلس الإدارة", "שירות דירקטוריון")
Q("CEO & Founder Advisory", "Asesoría para CEO y fundadores", "CEO- & Founder Advisory", "Conseil CEO & fondateurs", "Консалтинг для CEO и основателей", "Консалтинг для CEO та засновників", "CEO与创始人顾问", "استشارات CEOs والمؤسسين", "ייעוץ CEO ומייסדים")
Q("Technology Due Diligence", "Due diligence tecnológico", "Technology Due Diligence", "Due diligence technologique", "Технологический due diligence", "Технологічний due diligence", "技术尽职调查", "العناية الواجبة التقنية", "Due diligence טכנולוגי")
Q("Perspectives", "Perspectivas", "Perspektiven", "Perspectives", "Перспективы", "Перспективи", "观点", "وجهات نظر", "פרספקטיבות")
Q("Selected Writing", "Escritos seleccionados", "Ausgewählte Texte", "Écrits sélectionnés", "Избранные тексты", "Обрані тексти", "精选文章", "كتابات مختارة", "כתיבה נבחרת")
Q("Capital Markets", "Mercados de capitales", "Kapitalmärkte", "Marchés de capitaux", "Рынки капитала", "Ринки капіталу", "资本市场", "أسواق رأس المال", "שוק ההון")
Q("Precision Medicine", "Medicina de precisión", "Precision Medicine", "Médecine de précision", "Прецизионная медицина", "Прецизійна медицина", "精准医疗", "الطب الدقيق", "רפואת דיוק")
Q("Artificial Intelligence", "Inteligencia artificial", "Künstliche Intelligenz", "Intelligence artificielle", "Искусственный интеллект", "Штучний інтелект", "人工智能", "الذكاء الاصطناعي", "בינה מלאכותית")
Q("Executive Briefs", "Informes ejecutivos", "Executive Briefs", "Notes exécutives", "Исполнительные брифы", "Виконавчі брифи", "高管简报", "ملخصات تنفيذية", "תקצירי מנהלים")
Q("Ideas for Leaders", "Ideas para líderes", "Ideen für Führungskräfte", "Idées pour les dirigeants", "Идеи для лидеров", "Ідеї для лідерів", "领导者之思", "أفكار للقادة", "רעיונות למנהיגים")
Q("Insights", "Perspectivas", "Einblicke", "Perspectives", "Инсайты", "Інсайти", "见解", "رؤى", "תובנות")
Q("Insights — Michael Kofman", "Perspectivas — Michael Kofman", "Einblicke — Michael Kofman", "Perspectives — Michael Kofman", "Инсайты — Michael Kofman", "Інсайти — Michael Kofman", "见解 — Michael Kofman", "رؤى — Michael Kofman", "תובנות — Michael Kofman")
Q("Occasional Notes", "Notas ocasionales", "Gelegentliche Notizen", "Notes occasionnelles", "Время от времени", "Час від часу", "不定期札记", "ملاحظات متفرقة", "הערות מדי פעם")
Q("Executive Perspective, Without the Noise", "Perspectiva ejecutiva, sin ruido", "Executive Perspective, ohne Lärm", "Perspective exécutive, sans bruit", "Исполнительная перспектива без шума", "Виконавча перспектива без шуму", "高管视角，拒绝噪音", "منظور تنفيذي بلا ضجيج", "פרספקטיבה מנהלית, ללא רעש")
Q("Subscribe for Updates", "Suscribirse a actualizaciones", "Updates abonnieren", "S'abonner aux mises à jour", "Подписаться на обновления", "Підписатися на оновлення", "订阅更新", "اشترك في التحديثات", "הירשמו לעדכונים")
Q("Reading List", "Lista de lectura", "Leseliste", "Liste de lecture", "Список для чтения", "Список для читання", "阅读清单", "قائمة القراءة", "רשימת קריאה")
Q("Books That Shape Strategic Thinking", "Libros que moldean el pensamiento estratégico", "Bücher, die strategisches Denken prägen", "Livres qui façonnent la pensée stratégique", "Книги, формирующие стратегическое мышление", "Книги, що формують стратегічне мислення", "塑造战略思维的书籍", "كتب تشكّل التفكير الاستراتيجي", "ספרים שמעצבים חשיבה אסטרטגית")
Q("From Genetic Data to Clinical Decisions", "De datos genéticos a decisiones clínicas", "Von genetischen Daten zu klinischen Entscheidungen", "Des données génétiques aux décisions cliniques", "От генетических данных к клиническим решениям", "Від генетичних даних до клінічних рішень", "从遗传数据到临床决策", "من البيانات الجينية إلى القرارات السريرية", "מנתונים גenetיים להחלטות קlinיות")
Q("AI Strategy Beyond the Pilot", "Estrategia de IA más allá del piloto", "KI-Strategie jenseits des Pilots", "Stratégie IA au-delà du pilote", "Стратегия ИИ за пределами пилота", "Стратегія ШІ за межами пілота", "超越试点的AI战略", "استراتيجية الذكاء الاصطناعي beyond the pilot", "אסטרטגיית AI מעבר לפיילוט")
Q("Leadership Thesis", "Tesis de liderazgo", "Leadership Thesis", "Thèse de leadership", "Тезис лидерства", "Тезис лідерства", "领导力论题", "أطروحة القيادة", "תזת מנהיגות")
Q("Leadership Thesis — Michael Kofman", "Tesis de liderazgo — Michael Kofman", "Leadership Thesis — Michael Kofman", "Thèse de leadership — Michael Kofman", "Тезис лидерства — Michael Kofman", "Тезис лідерства — Michael Kofman", "领导力论题 — Michael Kofman", "أطروحة القيادة — Michael Kofman", "תזת מנהיגות — Michael Kofman")
Q("Build for the Long Term. Decide in the Present.", "Construir a largo plazo. Decidir en el presente.", "Für die Langzeit bauen. In der Gegenwart entscheiden.", "Construire pour le long terme. Décider dans le présent.", "Строить надолго. Решать — сейчас.", "Будувати надовго. Вирішувати — зараз.", "为长期建设。在当下决策。", "البناء على المدى البعيد. القرار في الحاضر.", "לבנות לטווח ארוך. להחליט בהווה.")
Q("Contact — Michael Kofman", "Contacto — Michael Kofman", "Kontakt — Michael Kofman", "Contact — Michael Kofman", "Контакты — Michael Kofman", "Контакти — Michael Kofman", "联系 — Michael Kofman", "تواصل — Michael Kofman", "יצירת קשר — Michael Kofman")
Q("Executive Overview — Michael Kofman", "Resumen ejecutivo — Michael Kofman", "Executive Overview — Michael Kofman", "Aperçu exécutif — Michael Kofman", "Исполнительный обзор — Michael Kofman", "Виконавчий огляд — Michael Kofman", "高管概览 — Michael Kofman", "نظرة تنفيذية — Michael Kofman", "סקירה מנהלית — Michael Kofman")
Q("Intellectual Property — Michael Kofman", "Propiedad intelectual — Michael Kofman", "Geistiges Eigentum — Michael Kofman", "Propriété intellectuelle — Michael Kofman", "Интеллектуальная собственность — Michael Kofman", "Інтелектуальна власність — Michael Kofman", "知识产权 — Michael Kofman", "الملكية الفكرية — Michael Kofman", "קניין רוחני — Michael Kofman")
Q("Press Archive — Michael Kofman", "Archivo de prensa — Michael Kofman", "Presse-Archiv — Michael Kofman", "Archives presse — Michael Kofman", "Архив прессы — Michael Kofman", "Архів преси — Michael Kofman", "媒体档案 — Michael Kofman", "أرشيف الصحافة — Michael Kofman", "ארכיון עיתונות — Michael Kofman")
Q("Privacy Policy — Michael Kofman", "Política de privacidad — Michael Kofman", "Datenschutz — Michael Kofman", "Politique de confidentialité — Michael Kofman", "Политика конфиденциальности — Michael Kofman", "Політика конфіденційності — Michael Kofman", "隐私政策 — Michael Kofman", "سياسة الخصوصية — Michael Kofman", "מדיניות פרטיות — Michael Kofman")
Q("What an IPO Changes — Michael Kofman", "Lo que cambia un IPO — Michael Kofman", "Was ein IPO verändert — Michael Kofman", "Ce qu'un IPO change — Michael Kofman", "Что меняет IPO — Michael Kofman", "Що змінює IPO — Michael Kofman", "IPO带来的变化 — Michael Kofman", "ما يغيره الاكتتاب العام — Michael Kofman", "מה IPO משנה — Michael Kofman")
Q("Data Infrastructure", "Infraestructura de datos", "Dateninfrastruktur", "Infrastructure de données", "Инфраструктура данных", "Інфраструктура даних", "数据基础设施", "بنية البيانات التحتية", "תשתית נתונים")
Q("Services", "Servicios", "Leistungen", "Services", "Услуги", "Послуги", "服务", "خدمات", "שירותים")
Q("Brief: IPO", "Brief: IPO", "Brief: IPO", "Brief : IPO", "Бриф: IPO", "Бриф: IPO", "简报：IPO", "Brief: IPO", "Brief: IPO")
Q("Patent", "Patente", "Patent", "Brevet", "Патент", "Патент", "专利", "براءة اختراع", "פטנט")
Q("Publications", "Publicaciones", "Publikationen", "Publications", "Публикации", "Публікації", "出版物", "منشورات", "פרסומים")
Q("Digital Invest Inc. Feature", "Reportaje sobre Digital Invest Inc.", "Digital Invest Inc. Feature", "Reportage Digital Invest Inc.", "Репортаж о Digital Invest Inc.", "Репортаж про Digital Invest Inc.", "Digital Invest Inc. 专题", "تقرير عن Digital Invest Inc.", "כתבה על Digital Invest Inc.")
Q("Legal", "Legal", "Rechtliches", "Mentions légales", "Правовая информация", "Правова інформація", "法律", "قانوني", "משפטי")
Q("Privacy Policy", "Política de privacidad", "Datenschutz", "Politique de confidentialité", "Политика конфиденциальности", "Політика конфіденційності", "隐私政策", "سياسة الخصوصية", "מדיניות פרטיות")
Q("Last updated: July 2026", "Última actualización: julio de 2026", "Zuletzt aktualisiert: Juli 2026", "Dernière mise à jour : juillet 2026", "Последнее обновление: июль 2026", "Останнє оновлення: липень 2026", "最后更新：2026年7月", "آخر تحديث: يوليو 2026", "עודכן לאחרונה: יולי 2026")
Q("Information We Collect", "Información que recopilamos", "Informationen, die wir erheben", "Informations collectées", "Какую информацию мы собираем", "Яку інформацію ми збираємо", "我们收集的信息", "المعلومات التي نجمعها", "מידע שאנו אוספים")
Q("How We Use Information", "Cómo usamos la información", "Wie wir Informationen nutzen", "Utilisation des informations", "Как мы используем информацию", "Як ми використовуємо інформацію", "我们如何使用信息", "كيف نستخدم المعلومات", "כיצד אנו משתמשים במידע")
Q("Third-Party Services", "Servicios de terceros", "Dienste Dritter", "Services tiers", "Сторонние сервисы", "Сторонні сервіси", "第三方服务", "خدمات طرف ثالث", "שירותי צד שלישי")
Q("Your Rights", "Sus derechos", "Ihre Rechte", "Vos droits", "Ваши права", "Ваші права", "您的权利", "حقوقك", "זכויותיך")
Q("Patents", "Patentes", "Patente", "Brevets", "Патенты", "Патенти", "专利", "براءات الاختراع", "פטנטים")
Q("Protected Inventions", "Invenciones protegidas", "Geschützte Erfindungen", "Inventions protégées", "Защищённые изобретения", "Захищені винаходи", "受保护的发明", "اختراعات محمية", "המצאות מוגנות")
Q("Technical & Executive Writing", "Escritura técnica y ejecutiva", "Technische & Executive Writing", "Écrits techniques & exécutifs", "Техническое и исполнительное письмо", "Технічне та виконавче письмо", "技术与高管写作", "كتابة تقنية وتنفيذية", "כתיבה טכנית ומנהלית")
Q("Research", "Investigación", "Forschung", "Recherche", "Исследования", "Дослідження", "研究", "بحث", "מחקר")
Q("Interdisciplinary Programs", "Programas interdisciplinarios", "Interdisziplinäre Programme", "Programmes interdisciplinaires", "Междисциплинарные программы", "Міждисциплінарні програми", "跨学科项目", "برامج متعددة التخصصات", "תוכניות בין-תחומיות")
Q("Applied Ideas, Documented", "Ideas aplicadas, documentadas", "Angewandte Ideen, dokumentiert", "Idées appliquées, documentées", "Прикладные идеи, задокументированные", "Прикладні ідеї, задокументовані", "应用思想，有据可查", "أفكار مطبّقة، موثّقة", "רעיונות יישומיים, מתועדים")
Q("Biographies", "Biografías", "Biografien", "Biographies", "Биографии", "Біографії", "传记", "سير ذاتية", "ביוגרפיות")
Q("Official Color Palette", "Paleta de colores oficial", "Offizielle Farbpalette", "Palette de couleurs officielle", "Официальная цветовая палитра", "Офіційна палітра кольорів", "官方配色", "لوحة الألوان الرسمية", "לוח צבעים רשמי")
Q("Download Brand Assets", "Descargar activos de marca", "Brand Assets herunterladen", "Télécharger les assets de marque", "Скачать бренд-активы", "Завантажити бренд-активи", "下载品牌资产", "تنزيل أصول العلامة التجارية", "הורדת נכסי מותג")
Q("Brand Assets", "Activos de marca", "Brand Assets", "Assets de marque", "Бренд-активы", "Бренд-активи", "品牌资产", "أصول العلامة التجارية", "נכסי מותג")
Q("Primary Logo", "Logotipo principal", "Primäres Logo", "Logo principal", "Основной логотип", "Основний логотип", "主标识", "الشعار الأساسي", "לוגו ראשי")
Q("Identity & Usage", "Identidad y uso", "Identität & Nutzung", "Identité & usage", "Идентичность и использование", "Ідентичність та використання", "标识与使用", "الهوية والاستخدام", "זהות ושימוש")
Q("Download PDF", "Descargar PDF", "PDF herunterladen", "Télécharger le PDF", "Скачать PDF", "Завантажити PDF", "下载PDF", "تنزيل PDF", "הורדת PDF")
Q("Download", "Descarga", "Download", "Téléchargement", "Скачать", "Завантажити", "下载", "تنزيل", "הורדה")
Q("One-Page Media Kit", "Kit de medios de una página", "Einseitiges Media Kit", "Media kit d'une page", "Одностраничный медиакit", "Односторінковий media kit", "单页媒体资料包", "حزمة إعلامية من صفحة واحدة", "ערכת מדיה בעמוד אחד")
Q("Press & Media", "Prensa y medios", "Presse & Medien", "Presse & médias", "Пресса и медиа", "Пресса і медіа", "媒体", "صحافة وإعلام", "עיתונות ומדיה")
Q("Selected Coverage", "Cobertura seleccionada", "Ausgewählte Berichterstattung", "Couverture sélectionnée", "Избранные публикации", "Обрані публікації", "精选报道", "تغطية مختارة", "כיסוי נבחר")
Q("From the Archive", "Del archivo", "Aus dem Archiv", "Des archives", "Из архива", "З архіву", "档案精选", "من الأرشيف", "מהארכיון")
Q("Open full page scan →", "Abrir escaneo completo →", "Vollständigen Scan öffnen →", "Ouvrir le scan complet →", "Открыть полный скан →", "Відкрити повний скан →", "打开完整扫描 →", "فتح المسح الكامل →", "פתיחת סריקה מלאה →")
Q("Biographical Recognition", "Reconocimiento biográfico", "Biografische Anerkennung", "Reconnaissance biographique", "Биографическое признание", "Біографічне визнання", "传记认可", "تقدير биográfي", "הכרה биográfית")
Q("Interview", "Entrevista", "Interview", "Interview", "Интервью", "Інтерв'ю", "采访", "مقابلة", "ראיון")
Q("Entrepreneur of the Year", "Emprendedor del Año", "Entrepreneur of the Year", "Entrepreneur of the Year", "Предприниматель года", "Підприємець року", "年度企业家", "رائد أعمال العام", "יזם השנה")
Q("Executive Award", "Premio ejecutivo", "Executive Award", "Prix exécutif", "Исполнительная награда", "Виконавча награда", "高管奖项", "جائزة تنفيذية", "פרס מנהלים")
Q("View archive", "Ver archivo", "Archiv ansehen", "Voir l'archive", "Смотреть архив", "Переглянути архів", "查看档案", "عرض الأرشيف", "צפייה בארכיון")
Q("View feature", "Ver reportaje", "Feature ansehen", "Voir l'article", "Смотреть материал", "Переглянути матеріал", "查看专题", "عرض التقرير", "צפייה בכתבה")
Q("Industry Recognition", "Reconocimiento sectorial", "Branchenanerkennung", "Reconnaissance sectorielle", "Отраслевое признание", "Галузеве визнання", "行业认可", "تقدير صناعي", "הכרה ענפית")
Q("Entrepreneur Magazine recognition.", "Reconocimiento de Entrepreneur Magazine.", "Entrepreneur Magazine recognition.", "Reconnaissance Entrepreneur Magazine.", "Признание Entrepreneur Magazine.", "Визнання Entrepreneur Magazine.", "Entrepreneur Magazine 认可。", "تقدير Entrepreneur Magazine.", "הכרה מ-Entrepreneur Magazine.")
Q("Speaking Topics", "Temas de conferencias", "Vortragsthemen", "Sujets de conférences", "Темы выступлений", "Теми виступів", "演讲主题", "موضوعات المحاضرات", "נושאי הרצאות")
Q("Digital Health Sector", "Sector de salud digital", "Digital-Health-Sektor", "Secteur de la santé numérique", "Сектор цифрового здравоохранения", "Сектор цифрового охорону здоров'я", "数字健康领域", "قطاع الصحة الرقمية", "מגזר בריאות דיגיטלית")
Q("Global Infrastructure", "Infraestructura global", "Globale Infrastruktur", "Infrastructure mondiale", "Глобальная инфраструктура", "Глобальна інфраструктура", "全球基础设施", "بنية تحتية عالمية", "תשתית גлобלית")
Q("Live Projects", "Proyectos activos", "Live-Projekte", "Projets actifs", "Активные проекты", "Активні проєкти", "活跃项目", "مشاريع نشطة", "פרויקטים פעילים")
Q("Active Sites", "Sitios activos", "Aktive Sites", "Sites actifs", "Активные сайты", "Активні сайти", "活跃网站", "مواقع نشطة", "אתרים פעילים")
Q("Active", "Activo", "Aktiv", "Actif", "Активно", "Активно", "活跃", "نشط", "פעיל")
Q("Exited", "Salida", "Exit", "Sortie", "Exit", "Exit", "已退出", "خروج", "יציאה")
Q("Legacy", "Legado", "Legacy", "Legacy", "Legacy", "Legacy", "遗留", "إرث", "מורשת")
Q("Current", "Actual", "Aktuell", "Actuel", "Текущее", "Поточне", "当前", "حالي", "נוכחי")
Q("Selected History", "Historia seleccionada", "Ausgewählte Historie", "Historique sélectionné", "Избранная история", "Вибрана історія", "精选历史", "تاريخ مختار", "היסטוריה נבחרת")
Q("Innovation Theater", "Teatro de innovación", "Innovation Theater", "Théâtre de l'innovation", "Театр инноваций", "Театр інновацій", "创新表演", "مسرح الابتكار", "תיאטרון חדשנות")
Q("Growth Without Governance", "Crecimiento sin gobernanza", "Wachstum ohne Governance", "Croissance sans gouvernance", "Рост без управления", "Зростання без управління", "无治理的增长", "نمو بلا حوكمة", "צמיחה ללא ממשל")
Q("False Certainty", "Falsa certeza", "Falsche Gewissheit", "Fausse certitude", "Ложная определённость", "Хибна певненість", "虚假确定性", "يقين زائف", "ודאות כוזבת")
Q("What I Believe", "En qué creo", "Woran ich glaube", "Ce en quoi je crois", "Вo что я верю", "У що я вірю", "我的信念", "ما أؤمن به", "במה אני מאמין")
Q("Seven Principles for Enduring Organizations", "Siete principios para organizaciones duraderas", "Sieben Prinzipien für beständige Organisationen", "Sept principes pour des organisations durables", "Семь принципов для устойчивых организаций", "Сім принципів для стійких організацій", "持久组织的七项原则", "سبعة مبادئ للمؤسسات الدائمة", "שבעה עקרונות לארגונים מתמשכים")
Q("The Horizon", "El horizonte", "Der Horizont", "L'horizon", "Горизонт", "Горizont", "地平线", "الأفق", "האופק")
Q("What I Reject", "Lo que rechazo", "Was ich ablehne", "Ce que je rejette", "Что я отвергаю", "Що я відкидаю", "我拒绝的", "ما أرفضه", "מה שאני דוחה")
Q("Three Expensive Illusions", "Tres ilusiones costosas", "Drei teure Illusionen", "Trois illusions coûteuses", "Три дорогих иллюзии", "Три дорогих ілюзії", "三种昂贵的幻觉", "ثلاثة أوهام مكلفة", "שלוש אשליות יקרות")
Q("Strategy Must Produce Choices", "La estrategia debe producir decisiones", "Strategie muss Entscheidungen erzeugen", "La stratégie doit produire des choix", "Стратегия должна порождать выбор", "Стратегія повинна породжувати вибір", "战略必须产生选择", "يجب أن تنتج الاسترategia خيارات", "אסטרטegיה חייבת לייצר בחירות")
Q("Technology Is a Governance Issue", "La tecnología es un asunto de gobernanza", "Technologie ist eine Governance-Frage", "La technologie est un enjeu de gouvernance", "Технология — вопрос управления", "Технологія — питання управління", "技术是治理问题", "التكنولوجيا مسألة حوكمة", "טכנולוגיה היא סוגיית ממשל")
Q("Evidence Should Outrank Enthusiasm", "La evidencia debe superar al entusiasmo", "Evidenz soll Enthusiasmus übertrumpfen", "Les preuves doivent primer sur l'enthousiasme", "Доказательства важнее энтузиазма", "Докази важливіші за ентузіазм", "证据应胜过热情", "يجب أن تتفوق الأدلة على الحماس", "ראיות צריכות לגבור על התלהבות")
Q("Architecture Shapes the Enterprise", "La arquitectura moldea la empresa", "Architektur formt das Unternehmen", "L'architecture façonne l'entreprise", "Архитектура формирует компанию", "Архітектура формує компанію", "架构塑造企业", "البنية تشكّل المؤسسة", "ארכיטקטורה מעצבת את הארגון")
Q("Trust Is Operating Infrastructure", "La confianza es infraestructura operativa", "Vertrauen ist Operating-Infrastruktur", "La confiance est une infrastructure opérationnelle", "Доверие — операционная инфраструктура", "Довіра — операційна інфраструктура", "信任是运营基础设施", "الثقة بنية تشغيلية", "אמון הוא תשתית תפעולית")
Q("Capital Must Follow Capability", "El capital debe seguir a la capacidad", "Kapital muss der Fähigkeit folgen", "Le capital doit suivre la capacité", "Капитал должен следовать за способностями", "Капітал повинен слідувати за спроможностями", "资本必须跟随能力", "يجب أن يتبع رأس المال القدرة", "הון חייב לעקוב אחר יכולת")
Q("Leaders Design Their Successors", "Los líderes diseñan a sus sucesores", "Führungskräfte gestalten ihre Nachfolger", "Les dirigeants conçoivent leurs successeurs", "Лидеры проектируют своих преемников", "Лідери проектують своїх наступників", "领导者设计继任者", "القادة يصمّمون خلفاءهم", "מנהיגים מתכננים את יורשיהם")
Q("The Next Advantage Is Responsible Integration", "La próxima ventaja es la integración responsable", "Der nächste Vorteil ist verantwortungsvolle Integration", "Le prochain avantage est l'intégration responsable", "Следующее преимущество — ответственная интеграция", "Наступна перевага — відповідальна інтеграція", "下一个优势是 responsible integration", "الميزة التالية هي التكامل المسؤول", "היתרון הבא הוא אינטגרציה אחראית")
Q("All active sites →", "Todos los sitios activos →", "Alle aktiven Sites →", "Tous les sites actifs →", "Все активные сайты →", "Усі активні сайти →", "所有活跃网站 →", "جميع المواقع النشطة →", "כל האתרים הפעילים →")
Q("All insights →", "Todas las perspectivas →", "Alle Einblicke →", "Toutes les perspectives →", "Все инсайты →", "Усі інсайти →", "全部见解 →", "جميع الرؤى →", "כל התובנות →")
Q("agron1.com →", "agron1.com →", "agron1.com →", "agron1.com →", "agron1.com →", "agron1.com →", "agron1.com →", "agron1.com →", "agron1.com →")
Q("Aerial-Ground Robotics Operations Network · agron1.com", "Aerial-Ground Robotics Operations Network · agron1.com", "Aerial-Ground Robotics Operations Network · agron1.com", "Aerial-Ground Robotics Operations Network · agron1.com", "Aerial-Ground Robotics Operations Network · agron1.com", "Aerial-Ground Robotics Operations Network · agron1.com", "Aerial-Ground Robotics Operations Network · agron1.com", "Aerial-Ground Robotics Operations Network · agron1.com", "Aerial-Ground Robotics Operations Network · agron1.com")
Q("Acquired · Concentric Networks, 2000", "Adquirida · Concentric Networks, 2000", "Übernommen · Concentric Networks, 2000", "Acquise · Concentric Networks, 2000", "Приобретена · Concentric Networks, 2000", "Придбана · Concentric Networks, 2000", "被收购 · Concentric Networks, 2000", "مُستحوذ عليها · Concentric Networks, 2000", "נרכשה · Concentric Networks, 2000")
Q("10 live websites · click any card to visit", "10 sitios activos · haga clic en cualquier tarjeta para visitar", "10 Live-Websites · Klick auf Karte zum Besuch", "10 sites actifs · cliquez sur une carte pour visiter", "10 активных сайтов · нажмите на карточку для перехода", "10 активних сайтів · натисніть на картку для переходу", "10个活跃网站 · 点击任意卡片访问", "10 مواقع نشطة · انقر على أي بطاقة للزيارة", "10 אתרים פעילים · לחצו על כרטיס לביקור")
Q("Data Infrastructure · 1996 — 2000", "Infraestructura de datos · 1996 — 2000", "Dateninfrastruktur · 1996 — 2000", "Infrastructure de données · 1996 — 2000", "Инфраструктура данных · 1996 — 2000", "Інфраструктура даних · 1996 — 2000", "数据基础设施 · 1996 — 2000", "بنية البيانات التحتية · 1996 — 2000", "תשתית נתונים · 1996 — 2000")
Q("Robotics & UAV · 2026 — Present", "Robótica y UAV · 2026 — Presente", "Robotik & UAV · 2026 — heute", "Robotique & UAV · 2026 — Aujourd'hui", "Робототехника и БПЛА · 2026 — настоящее время", "Робототехніка та БПЛА · 2026 — теперішній час", "机器人与UAV · 2026 — 至今", "الروبotics وUAV · 2026 — الحاضر", "רובוטיקה ו-UAV · 2026 — הווה")

# Import extended long-form translations
from i18n_long_translations import LONG  # noqa: E402
from i18n_final_patches import STRING_PATCHES  # noqa: E402

QUALITY.update(LONG)
QUALITY.update(STRING_PATCHES)
# fmt: on


def main() -> None:
    baseline = flatten(build_baseline())
    gaps = load_gaps()

    # Collect unique English strings from gaps
    unique_en: dict[str, None] = {}
    for val in gaps.values():
        unique_en[val] = None

    table: dict[str, dict[str, str]] = {}
    for en in unique_en:
        if should_keep(en):
            entry = {lang: en for lang in LANGS}
        elif en in QUALITY:
            entry = dict(QUALITY[en])
        else:
            # Build from baseline: pick first path with this English value
            path = next(p for p, v in gaps.items() if v == en)
            bl = baseline.get(path, {})
            entry = {}
            for lang in LANGS:
                val = bl.get(lang, en)
                if val == en and lang in ("ru", "uk", "ar", "he") and en in QUALITY:
                    val = QUALITY[en][lang]
                entry[lang] = val
        table[en] = entry

    OUT_PATH.write_text(json.dumps(table, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    missing = [en for en in unique_en if not should_keep(en) and en not in QUALITY and en not in table]
    print(f"Wrote {OUT_PATH} — {len(table)} strings")
    uncovered = [en for en in unique_en if not should_keep(en) and en not in QUALITY]
    print(f"Uncovered quality entries: {len(uncovered)}")


if __name__ == "__main__":
    main()
