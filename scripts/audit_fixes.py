#!/usr/bin/env python3
"""One-shot i18n and content fixes from site audit (run before build)."""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TRANS = ROOT / "js" / "translations.js"

QUOTE2 = {
    "es": (
        "Empresario del Año — reconocido por liderazgo y logros innovadores "
        "en plataformas e infraestructura."
    ),
    "de": (
        "Unternehmer des Jahres — ausgezeichnet für Führung und "
        "Durchbrüche in Plattforminnovation und Infrastruktur."
    ),
    "fr": (
        "Entrepreneur de l'année — reconnu pour son leadership et ses "
        "réalisations en innovation de plateformes et infrastructure."
    ),
    "uk": (
        "Підприємець року — за лідерство та проривні досягнення в платформних "
        "інноваціях і інфраструктурі."
    ),
    "zh": "年度企业家——因平台创新与基础设施领域的领导力与突破成就而获认可。",
    "ar": (
        "رائد الأعمال للعام — تقديراً للقيادة والإنجازات في ابتكار المنصات "
        "والبنية التحتية."
    ),
    "he": (
        "יזם השנה — הכרה למנהיגות ולהישגים פורצי דרך בחדשנות פלטפורמות "
        "ותשתיות."
    ),
}

QUOTE3 = {
    "es": (
        "Digital Invest Inc. entre las 10 mejores empresas de EE. UU. en "
        "medicina de precisión y salud digital."
    ),
    "de": (
        "Digital Invest Inc. zu den Top-10-Unternehmen der USA in "
        "Präzisionsmedizin und Digital Health."
    ),
    "fr": (
        "Digital Invest Inc. parmi les 10 meilleures entreprises américaines "
        "en médecine de précision et santé numérique."
    ),
    "uk": (
        "Digital Invest Inc. — серед 10 найкращих компаній США в precision "
        "medicine та digital health."
    ),
    "zh": "Digital Invest Inc. 入选美国精准医学与数字健康十大最佳公司。",
    "ar": (
        "Digital Invest Inc. ضمن أفضل 10 شركات أمريكية في الطب الدقيق "
        "والصحة الرقمية."
    ),
    "he": (
        "Digital Invest Inc. בין 10 החברות המובילות בארה\"ב ברפואת דיוק "
        "ובריאות דיגיטלית."
    ),
}

PRIVACY = {
    "es": {
        "meta": {
            "privacy": {
                "title": "Política de privacidad — Michael Kofman",
                "description": "Política de privacidad de mkofman.com: formularios de contacto y analítica.",
            }
        },
        "footer": {"privacy": "Privacidad"},
        "privacy": {
            "eyebrow": "Legal",
            "title": "Política de privacidad",
            "lead": "Cómo mkofman.com trata la información cuando visita el sitio o envía un mensaje.",
            "updated": "Actualizado: julio de 2026",
            "s1title": "Información que recopilamos",
            "s1text": "Al enviar un formulario, recibimos los campos que usted proporciona (nombre, email, mensaje). Si la analítica está activa, podemos recopilar datos de uso anonimizados.",
            "s2title": "Cómo usamos la información",
            "s2text": "Los formularios se usan para responder consultas y mejorar el sitio. No vendemos datos personales.",
            "s3title": "Servicios de terceros",
            "s3text": "Los formularios pueden procesarse con Formspree. La analítica puede usar Plausible o Google Analytics si está configurada.",
            "s4title": "Sus derechos",
            "s4text": "Puede solicitar acceso, corrección o eliminación escribiendo a mkofman@mkofman.com.",
            "s5title": "Contacto",
            "s5text": "Preguntas sobre esta política: mkofman@mkofman.com",
        },
    },
    "de": {
        "meta": {
            "privacy": {
                "title": "Datenschutz — Michael Kofman",
                "description": "Datenschutzerklärung für mkofman.com — Kontaktformulare und Analyse.",
            }
        },
        "footer": {"privacy": "Datenschutz"},
        "privacy": {
            "eyebrow": "Rechtliches",
            "title": "Datenschutzerklärung",
            "lead": "Wie mkofman.com Informationen verarbeitet, wenn Sie die Website besuchen oder eine Nachricht senden.",
            "updated": "Stand: Juli 2026",
            "s1title": "Welche Daten wir erheben",
            "s1text": "Bei Formularübermittlungen erhalten wir die von Ihnen angegebenen Felder. Bei aktivierter Analyse anonymisierte Nutzungsdaten.",
            "s2title": "Verwendung der Daten",
            "s2text": "Formulare dienen der Beantwortung von Anfragen und der Verbesserung der Website. Wir verkaufen keine personenbezogenen Daten.",
            "s3title": "Drittanbieter",
            "s3text": "Formulare können über Formspree verarbeitet werden. Analyse optional über Plausible oder Google Analytics.",
            "s4title": "Ihre Rechte",
            "s4text": "Auskunft, Berichtigung oder Löschung: mkofman@mkofman.com.",
            "s5title": "Kontakt",
            "s5text": "Fragen zu dieser Richtlinie: mkofman@mkofman.com",
        },
    },
    "fr": {
        "meta": {
            "privacy": {
                "title": "Politique de confidentialité — Michael Kofman",
                "description": "Politique de confidentialité de mkofman.com — formulaires et analytique.",
            }
        },
        "footer": {"privacy": "Confidentialité"},
        "privacy": {
            "eyebrow": "Mentions légales",
            "title": "Politique de confidentialité",
            "lead": "Comment mkofman.com traite les informations lors de votre visite ou de l'envoi d'un message.",
            "updated": "Mise à jour : juillet 2026",
            "s1title": "Informations collectées",
            "s1text": "Lors de l'envoi d'un formulaire, nous recevons les champs fournis. Si l'analytique est activée, des données d'usage anonymisées peuvent être collectées.",
            "s2title": "Utilisation des informations",
            "s2text": "Les formulaires servent à répondre aux demandes et à améliorer le site. Nous ne vendons pas de données personnelles.",
            "s3title": "Services tiers",
            "s3text": "Les formulaires peuvent être traités par Formspree. Analytique via Plausible ou Google Analytics si configurée.",
            "s4title": "Vos droits",
            "s4text": "Accès, rectification ou suppression : mkofman@mkofman.com.",
            "s5title": "Contact",
            "s5text": "Questions sur cette politique : mkofman@mkofman.com",
        },
    },
    "uk": {
        "meta": {
            "privacy": {
                "title": "Політика конфіденційності — Michael Kofman",
                "description": "Політика конфіденційності mkofman.com — форми та аналітика.",
            }
        },
        "footer": {"privacy": "Конфіденційність"},
        "privacy": {
            "eyebrow": "Правова інформація",
            "title": "Політика конфіденційності",
            "lead": "Як mkofman.com обробляє інформацію під час відвідування сайту або надсилання повідомлення.",
            "updated": "Оновлено: липень 2026",
            "s1title": "Які дані збираємо",
            "s1text": "Під час надсилання форми отримуємо вказані вами поля. За увімкненої аналітики — анонімізовані дані відвідувань.",
            "s2title": "Як використовуємо дані",
            "s2text": "Для відповіді на запити та покращення сайту. Персональні дані не продаємо.",
            "s3title": "Сторонні сервіси",
            "s3text": "Форми можуть оброблятися Formspree. Аналітика — Plausible або Google Analytics за налаштуванням.",
            "s4title": "Ваші права",
            "s4text": "Запит доступу, виправлення або видалення: mkofman@mkofman.com.",
            "s5title": "Контакт",
            "s5text": "Питання щодо політики: mkofman@mkofman.com",
        },
    },
    "zh": {
        "meta": {
            "privacy": {
                "title": "隐私政策 — Michael Kofman",
                "description": "mkofman.com 隐私政策——联系表单与分析说明。",
            }
        },
        "footer": {"privacy": "隐私政策"},
        "privacy": {
            "eyebrow": "法律信息",
            "title": "隐私政策",
            "lead": "说明 mkofman.com 在您访问网站或发送消息时如何处理信息。",
            "updated": "更新：2026年7月",
            "s1title": "我们收集的信息",
            "s1text": "提交表单时，我们接收您填写的字段。若启用分析，可能收集匿名使用数据。",
            "s2title": "信息用途",
            "s2text": "用于回复咨询并改进网站。我们不出售个人数据。",
            "s3title": "第三方服务",
            "s3text": "表单可能由 Formspree 处理。分析可使用 Plausible 或 Google Analytics（如已配置）。",
            "s4title": "您的权利",
            "s4text": "访问、更正或删除数据请联系 mkofman@mkofman.com。",
            "s5title": "联系",
            "s5text": "政策相关问题：mkofman@mkofman.com",
        },
    },
    "ar": {
        "meta": {
            "privacy": {
                "title": "سياسة الخصوصية — Michael Kofman",
                "description": "سياسة خصوصية mkofman.com — النماذج والتحليلات.",
            }
        },
        "footer": {"privacy": "الخصوصية"},
        "privacy": {
            "eyebrow": "قانوني",
            "title": "سياسة الخصوصية",
            "lead": "كيف يتعامل mkofman.com مع المعلومات عند زيارة الموقع أو إرسال رسالة.",
            "updated": "آخر تحديث: يوليو 2026",
            "s1title": "المعلومات التي نجمعها",
            "s1text": "عند إرسال نموذج، نتلقى الحقول التي تقدمها. إذا كانت التحليلات مفعّلة، قد نجمع بيانات استخدام مجهولة.",
            "s2title": "كيف نستخدم المعلومات",
            "s2text": "للرد على الاستفسارات وتحسين الموقع. لا نبيع البيانات الشخصية.",
            "s3title": "خدمات طرف ثالث",
            "s3text": "قد تُعالَج النماذج عبر Formspree. التحليلات عبر Plausible أو Google Analytics عند التفعيل.",
            "s4title": "حقوقك",
            "s4text": "طلب الوصول أو التصحيح أو الحذف: mkofman@mkofman.com.",
            "s5title": "اتصل بنا",
            "s5text": "أسئلة حول هذه السياسة: mkofman@mkofman.com",
        },
    },
    "he": {
        "meta": {
            "privacy": {
                "title": "מדיניות פרטיות — Michael Kofman",
                "description": "מדיניות פרטיות של mkofman.com — טפסים ואנליטיקה.",
            }
        },
        "footer": {"privacy": "פרטיות"},
        "privacy": {
            "eyebrow": "משפטי",
            "title": "מדיניות פרטיות",
            "lead": "כיצד mkofman.com מטפל במידע בעת ביקור באתר או שליחת הודעה.",
            "updated": "עודכן: יולי 2026",
            "s1title": "מידע שאנו אוספים",
            "s1text": "בשליחת טופס אנו מקבלים את השדות שמילאת. אם אנליטיקה מופעלת — נתוני שימוש אנונימיים.",
            "s2title": "שימוש במידע",
            "s2text": "למענה לפניות ושיפור האתר. איננו מוכרים מידע אישי.",
            "s3title": "שירותי צד שלישי",
            "s3text": "טפסים עשויים להיות מעובדים ב-Formspree. אנליטיקה — Plausible או Google Analytics.",
            "s4title": "זכויותיך",
            "s4text": "בקשת גישה, תיקון או מחיקה: mkofman@mkofman.com.",
            "s5title": "יצירת קשר",
            "s5text": "שאלות על מדיניות זו: mkofman@mkofman.com",
        },
    },
}

BRIEF_EYEBROW = {
    "es": "Informe ejecutivo",
    "de": "Executive Brief",
    "fr": "Note exécutive",
    "ru": "Исполнительный бриф",
    "uk": "Виконавчий бриф",
    "zh": "高管简报",
    "ar": "ملخص تنفيذي",
    "he": "תקציר מנהלים",
}

V5_LESSON = {
    "en": "Lesson: infrastructure scale is earned through operational excellence long before the exit.",
    "es": "Lección: la escala en infraestructura se gana con excelencia operativa mucho antes de la salida.",
    "de": "Lehre: Infrastruktur-Skalierung entsteht durch operative Exzellenz lange vor dem Exit.",
    "fr": "Leçon : l'échelle en infrastructure se gagne par l'excellence opérationnelle bien avant la sortie.",
    "ru": "Урок: масштаб в инфраструктуре создаётся операционным совершенством задолго до exit.",
    "uk": "Урок: масштаб у інфраструктурі досягається операційною досконалістю задовго до exit.",
    "zh": "经验：基础设施的规模来自长期运营卓越，而非退出前的冲刺。",
    "ar": "الدرس: نمو البنية التحتية يُبنى بالتميز التشغيلي قبل الخروج بكثير.",
    "he": "לקח: קנה מידה בתשתיות נבנה במצוינות תפעולית הרבה לפני יציאה.",
}


def parse_translations() -> dict:
    raw = TRANS.read_text(encoding="utf-8")
    start, end = raw.find("{"), raw.rfind("}")
    return json.loads(raw[start : end + 1])


def write_translations(data: dict) -> None:
    body = json.dumps(data, ensure_ascii=False, indent=2)
    TRANS.write_text(f"const TRANSLATIONS = {body};\n", encoding="utf-8")


def deep_merge(target: dict, source: dict) -> None:
    for key, val in source.items():
        if key in target and isinstance(target[key], dict) and isinstance(val, dict):
            deep_merge(target[key], val)
        else:
            target[key] = val


def fill_missing(target: dict, source: dict) -> None:
    for key, val in source.items():
        if key not in target:
            target[key] = json.loads(json.dumps(val))
        elif isinstance(val, dict) and isinstance(target.get(key), dict):
            fill_missing(target[key], val)


def main() -> None:
    data = parse_translations()
    en = data["en"]

    for lang in data:
        if lang == "en":
            continue
        fill_missing(data[lang], en)

    for lang, patch in PRIVACY.items():
        if lang in data:
            deep_merge(data[lang], patch)

    for lang in QUOTE2:
        if lang in data and "home" in data[lang]:
            data[lang]["home"]["quote2text"] = QUOTE2[lang]
            data[lang]["home"]["quote3text"] = QUOTE3[lang]

    for lang, text in V5_LESSON.items():
        if lang in data and "ventures" in data[lang]:
            data[lang]["ventures"]["v5lesson"] = text

    for lang in data:
        for brief in ("briefIpo", "briefGenetic", "briefAi"):
            if brief in data[lang] and isinstance(data[lang][brief], dict):
                if lang == "en":
                    data[lang][brief]["eyebrow"] = "Executive Brief"
                elif lang in BRIEF_EYEBROW:
                    data[lang][brief]["eyebrow"] = BRIEF_EYEBROW[lang]

    # RU/UK caseStudies cs3 + mediaKit download + meta.deck + nav.ip
    cs3_ru = {
        "cs3eyebrow": "Робототехника и БПЛА · 2026 — настоящее время",
        "cs3title": "AGRON Inc.",
        "cs3challenge": "Задача",
        "cs3challengeText": "Создать экосистему для разработки БПЛА, геопространственных систем и морской разведки.",
        "cs3action": "Подход",
        "cs3actionText": "AGRON Ecosystem объединяет Global Drone Academy, AGRON, ISDRI и GUARD.",
        "cs3result": "Результат",
        "cs3resultText": "Программы в 10+ странах, более 10 000 операторов и специалистов БПЛА.",
    }
    if "ru" in data:
        deep_merge(data["ru"].setdefault("caseStudies", {}), cs3_ru)
        data["ru"].setdefault("home", {})["cs3title"] = "AGRON Inc."
        data["ru"].setdefault("home", {})["cs3desc"] = (
            "Основана в 2026 году — экосистема AGRON для БПЛА, геопространственных систем и морской разведки."
        )
        data["ru"].setdefault("nav", {})["ip"] = "Интеллектуальная собственность"
        mk = data["ru"].setdefault("mediaKit", {})
        mk.setdefault("downloadEyebrow", "Скачать")
        mk.setdefault("downloadTitle", "Медиа-кит в PDF")
        mk.setdefault("downloadLead", "PDF с биографиями, портретом и контактами для прессы.")
        mk.setdefault("downloadCta", "Скачать PDF")

    cs3_uk = {
        "cs3eyebrow": "Робототехніка та БПЛА · 2026 — сьогодні",
        "cs3title": "AGRON Inc.",
        "cs3challenge": "Завдання",
        "cs3challengeText": "Створити екосистему для розробки БПЛА, геопространственних систем і морської розвідки.",
        "cs3action": "Підхід",
        "cs3actionText": "AGRON Ecosystem об'єднує Global Drone Academy, AGRON, ISDRI та GUARD.",
        "cs3result": "Результат",
        "cs3resultText": "Програми у 10+ країнах, понад 10 000 операторів і фахівців БПЛА.",
    }
    if "uk" in data:
        deep_merge(data["uk"].setdefault("caseStudies", {}), cs3_uk)
        data["uk"].setdefault("home", {})["cs3title"] = "AGRON Inc."
        data["uk"].setdefault("home", {})["cs3desc"] = (
            "Заснована у 2026 році — екосистема AGRON для БПЛА, геопространствених систем і морської розвідки."
        )
        data["uk"].setdefault("nav", {})["ip"] = "Інтелектуальна власність"
        mk = data["uk"].setdefault("mediaKit", {})
        mk.setdefault("downloadEyebrow", "Завантажити")
        mk.setdefault("downloadTitle", "Медіа-кит PDF")
        mk.setdefault("downloadLead", "PDF з біографіями, портретом і контактами для преси.")
        mk.setdefault("downloadCta", "Завантажити PDF")

    write_translations(data)
    print("audit_fixes: translations.js updated")


if __name__ == "__main__":
    main()
