#!/usr/bin/env python3
"""Auto-generate remaining long translations from baseline es/de/fr + ru/uk/ar/he map."""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from gen_i18n_gaps_translations import build
from i18n_constants import LANGS, T
from build_string_table import QUALITY, should_keep
from i18n_long_translations import LONG

GAPS = json.loads(Path("/tmp/i18n_gaps.json").read_text())


def flatten_baseline(sectioned):
    flat = {}
    for lang in LANGS:
        for sec, keys in sectioned[lang].items():
            if not isinstance(keys, dict):
                continue
            if sec == "meta":
                for k, v in keys.items():
                    flat.setdefault(f"meta.{k}", {})[lang] = v
            else:
                for k, v in keys.items():
                    flat.setdefault(f"{sec}.{k}", {})[lang] = v
    return flat


def first_path(en: str) -> str:
    for sec, keys in GAPS.items():
        for k, v in keys.items():
            if v == en:
                return f"{sec}.{k}"
    raise KeyError(en)


def load_ru_uk_fixes() -> dict[str, dict[str, str]]:
    from i18n_ru_uk_fixes import FIXES  # noqa: WPS433

    out: dict[str, dict[str, str]] = {}
    for sec, langs in FIXES.items():
        for key, val in langs.get("ru", {}).items():
            path = f"{sec}.{key}"
            en = None
            for s, keys in GAPS.items():
                if s == sec and key in keys:
                    en = keys[key]
                    break
            if en:
                out.setdefault(en, {})["ru"] = val
        for key, val in langs.get("uk", {}).items():
            for s, keys in GAPS.items():
                if s == sec and key in keys:
                    en = keys[key]
                    out.setdefault(en, {})["uk"] = val
                    break
    return out


# Slavic/RTL overrides for remaining strings (keyed by English)
EXTRA: dict[str, dict[str, str]] = {}


def add(en: str, ru: str, uk: str, ar: str, he: str) -> None:
    EXTRA[en] = {"ru": ru, "uk": uk, "ar": ar, "he": he}


# Batch add remaining translations
add("Approach", "Подход", "Підхід", "النهج", "גישה")
add("Archive", "Архив", "Архів", "الأرشيف", "ארכיון")
add("Background", "Образование", "Освіта", "الخلفية", "רקע")
add("Brief: AI Strategy", "Бриф: стратегия ИИ", "Бриф: стратегія ШІ", "Brief: استراتيجية AI", "Brief: אסטרטegיית AI")
add("Brief: Genetic Data", "Бриф: генетические данные", "Бриф: генетичні дані", "Brief: البيانات الجينية", "Brief: נתונים גנטיים")
add("Challenge", "Вызов", "Виклик", "التحدي", "אתגר")
add("Choose a Convenient Time", "Выберите удобное время", "Оберіть зручний час", "اختر وقتاً مناسباً", "בחרו זמן נוח")
add("Companies & Public Markets", "Компании и публичные рынки", "Компанії та публічні ринки", "الشركات والأسواق العامة", "חברות ושווקים ציבוריים")
add("Current Work", "Текущая работа", "Поточна робота", "العمل الحالي", "עבודה נוכחית")
add("Engineering & Communications", "Инженерия и коммуникации", "Інженерія та комунікації", "الهندسة والاتصالات", "הנדסה ותקשורת")
add("For advisory inquiries", "По вопросам консалтинга", "Щодо консалтингових запитів", "للاستفسارات الاستشارية", "לפניות ייעוץ")
add("Government & Defense Programs", "Государственные и оборонные программы", "Державні та оборонні програми", "برامج حكومية ودفاعية", "תוכניות ממשלה וביטחון")
add("Inquiry Type", "Тип запроса", "Тип запиту", "نوع الاستفسار", "סוג פנייה")
add("Intellectual Property", "Интеллектуальная собственность", "Інтелектуальна власність", "الملكية الفكرية", "קניין רוחני")
add("Internet & Infrastructure", "Интернет и инфраструктура", "Інтернет та інфраструктура", "الإنترنت والبنية التحتية", "אינטרנט ותשתית")
add("Open Scheduling Calendar", "Открыть календарь встреч", "Відкрити календар зустрічей", "فتح تقويم المواعيد", "פתח יומן תיאומים")
add("Outcome", "Результат", "Результат", "النتيجة", "תוצאה")
add("Press", "Пресса", "Преса", "صحافة", "עיתונות")
add("Public Technology Company", "Публичная технологическая компания", "Публічна технологічна компанія", "شركة تقنية عامة", "חברת טכנולוגיה ציבורית")
add("Schedule a Conversation", "Запланировать разговор", "Запланувати розмову", "جدولة محادثة", "קבע שיחה")
add("Strategic Partner", "Стратегический партнёр", "Стратегічний партнер", "شريك استرategي", "שותף אסטרטגי")
add("Board Colleague", "Коллега по совету директоров", "Колега з ради директорів", "زميل في مجلس الإدارة", "עמית דירקtorיון")
add("Executive Collaborator", "Исполнительный партнёр", "Виконавчий партнер", "متعاون تنفيذي", "שותף executive")
add("Today", "Сегодня", "Сьогодні", "اليوم", "היום")
add("What an IPO Changes", "Что меняет IPO", "Що змінює IPO", "ما يغيره الاكتتاب العام", "מה IPO משנה")
add("Ukrainian State Marine Technical University", "Украинский государственный морской технический университет", "Український державний морський технічний університет", "الجامعة التقنية البحرية الحكومية الأوkrainian", "האוניברסיטה הטכנית הימית הממלכתית של אוקראינה")
add("English, Russian, Ukrainian", "Английский, русский, украинский", "Англійська, російська, українська", "الإنجليزية، الروسية، الأوkrainian", "אנגלית, רוסית, אוקראינית")
add("Entrepreneur Magazine · 2001", "Entrepreneur Magazine · 2001", "Entrepreneur Magazine · 2001", "Entrepreneur Magazine · 2001", "Entrepreneur Magazine · 2001")

# fmt: off
add("Authentic material from company building, infrastructure, and leadership.",
    "Подлинные материалы о создании компаний, инфраструктуре и лидерстве.",
    "Автентичні матеріали про створення компаній, інфраструктуру та лідерство.",
    "مواد أصيلة عن بناء الشركات والبنية التحتية والقيادة.",
    "חומר אותנטי מבניית חברות, תשתיות ומנהיגות.")
add("Open to strategic advisory conversations with technology, healthcare, and infrastructure organizations — drawing on direct operating experience across company building, technology strategy, and growth-stage execution.",
    "Открыт к стратегическим консалтинговым диалогам с технологическими, медицинскими и инфраструктурными организациями — на основе прямого операционного опыта в создании компаний, технологической стратегии и росте.",
    "Відкритий до стратегічних консалтингових діалогів із технологічними, медичними та інфраструктурними організаціями — на основі прямого операційного досвіду у створенні компаній, технологічній стратегії та зростанні.",
    "منفتح على محادثات استشارية استратategية مع منظمات التكنولوجيا والرعاية الصحية والبنية التحtية — استناداً إلى خبرة تشغيلية مباشرة في بناء الشركات واستراتيجية التكنولوجia والتنفيذ في مراحل النمو.",
    "פתוח לשיחות ייעוץ אסטרטegיות עם ארגוני טכנולוגיה, בריאות ותשתיות — על בסיס ניסיון תפעולי ישיר בבניית חברות, אסטרטegיה טכנולוגית וביצוע בשלבי צמיחה.")
add("Organizations building UAV and Counter-UAS capability need independent assessment, structured training, and operational architecture — not isolated platforms or ad-hoc piloting.",
    "Организациям, развивающим возможности UAV и Counter-UAS, нужны независимая оценка, структурированное обучение и операционная архитектура — а не изолированные платформы или ad-hoc пилотирование.",
    "Організаціям, що розвивають можливості UAV і Counter-UAS, потрібні незалежна оцінка, структуроване навчання та операційна архітектура — а не ізольовані платформи чи ad-hoc piloting.",
    "المنظمات التي تبني قدرات UAV وCounter-UAS تحتاج تقييماً مستقلاً وتدريباً منظماً وarchitecture تشغيلية — وليس منصات معزولة أو piloting ad hoc.",
    "ארגונים שבונים יכולות UAV ו-Counter-UAS צריכים הערכה עצמאית, הכשרה מובנית וארכיטקטורה תפעולית — לא פלטפורמות מבודדות או piloting ad hoc.")
# fmt: on


def main() -> None:
    baseline = flatten_baseline(build())
    ru_uk = load_ru_uk_fixes()
    strings = sorted(set(v for s, kv in GAPS.items() for v in kv.values()))
    missing = [s for s in strings if not should_keep(s) and s not in QUALITY and s not in LONG]

    generated = {}
    for en in missing:
        path = first_path(en)
        bl = baseline.get(path, {})
        es = bl.get("es", en)
        de = bl.get("de", es)
        fr = bl.get("fr", es)
        zh = bl.get("zh", es)
        extra = EXTRA.get(en, {})
        ru = extra.get("ru") or ru_uk.get(en, {}).get("ru") or bl.get("ru", es)
        uk = extra.get("uk") or ru_uk.get(en, {}).get("uk") or bl.get("uk", es)
        ar = extra.get("ar") or bl.get("ar", es)
        he = extra.get("he") or bl.get("he", es)
        generated[en] = T(es, de, fr, ru, uk, zh, ar, he)

    out_path = Path(__file__).resolve().parent / "i18n_auto_long.json"
    out_path.write_text(json.dumps(generated, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Generated {len(generated)} entries -> {out_path}")
    still_en = sum(1 for en, m in generated.items() for lang in ("ar", "he") if m[lang] == en)
    print(f"ar/he still identical to EN: {still_en}")


if __name__ == "__main__":
    main()
