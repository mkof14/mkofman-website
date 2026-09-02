#!/usr/bin/env python3
"""Path-based translation patches for keys not covered by gaps or string table."""
from __future__ import annotations

from i18n_constants import T

# flat path -> {lang: translation}
PATH_PATCHES: dict[str, dict[str, str]] = {
    "about.photoServerCaption": T(
        "Entornos de almacenamiento, redes y servidores en DataPeer y empresas relacionadas.",
        "Storage-, Netzwerk- und Serverumgebungen bei DataPeer und verwandten Unternehmen.",
        "Environnements de stockage, réseaux et serveurs chez DataPeer et entreprises associées.",
        "Среды хранения, сетей и серверов в DataPeer и связанных компаниях.",
        "Середовища зберігання, мереж і серверів у DataPeer та пов’язаних компаніях.",
        "DataPeer及相关企业的存储、网络和服务器环境。",
        "بيئات التخزين والشبكات والخوادم في DataPeer والشركات ذات الصلة.",
        "סביבות אחסון, רשתות ושרתים ב-DataPeer ובחברות קשורות.",
    ),
    "caseStudies.cs3resultText": T(
        "Un ecosistema conectado de servicios profesionales que abarca consultoría, desarrollo de capacidades, infraestructura de formación, sistemas geoespaciales e inteligencia marítima a través de AGRON, ISDRI y empresas relacionadas.",
        "Ein vernetztes Professional-Services-Ökosystem für Beratung, Capability Development, Trainingsinfrastruktur, Geospatial-Systeme und Maritime Intelligence über AGRON, ISDRI und verbundene Unternehmen.",
        "Un écosystème de services professionnels couvrant conseil, développement de capacités, infrastructure de formation, systèmes géospatiaux et intelligence maritime via AGRON, ISDRI et entreprises associées.",
        "Связанная экосистема профессиональных услуг: консалтинг, развитие возможностей, инфраструктура обучения, геопространственные системы и морская разведка через AGRON, ISDRI и связанные компании.",
        "Пов’язана екосистема професійних послуг: консалтинг, розвиток можливостей, інфраструктура навчання, геопросторові системи та морська розвідка через AGRON, ISDRI та пов’язані компанії.",
        "通过AGRON、ISDRI及相关公司，涵盖咨询、能力开发、培训基础设施、地理空间系统和海事情报的互联专业服务生态系统。",
        "نظام بيئي متصل للخدمات المهنية يشمل الاستشارات وتطوير القدرات والبنية التدريبية والأنظمة الجغرافية المكانية والاستخبارات البحرية عبر AGRON وISDRI والشركات ذات الصلة.",
        "מערכת אקולוגית מקושרת של שירותים מקצועיים — ייעוץ, פיתוח יכולות, תשתית הכשרה, מערכות geospatial ומודיעין ימי דרך AGRON, ISDRI וחברות קשורות.",
    ),
    "press.clipBody": T(
        "El artículo destaca el reconocimiento como Emprendedor del Año por Entrepreneur Magazine (2001) y analiza el enfoque de DataPeer en almacenamiento crítico, iSCSI y continuidad del negocio.",
        "Der Beitrag erwähnt die Auszeichnung als Unternehmer des Jahres durch Entrepreneur Magazine (2001) und DataPeers Ansatz zu geschäftskritischem Storage, iSCSI und Business Continuity.",
        "L'article note la reconnaissance comme Entrepreneur de l'année par Entrepreneur Magazine (2001) et l'approche de DataPeer en stockage critique, iSCSI et continuité d'activité.",
        "Материал отмечает звание «Предприниматель года» от Entrepreneur Magazine (2001) и подход DataPeer к критически важному хранению, iSCSI и непрерывности бизнеса.",
        "Матеріал відзначає звання «Підприємець року» від Entrepreneur Magazine (2001) і підхід DataPeer до критично важливого зберігання, iSCSI і безперервності бізнесу.",
        "该专题提到2001年获Entrepreneur Magazine年度企业家称号，并讨论DataPeer在关键任务存储、iSCSI和业务连续性方面的方法。",
        "يُشير التقرير إلى تكريم «رائد أعمال العام» من Entrepreneur Magazine (2001)، ويناقش نهج DataPeer في التخزين الحيوي وiSCSI واستمرارية الأعمال.",
        "הכתבה מציינת הכרה כ«יזם השנה» מ-Entrepreneur Magazine (2001) ואת גישת DataPeer לאחסון קריטי, iSCSI והמשכיות עסקית.",
    ),
    "about.secIntroTitle": T(
        "Introducción", "Einführung", "Présentation", "Введение", "Вступ", "简介", "مقدمة", "הקדמה"
    ),
    "about.contactLabel": T(
        "Contacto", "Kontakt", "Contacter", "Контакты", "Контакти", "联系", "تواصل", "יצירת קשר"
    ),
    "contact.eyebrow": T(
        "Contacto", "Kontakt", "Contacter", "Контакты", "Контакти", "联系", "تواصل", "יצירת קשר"
    ),
    "contact.message": T(
        "Mensaje", "Nachricht", "Votre message", "Сообщение", "Повідомлення", "留言", "رسالة", "הודעה"
    ),
    "home.perspectivesEyebrow": T(
        "Perspectivas", "Perspektiven", "Points de vue", "Перспективы", "Перспективи", "观点", "وجهات نظر", "פרספקטיבות"
    ),
    "insights.eyebrow": T(
        "Perspectivas", "Perspektiven", "Points de vue", "Перспективы", "Перспективи", "观点", "وجهات نظر", "פרספקטיבות"
    ),
    "nav.groupServices": T(
        "Servicios", "Leistungen", "Prestations", "Услуги", "Послуги", "服务", "خدمات", "שירותים"
    ),
    "nav.contact": T(
        "Contacto", "Kontakt", "Contacter", "Контакты", "Контакти", "联系", "تواصل", "יצירת קשר"
    ),
    "privacy.s5title": T(
        "Contacto", "Kontakt", "Contacter", "Контакты", "Контакти", "联系", "تواصل", "יצירת קשר"
    ),
    "mediaKit.bioEyebrow": T(
        "Biografías", "Biografien", "Biographies officielles", "Биографии", "Биографії", "传记", "سير ذاتية", "ביוגרפיות"
    ),
    "ip.publicationsEyebrow": T(
        "Publicaciones", "Publikationen", "Ouvrages publiés", "Публикации", "Публікації", "出版物", "منشورات", "פרסומים"
    ),
    "meta.contact.title": T(
        "Contacto — Michael Kofman",
        "Kontakt — Michael Kofman",
        "Contacter — Michael Kofman",
        "Контакты — Michael Kofman",
        "Контакти — Michael Kofman",
        "联系 — Michael Kofman",
        "تواصل — Michael Kofman",
        "יצירת קשר — Michael Kofman",
    ),
    "meta.thesis.title": T(
        "Tesis de liderazgo — Michael Kofman",
        "Führungsthese — Michael Kofman",
        "Thèse de leadership — Michael Kofman",
        "Тезис лидерства — Michael Kofman",
        "Тезис лідерства — Michael Kofman",
        "领导力论题 — Michael Kofman",
        "أطروحة القيادة — Michael Kofman",
        "תזת מנהיגות — Michael Kofman",
    ),
    "meta.deck.title": T(
        "Resumen ejecutivo — Michael Kofman",
        "Führungskräfte-Übersicht — Michael Kofman",
        "Aperçu exécutif — Michael Kofman",
        "Исполнительный обзор — Michael Kofman",
        "Виконавчий огляд — Michael Kofman",
        "高管概览 — Michael Kofman",
        "نظرة تنفيذية — Michael Kofman",
        "סקירה מנהלית — Michael Kofman",
    ),
    "footer.navigation": T(
        "Navegación", "Menü", "Menu", "Навигация", "Навігація", "导航", "التنقل", "ניווט"
    ),
    "nav.briefIpo": T(
        "Informe: IPO", "Kurzbericht: IPO", "Note : IPO", "Бриф: IPO", "Бриф: IPO", "简报：IPO", "ملخص: IPO", "תקציר: IPO"
    ),
    "press.y2000type": T(
        "Entrevista", "Gespräch", "Entretien", "Интервью", "Інтерв'ю", "采访", "مقابلة", "ראיון"
    ),
}
