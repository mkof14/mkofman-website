#!/usr/bin/env python3
"""Apply locale patches and translate page-content for all languages."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

PAGE_ABOUT = {
    "es": {
        "bioP1": "Michael Kofman es ejecutivo tecnológico, fundador y asesor de consejos. Es CEO de Digital Invest Inc. y fundador de AGRON Inc., con experiencia previa en ingeniería satelital, infraestructura de internet, empresas tecnológicas públicas y ciencias de la vida en EE. UU. y Europa.",
        "secTechP1": "Formación en ingeniería de sistemas transceptores satelitales en Nikolaev Shipbuilding Plant y comunicaciones digitales en Astra Corp.",
        "secBusinessP1": "Fundó y dirigió múltiples empresas tecnológicas, incluidas 9 Net Avenue Inc., DataPeer Inc., XIBI Group Inc. y Elitan United Inc. La cronología completa está en The Record.",
        "secCurrentP1": "CEO de Digital Invest Inc., enfocado en medicina biomatemática e inteligencia genómica. Fundador de AGRON Inc., en operaciones autónomas aéreo-terrestres y sistemas geoespaciales.",
        "secBackgroundP1": "Doctor en Ciencias Técnicas (2009) y Ph.D. en Tecnologías de la Información (2004), Ukrainian State Marine Technical University. Autor de trabajos técnicos; patente en HDTV satelital digital adquirida por Sony.",
    },
    "de": {
        "bioP1": "Michael Kofman ist Technologie-Executive, Gründer und Board-Berater. Er ist CEO von Digital Invest Inc. und Gründer von AGRON Inc., mit Erfahrung in Satelliteningenieurwesen, Internetinfrastruktur, börsennotierten Technologieunternehmen und Life Sciences in den USA und Europa.",
        "secTechP1": "Ingenieur-Hintergrund in Satellitentransceiver-Systemen am Nikolaev Shipbuilding Plant und digitale Kommunikation bei Astra Corp.",
        "secBusinessP1": "Gründete und leitete mehrere Technologieunternehmen, darunter 9 Net Avenue Inc., DataPeer Inc., XIBI Group Inc. und Elitan United Inc. Vollständige Chronologie in The Record.",
        "secCurrentP1": "CEO von Digital Invest Inc. in biomathematischer Medizin und genomischer Intelligenz. Gründer von AGRON Inc. in autonomen Luft-Boden-Operationen und geospatialen Systemen.",
        "secBackgroundP1": "Doctor of Technical Sciences (2009) und Ph.D. in Information Technology (2004), Ukrainian State Marine Technical University. Autor technischer Arbeiten; Patent in digitalem Satelliten-HDTV, übernommen von Sony.",
    },
    "fr": {
        "bioP1": "Michael Kofman est dirigeant technologique, fondateur et conseiller. Il est CEO de Digital Invest Inc. et fondateur d'AGRON Inc., avec une expérience en ingénierie satellitaire, infrastructure internet, sociétés technologiques cotées et sciences de la vie aux États-Unis et en Europe.",
        "secTechP1": "Formation en systèmes émetteurs-récepteurs satellitaires au Nikolaev Shipbuilding Plant et communications numériques chez Astra Corp.",
        "secBusinessP1": "A fondé et dirigé plusieurs entreprises technologiques, dont 9 Net Avenue Inc., DataPeer Inc., XIBI Group Inc. et Elitan United Inc. Chronologie complète dans The Record.",
        "secCurrentP1": "CEO de Digital Invest Inc. en médecine biomathématique et intelligence génomique. Fondateur d'AGRON Inc. en opérations autonomes aéro-terrestres et systèmes géospatiaux.",
        "secBackgroundP1": "Doctor of Technical Sciences (2009) et Ph.D. in Information Technology (2004), Ukrainian State Marine Technical University. Auteur de travaux techniques; brevet HDTV satellitaire acquis par Sony.",
    },
    "ru": {
        "bioP1": "Michael Kofman — технологический executive, основатель и советник. CEO Digital Invest Inc. и основатель AGRON Inc.; опыт в спутниковой инженерии, интернет-инфраструктуре, публичных технологических компаниях и life sciences в США и Европе.",
        "secTechP1": "Инженерный background: спутниковые трансиверы на Nikolaev Shipbuilding Plant и цифровые коммуникации в Astra Corp.",
        "secBusinessP1": "Основал и возглавлял технологические компании, включая 9 Net Avenue Inc., DataPeer Inc., XIBI Group Inc. и Elitan United Inc. Полная хронология — в The Record.",
        "secCurrentP1": "CEO Digital Invest Inc. в биоматематической медицине и геномной аналитике. Основатель AGRON Inc. в автономных воздушно-наземных операциях и геопространственных системах.",
        "secBackgroundP1": "Doctor of Technical Sciences (2009) и Ph.D. in Information Technology (2004), Ukrainian State Marine Technical University. Автор технических работ; патент в digital satellite HDTV, приобретённый Sony.",
    },
    "uk": {
        "bioP1": "Michael Kofman — технологічний executive, засновник і радник. CEO Digital Invest Inc. і засновник AGRON Inc.; досвід у супутниковій інженерії, інтернет-інфраструктурі, публічних технологічних компаніях і life sciences у США та Європі.",
        "secTechP1": "Інженерна підготовка: супутникові трансивери на Nikolaev Shipbuilding Plant і цифрові комунікації в Astra Corp.",
        "secBusinessP1": "Заснував і очолював технологічні компанії, зокрема 9 Net Avenue Inc., DataPeer Inc., XIBI Group Inc. і Elitan United Inc. Повна хронологія — у The Record.",
        "secCurrentP1": "CEO Digital Invest Inc. у біоматематичній медицині та геномній аналітиці. Засновник AGRON Inc. в автономних повітряно-наземних операціях і геопросторових системах.",
        "secBackgroundP1": "Doctor of Technical Sciences (2009) і Ph.D. in Information Technology (2004), Ukrainian State Marine Technical University. Автор технічних робіт; патент у digital satellite HDTV, придбаний Sony.",
    },
    "zh": {
        "bioP1": "Michael Kofman 是技术高管、创始人和董事会顾问。现任 Digital Invest Inc. CEO 和 AGRON Inc. 创始人，此前工作涵盖卫星工程、互联网基础设施、公开科技公司和生命科学。",
        "secTechP1": "工程背景包括 Nikolaev Shipbuilding Plant 的卫星收发器系统和 Astra Corp 的数字通信工作。",
        "secBusinessP1": "创立并领导多家科技公司，包括 9 Net Avenue Inc.、DataPeer Inc.、XIBI Group Inc. 和 Elitan United Inc。完整年表见 The Record。",
        "secCurrentP1": "Digital Invest Inc. CEO，专注生物数学医学和基因组智能。AGRON Inc. 创始人，从事自主空地作业和地理空间系统。",
        "secBackgroundP1": "技术科学博士（2009）和信息技术博士（2004），乌克兰国立海洋技术大学。著有技术论文；数字卫星 HDTV 专利被 Sony 收购。",
    },
    "ar": {
        "bioP1": "Michael Kofman تنفيذي تقني ومؤسس ومستشار. CEO لـ Digital Invest Inc. ومؤسس AGRON Inc.، مع خبرة في هندسة الأقمار الصناعية وبنية الإنترنت والشركات التقنية العامة وعلوم الحياة.",
        "secTechP1": "خلفية هندسية في أنظمة transceiver للأقمار الصناعية واتصالات رقمية في Astra Corp.",
        "secBusinessP1": "أسس وقاد عدة شركات تقنية. السجل الكامل في The Record.",
        "secCurrentP1": "CEO لـ Digital Invest Inc. في الطب الرياضي الحيوي والذكاء الجينومي. مؤسس AGRON Inc. في العمليات المستقلة جواً-أرضاً.",
        "secBackgroundP1": "Doctor of Technical Sciences (2009) و Ph.D. in Information Technology (2004). مؤلف أوراق تقنية؛ براءة HDTV فضائية acquired by Sony.",
    },
    "he": {
        "bioP1": "Michael Kofman הוא מנהיג טכנולוגי, מייסד ויועץ. CEO של Digital Invest Inc. ומייסד AGRON Inc., עם ניסיון בהנדסת לוויינים, תשתיות אינטרנט, חברות ציבוריות ומדעי החיים.",
        "secTechP1": "רקע הנדסי במערכות transceiver לווייניות ותקשורת דיגיטלית ב-Astra Corp.",
        "secBusinessP1": "ייסד והנהיג חברות טכנולוגיה רבות. כרונולוגיה מלאה ב-The Record.",
        "secCurrentP1": "CEO של Digital Invest Inc. ברפואה ביו-מתמטית ואינטליגנציה גénomית. מייסד AGRON Inc. בפעילות אווירית-קרקעית אוטונומית.",
        "secBackgroundP1": "Doctor of Technical Sciences (2009) ו-Ph.D. in Information Technology (2004). מחבר מאמרים טכניים; פטנט HDTV לווייני נרכש על ידי Sony.",
    },
}

RECOGNITION = {
    "es": {"a1desc": "Entrepreneur Magazine · 2001", "ip1desc": "Patente en sistemas HDTV satelitales digitales, adquirida posteriormente por Sony Corporation.", "press1desc": "Healthcare Tech Outlook sobre Digital Invest Inc. y medicina de precisión (2023)."},
    "de": {"a1desc": "Entrepreneur Magazine · 2001", "ip1desc": "Patent für digitale Satelliten-HDTV-Systeme, später von Sony Corporation übernommen.", "press1desc": "Healthcare Tech Outlook über Digital Invest Inc. und Präzisionsmedizin (2023)."},
    "fr": {"a1desc": "Entrepreneur Magazine · 2001", "ip1desc": "Brevet pour systèmes HDTV satellitaires numériques, acquis par Sony Corporation.", "press1desc": "Healthcare Tech Outlook sur Digital Invest Inc. et médecine de précision (2023)."},
    "ru": {"a1desc": "Entrepreneur Magazine · 2001", "ip1desc": "Патент в области digital satellite HDTV, впоследствии приобретённый Sony Corporation.", "press1desc": "Healthcare Tech Outlook о Digital Invest Inc. и precision medicine (2023)."},
    "uk": {"a1desc": "Entrepreneur Magazine · 2001", "ip1desc": "Патент у сфері digital satellite HDTV, згодом придбаний Sony Corporation.", "press1desc": "Healthcare Tech Outlook про Digital Invest Inc. і precision medicine (2023)."},
    "zh": {"a1desc": "Entrepreneur Magazine · 2001", "ip1desc": "数字卫星 HDTV 系统专利，后被 Sony Corporation 收购。", "press1desc": "Healthcare Tech Outlook 关于 Digital Invest Inc. 和精准医疗（2023）。"},
    "ar": {"a1desc": "Entrepreneur Magazine · 2001", "ip1desc": "براءة في أنظمة HDTV فضائية رقمية، استحوذت عليها Sony Corporation.", "press1desc": "Healthcare Tech Outlook عن Digital Invest Inc. (2023)."},
    "he": {"a1desc": "Entrepreneur Magazine · 2001", "ip1desc": "פטנט במערכות HDTV לווייני דיגיטלי, נרכש על ידי Sony Corporation.", "press1desc": "Healthcare Tech Outlook על Digital Invest Inc. (2023)."},
}


def deep_merge(target: dict, source: dict) -> None:
    for k, v in source.items():
        if isinstance(v, dict) and isinstance(target.get(k), dict):
            deep_merge(target[k], v)
        else:
            target[k] = v


def load_json_js(path: Path) -> dict:
    raw = path.read_text(encoding="utf-8")
    return json.loads(raw[raw.find("{") : raw.rfind("}") + 1])


def main() -> None:
    patches = json.loads((ROOT / "scripts" / "locale_patches.json").read_text(encoding="utf-8"))
    trans_path = ROOT / "js" / "translations.js"
    data = load_json_js(trans_path)

    for lang, patch in patches.items():
        if lang in data:
            deep_merge(data[lang], patch)

    trans_path.write_text(
        "const TRANSLATIONS = " + json.dumps(data, ensure_ascii=False, indent=2) + ";\n",
        encoding="utf-8",
    )

    pc_path = ROOT / "js" / "page-content.js"
    pc = load_json_js(pc_path)
    for lang, about in PAGE_ABOUT.items():
        if lang in pc:
            pc[lang].setdefault("about", {}).update(about)
        if lang in RECOGNITION:
            pc[lang].setdefault("recognition", {}).update(RECOGNITION[lang])
    pc_path.write_text(
        "const PAGE_CONTENT = " + json.dumps(pc, ensure_ascii=False, indent=2) + ";\n",
        encoding="utf-8",
    )
    print("translate_all: patched translations + page-content")


if __name__ == "__main__":
    main()
