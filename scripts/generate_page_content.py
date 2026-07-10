#!/usr/bin/env python3
"""Generate js/page-content.js with multilingual page body content."""
import json
import os

PRESENT = {
    "en": "Present",
    "es": "Actual",
    "de": "Heute",
    "fr": "Aujourd'hui",
    "ru": "настоящее время",
    "uk": "дотепер",
    "zh": "至今",
    "ar": "حتى الآن",
    "he": "עד היום",
}

LANGS = ["en", "es", "de", "fr", "ru", "uk", "zh", "ar", "he"]


def yr(start, end, lang):
    if end == "present":
        return f"{start} — {PRESENT[lang]}"
    return f"{start} — {end}"


def build_en():
    return {
        "ui": {"present": PRESENT["en"]},
        "about": {
            "bioP1": "Michael Kofman is the CEO of Digital Invest Inc. and serves on its Board of Directors. A technological visionary, he is renowned for his dynamic approach to understanding the ever-evolving needs of today's complex market. His expertise spans executive acumen, strategic analysis of emerging technologies and markets, information security and privacy, research, science and development, administration, and investment.",
            "bioP2": "As an entrepreneur, board member, and advisor for both public and private companies, Michael Kofman has successfully established several companies in the United States and Europe. Recently, he embarked on an ambitious project with the creation of Digital Invest, a company dedicated to the bio-mathematical sphere, aimed at transforming outdated approaches in medicine using the latest advancements in science, DNA technologies, AI, and ML.",
            "secBioTitle": "Precision Medicine & Biotechnology",
            "secBioP1": "Prior to Digital Invest, he played a significant role in the success of Biotechnology Group Inc. (2008–2014), a company committed to DNA testing and analysis, process automation for creating genetic profiles, and comprehensive human genetic research. Mr. Kofman is a firm believer in the potential of combining life sciences with the latest technological advancements.",
            "secBioP2": "Under his leadership, successful genetic testing projects have been initiated in Ukraine, Russia, and the Baltic countries. This unique experience is continually enriched with modern technologies and new equipment. In collaboration with Harvard Medical School and Stanford Biomath, Mr. Kofman played a crucial role in developing easily understandable genetic reports for both doctors and patients. This innovative approach has been widely adopted by leading laboratories in the United States and abroad.",
            "secTechTitle": "Technology & Infrastructure",
            "secTechP1": "From 2001 to 2019, Mr. Kofman directed technology strategy for government, defense, and state-owned enterprise programs — including complex technical initiatives for government-owned companies. Following September 11, 2001, he led large-scale government projects centered on big data, secure infrastructure, and high-throughput data centers across the United States and Europe.",
            "secTechP2": "In 2006, Mr. Kofman founded XIBI Group Inc. — a technology company where he served on the board of directors. The American company specializes in data storage and big data management services for large commercial and government organizations.",
            "secTechP3": "From 2000 to 2004, Mr. Kofman led DataPeer Inc. — a data management and storage company offering a wide range of services related to information storage for small and medium-sized businesses. At DataPeer he developed unique technological solutions that facilitated faster information tracking and easier data accessibility for individual end-users and government institutions worldwide.",
            "secTechP4": "In 1996, Mr. Kofman founded 9 Net Avenue Inc. It quickly became one of the world's largest hosting companies. By 2000, 9 Net Avenue was acquired by Concentric Networks (NASDAQ: CNTX), and then by XO Communications (NASDAQ: XOXO), reaching a peak market value of $19.5 billion.",
            "secPost9NetP1": "Following the acquisition of 9 Net Avenue, Mr. Kofman gained extensive experience working with public companies, serving on boards of directors, and participating in strategic decision-making at the highest executive level.",
            "secEarlyTitle": "Early Career & Engineering",
            "secEarlyP1": "From 1994 to 1996, Mr. Kofman served as CEO and Director of Information Technology at Elitan United Inc. — an IT company from Massachusetts, which provided comprehensive strategies and technological services for leading global organizations. He played a pivotal role in developing and managing a scalable infrastructure, leading the company's growth from just nine to over 4,000 employees worldwide.",
            "secEarlyP2": "From 1989 to 1994, he was the founder and CEO of Astra Corp, one of the largest manufacturers of digital transceiver satellite systems in Europe, earning international recognition in the field of satellite devices. His responsibilities encompassed research, operating system development, network software applications, and overall technical strategy.",
            "secEarlyP3": "From 1984 to 1989, Mr. Kofman worked at the shipbuilding plant in Nikolaev, Ukraine, where he actively participated in the development and creation of satellite transceiver systems for transmitting classified information to military ships and back. He was recognized as an electronics engineer of the highest level, receiving the 6th category — the highest recognition at the plant, where 93 thousand people worked.",
            "secResearchTitle": "Research & Patents",
            "secResearchP1": "Michael Kofman is the author of technical papers focused on satellite and optical systems for data transmission. He also received a patent in the field of digital satellite high-definition television (HDTV) systems, which was subsequently acquired by Sony.",
        },
        "ventures": {
            "v1year": yr(2021, "present", "en"),
            "v1role": "Founder & CEO · Board Member",
            "v1p1": "Founded and scaled Digital Invest from inception through a successful IPO. The company is dedicated to the bio-mathematical sphere, transforming medicine through AI, ML, and DNA technologies.",
            "v1highlight": "Top 10 U.S. Precision Medicine Company — 2023",
            "v2year": yr(2008, 2014, "en"),
            "v2role": "CEO & CTO",
            "v2p1": "DNA testing and analysis, automation of genetic profiling, and comprehensive human genetic research. Initiated genetic testing projects in Ukraine, Russia, and the Baltic countries.",
            "v2p2": "Collaborated with Harvard Medical School and Stanford Biomath on genetic reports adopted by leading laboratories worldwide.",
            "v2highlight": "Harvard Medical School & Stanford Biomath Partner",
            "v3year": yr(2006, 2011, "en"),
            "v3role": "Founder & CEO · Board of Directors",
            "v3p1": "Data storage and big data management services for large commercial and government organizations. Established the company as a trusted provider of enterprise data solutions.",
            "v3highlight": "Enterprise & Government Data Solutions",
            "v4year": yr(2000, 2004, "en"),
            "v4role": "Founder & CEO",
            "v4p1": "Data management and storage for small and medium-sized businesses. Developed solutions for faster information tracking and easier data accessibility for end-users and government institutions worldwide.",
            "v4highlight": "Global Data Management Platform",
            "v5year": yr(1996, 2000, "en"),
            "v5role": "Founder & CEO",
            "v5p1": "Built one of the world's largest hosting companies. By 2000, acquired by Concentric Networks (NASDAQ: CNTX), then XO Communications (NASDAQ: XOXO), reaching a peak market value of $19.5 billion.",
            "v5highlight": "Acquired · Peak Value $19.5 Billion",
            "v6year": yr(1994, 1996, "en"),
            "v6role": "CEO & Director of Information Technology",
            "v6p1": "IT company from Massachusetts providing comprehensive strategies and technological services for leading global organizations. Led scalable infrastructure development and global IT operations.",
            "v6highlight": "Global IT Strategy & Infrastructure",
            "v7year": yr(1989, 1994, "en"),
            "v7role": "Founder & CEO",
            "v7p1": "One of Europe's largest manufacturers of digital transceiver satellite systems. Led research, operating system development, network software applications, and overall technical strategy.",
            "v7highlight": "European Satellite Systems Leader",
            "v8year": yr(1984, 1989, "en"),
            "v8role": "Electronics Engineer · Highest Category (6th)",
            "v8p1": "Development and creation of satellite transceiver systems for transmitting classified information to military ships. Recognized as an electronics engineer of the highest level at a plant of 93,000 employees.",
            "v8highlight": "Military Satellite Systems Engineering",
        },
        "career": {
            "t1year": yr(2021, "present", "en"),
            "t1title": "Digital Invest Inc.",
            "t1role": "Founder & CEO",
            "t1desc": "Founded and scaled the company from inception through a successful IPO. Led the full public offering process — legal structuring, financial compliance, investor roadshows, and SEC coordination. Directed design, construction, and operations of multiple data centers in the U.S. and Europe. Built enterprise-level software systems for automation, predictive monitoring, and centralized data control. Achieved consistent financial growth, positioning the company among Top 10 Precision Medicine Companies in the U.S. (2023).",
            "t2year": yr(2001, 2019, "en"),
            "t2title": "GovTech, Defense & State Programs",
            "t2role": "Chief Technology Advisor / Program Architect",
            "t2desc": "Directed technology strategy and delivery for classified and high-sensitivity programs involving U.S. government agencies, allied defense systems, and state-owned enterprises. Headed complex technical projects for government-owned companies across multiple sectors. Following September 11, 2001, led large-scale government initiatives centered on big data, secure communications, predictive analytics, and national-level data integration — including the design, construction, and operation of high-throughput data centers across the United States and Europe. Interfaced with military program officers, technology vendors, and regulatory entities.",
            "t3year": yr(2008, 2014, "en"),
            "t3title": "Biotechnology Group Inc.",
            "t3role": "CEO & CTO",
            "t3desc": "Led DNA testing and analysis, automation of genetic profiling, and comprehensive human genetic research. Initiated genetic testing projects in Ukraine, Russia, and the Baltic countries. Collaborated with Harvard Medical School and Stanford Biomath to develop understandable genetic reports adopted by leading laboratories worldwide.",
            "t4year": yr(2000, 2012, "en"),
            "t4title": "Telecommunications Projects",
            "t4role": "VP of Technology / Regional CTO — Eastern Europe & CIS",
            "t4desc": "Directed national infrastructure rollouts across Canada, Italy, Switzerland, Ukraine, and the Baltic Republics. Oversaw 1,000+ engineering and deployment staff across telecom operations including switching systems, broadband expansion, and cross-border connectivity. Implemented core systems for network redundancy, uptime optimization, and intelligent routing.",
            "t5year": yr(2006, 2011, "en"),
            "t5title": "XIBI Group Inc.",
            "t5role": "Founder & CEO · Board of Directors",
            "t5desc": "Founded a technology company specializing in data storage and big data management services for large commercial and government organizations. Established the company as a trusted provider of enterprise data solutions.",
            "t6year": yr(2000, 2004, "en"),
            "t6title": "DataPeer Inc.",
            "t6role": "Founder & CEO",
            "t6desc": "Established a data management and storage company for SMBs. Developed unique technological solutions for faster information tracking and easier data accessibility for end-users and government institutions worldwide.",
            "t7year": yr(1996, 2000, "en"),
            "t7title": "9 Net Avenue Inc.",
            "t7role": "Founder & CEO",
            "t7desc": "Built one of the world's largest hosting companies. By 2000, acquired by Concentric Networks (NASDAQ: CNTX), then XO Communications (NASDAQ: XOXO), reaching a peak market value of $19.5 billion.",
            "t8year": yr(1994, 1996, "en"),
            "t8title": "Elitan United Inc.",
            "t8role": "CEO & Director of Information Technology",
            "t8desc": "Led comprehensive IT strategies and technological services for leading global organizations from Massachusetts during a period of rapid expansion, building scalable infrastructure and global IT operations.",
            "t9year": yr(1989, 1994, "en"),
            "t9title": "Astra Corp",
            "t9role": "Founder & CEO",
            "t9desc": "Founded one of Europe's largest manufacturers of digital transceiver satellite systems. Led research, operating system development, network software applications, and overall technical strategy, earning international recognition.",
            "t10year": yr(1984, 1989, "en"),
            "t10title": "Nikolaev Shipbuilding Plant",
            "t10role": "Electronics Engineer — 6th Category (Highest)",
            "t10desc": "Developed and created satellite transceiver systems for transmitting classified information to military ships. Recognized as an electronics engineer of the highest level at a plant of 93,000 employees — the beginning of a distinguished career in technology and innovation.",
            "s1title": "Executive Leadership",
            "s1desc": "Dual-sided CEO/CTO management across public and private companies, from startup to IPO and beyond.",
            "s2title": "IPO & Financial Scaling",
            "s2desc": "Full public offering execution — legal structuring, SEC coordination, investor roadshows, and compliance.",
            "s3title": "Platform Architecture",
            "s3desc": "Scalable systems design for enterprise automation, predictive monitoring, and centralized data control.",
            "s4title": "Secure Infrastructure",
            "s4desc": "Data center development and operations for government, military, and high-security commercial platforms.",
        },
        "recognition": {
            "a1title": "Entrepreneur of the Year",
            "a1desc": "Entrepreneur Magazine, 1999 — 2001 — leadership and breakthrough achievements in platform innovation and infrastructure.",
            "a2title": "Top 10 U.S. Precision Medicine Company",
            "a2desc": "Digital Invest Inc. recognized among America's 10 Best Companies in Precision Medicine and Digital Health — 2023.",
            "a3title": "Who's Who in America",
            "a3desc": "Listed, 1999 — 2018 — for exceptional achievements in business creation and development.",
            "a4title": "Who's Who in the World",
            "a4desc": "Listed, 2000 — 2004 — among global leaders in science, engineering, and business innovation.",
            "a5title": "Who's Who in Science & Engineering",
            "a5desc": "Listed, 2000 — 2014 — for contributions to technology, satellite systems, and digital infrastructure.",
            "a6title": "Electronics Engineer — 6th Category",
            "a6desc": "Highest recognition at Nikolaev Shipbuilding Plant (93,000 employees) for satellite transceiver systems engineering.",
            "ip1year": "Patent",
            "ip1title": "Digital Satellite HDTV Systems",
            "ip1role": "Subsequently Acquired by Sony",
            "ip1desc": "Received a patent in the field of digital satellite high-definition television (HDTV) systems. The patent was subsequently acquired by Sony Corporation, validating the innovation's commercial significance.",
            "ip2year": "Publications",
            "ip2title": "Technical Papers",
            "ip2role": "Satellite & Optical Systems",
            "ip2desc": "Author of technical papers focused on satellite and optical systems for data transmission. Research contributions span signal processing, simulation modeling, and automation platforms applied in telecommunications, national infrastructure, and digital health.",
            "ip3year": "Research",
            "ip3title": "International Collaborations",
            "ip3role": "U.S. & Europe",
            "ip3desc": "Engaged in international research collaborations and knowledge transfer initiatives. Developed embedded engineering systems for data acquisition, predictive diagnostics, and cloud-based orchestration across multiple industries.",
            "edu1title": "Doctor of Technical Sciences",
            "edu1desc": "2009 — Ukrainian State Marine Technical University",
            "edu2title": "Ph.D. in Information Technology",
            "edu2desc": "2004 — Ukrainian State Marine Technical University",
            "edu3title": "Master's Degrees",
            "edu3desc": "Electronics, Digital Satellite Systems, and Economics",
            "press1title": "Healthcare Tech Outlook",
            "press1role": "Digital Invest Inc. Feature",
            "press1desc": "Digital Invest Inc. featured as one of America's leading companies in precision medicine and digital health, recognized for innovative approaches to transforming medicine through AI, ML, and DNA technologies.",
            "press1link": "Read Feature →",
            "press2title": "Top Precision Medicine Solutions",
            "press2role": "Industry Recognition",
            "press2desc": "Named among the top precision medicine solutions companies, highlighting Digital Invest's role in advancing bio-mathematical approaches to modern healthcare.",
            "press2link": "View Listing →",
        },
        "contact": {"infoEyebrow": "Contact Information"},
    }


# Translations keyed by language code — each mirrors EN structure
TRANSLATIONS = {
    "es": {
        "ui": {"present": PRESENT["es"]},
        "about": {
            "bioP1": "Michael Kofman es CEO de Digital Invest Inc. y miembro de su Consejo de Administración. Visionario tecnológico, es reconocido por su enfoque dinámico para comprender las necesidades en constante evolución del complejo mercado actual. Su experiencia abarca liderazgo ejecutivo, análisis estratégico de tecnologías y mercados emergentes, seguridad de la información y privacidad, investigación, ciencia y desarrollo, administración e inversión.",
            "bioP2": "Como emprendedor, miembro de juntas directivas y asesor de empresas públicas y privadas, Michael Kofman ha fundado con éxito varias compañías en Estados Unidos y Europa. Recientemente emprendió un ambicioso proyecto con la creación de Digital Invest, empresa dedicada a la esfera biomatemática, orientada a transformar enfoques obsoletos en medicina mediante los últimos avances en ciencia, tecnologías de ADN, IA y ML.",
            "secBioTitle": "Medicina de precisión y biotecnología",
            "secBioP1": "Antes de Digital Invest, desempeñó un papel decisivo en el éxito de Biotechnology Group Inc. (2008–2014), empresa dedicada a pruebas y análisis de ADN, automatización de perfiles genéticos e investigación genética humana integral. El Sr. Kofman cree firmemente en el potencial de combinar las ciencias de la vida con los últimos avances tecnológicos.",
            "secBioP2": "Bajo su liderazgo se iniciaron proyectos exitosos de pruebas genéticas en Ucrania, Rusia y los países bálticos. Esta experiencia única se enriquece continuamente con tecnologías modernas y nuevo equipamiento. En colaboración con Harvard Medical School y Stanford Biomath, el Sr. Kofman desempeñó un papel crucial en el desarrollo de informes genéticos comprensibles para médicos y pacientes. Este enfoque innovador ha sido ampliamente adoptado por laboratorios líderes en Estados Unidos y en el extranjero.",
            "secTechTitle": "Tecnología e infraestructura",
            "secTechP1": "De 2001 a 2019, el Sr. Kofman dirigió la estrategia tecnológica de programas gubernamentales, de defensa y de empresas estatales — incluidas iniciativas técnicas complejas para compañías de propiedad estatal. Tras el 11 de septiembre de 2001, lideró proyectos gubernamentales a gran escala centrados en big data, infraestructura segura y centros de datos de alto rendimiento en Estados Unidos y Europa.",
            "secTechP2": "En 2006, el Sr. Kofman fundó XIBI Group Inc. — empresa tecnológica en cuya junta directiva sirvió. La compañía estadounidense se especializa en almacenamiento de datos y servicios de gestión de big data para grandes organizaciones comerciales y gubernamentales.",
            "secTechP3": "De 2000 a 2004, el Sr. Kofman dirigió DataPeer Inc. — empresa de gestión y almacenamiento de datos que ofrecía una amplia gama de servicios de almacenamiento de información para pequeñas y medianas empresas. En DataPeer desarrolló soluciones tecnológicas únicas que facilitaron un seguimiento más rápido de la información y un acceso más sencillo a los datos para usuarios finales e instituciones gubernamentales en todo el mundo.",
            "secTechP4": "En 1996, el Sr. Kofman fundó 9 Net Avenue Inc., que rápidamente se convirtió en una de las mayores empresas de hosting del mundo. En 2000, 9 Net Avenue fue adquirida por Concentric Networks (NASDAQ: CNTX) y posteriormente por XO Communications (NASDAQ: XOXO), alcanzando un valor de mercado máximo de 19,5 mil millones de dólares.",
            "secPost9NetP1": "Tras la adquisición de 9 Net Avenue, el Sr. Kofman adquirió una amplia experiencia trabajando en empresas públicas, participando en juntas directivas y tomando decisiones estratégicas al más alto nivel ejecutivo.",
            "secEarlyTitle": "Primeros años y ingeniería",
            "secEarlyP1": "De 1994 a 1996, el Sr. Kofman fue CEO y Director de Tecnología de la Información en Elitan United Inc. — empresa de TI de Massachusetts que ofrecía estrategias integrales y servicios tecnológicos a organizaciones globales líderes. Desempeñó un papel fundamental en el desarrollo y gestión de infraestructura escalable, llevando el crecimiento de la empresa de solo nueve a más de 4.000 empleados en todo el mundo.",
            "secEarlyP2": "De 1989 a 1994, fue fundador y CEO de Astra Corp, uno de los mayores fabricantes europeos de sistemas satelitales de transcepción digital, con reconocimiento internacional en el campo de dispositivos satelitales. Sus responsabilidades abarcaban investigación, desarrollo de sistemas operativos, aplicaciones de software de red y estrategia técnica general.",
            "secEarlyP3": "De 1984 a 1989, el Sr. Kofman trabajó en el astillero de Nikolaev, Ucrania, donde participó activamente en el desarrollo y creación de sistemas satelitales de transcepción para transmitir información clasificada a buques militares y de regreso. Fue reconocido como ingeniero electrónico del más alto nivel, recibiendo la 6.ª categoría — la máxima distinción en el astillero, donde trabajaban 93 mil personas.",
            "secResearchTitle": "Investigación y patentes",
            "secResearchP1": "Michael Kofman es autor de trabajos técnicos sobre sistemas satelitales y ópticos de transmisión de datos. También obtuvo una patente en el campo de sistemas de televisión de alta definición (HDTV) por satélite digital, posteriormente adquirida por Sony.",
        },
        "ventures": {
            "v1year": yr(2021, "present", "es"), "v1role": "Fundador y CEO · Miembro del consejo",
            "v1p1": "Fundó y escaló Digital Invest desde su inicio hasta una exitosa salida a bolsa. La empresa está dedicada a la esfera biomatemática, transformando la medicina mediante IA, ML y tecnologías de ADN.",
            "v1highlight": "Top 10 empresa de medicina de precisión en EE. UU. — 2023",
            "v2year": yr(2008, 2014, "es"), "v2role": "CEO y CTO",
            "v2p1": "Pruebas y análisis de ADN, automatización de perfiles genéticos e investigación genética humana integral. Inició proyectos de pruebas genéticas en Ucrania, Rusia y los países bálticos.",
            "v2p2": "Colaboró con Harvard Medical School y Stanford Biomath en informes genéticos adoptados por laboratorios líderes en todo el mundo.",
            "v2highlight": "Socio de Harvard Medical School y Stanford Biomath",
            "v3year": yr(2006, 2011, "es"), "v3role": "Fundador y CEO · Consejo de administración",
            "v3p1": "Almacenamiento de datos y servicios de gestión de big data para grandes organizaciones comerciales y gubernamentales. Estableció la empresa como proveedor de confianza de soluciones de datos empresariales.",
            "v3highlight": "Soluciones de datos empresariales y gubernamentales",
            "v4year": yr(2000, 2004, "es"), "v4role": "Fundador y CEO",
            "v4p1": "Gestión y almacenamiento de datos para pequeñas y medianas empresas. Desarrolló soluciones para un seguimiento más rápido de la información y un acceso más sencillo a los datos para usuarios finales e instituciones gubernamentales en todo el mundo.",
            "v4highlight": "Plataforma global de gestión de datos",
            "v5year": yr(1996, 2000, "es"), "v5role": "Fundador y CEO",
            "v5p1": "Construyó una de las mayores empresas de hosting del mundo. En 2000, adquirida por Concentric Networks (NASDAQ: CNTX) y luego por XO Communications (NASDAQ: XOXO), alcanzando un valor de mercado máximo de 19,5 mil millones de dólares.",
            "v5highlight": "Adquirida · Valor máximo de 19,5 mil millones de dólares",
            "v6year": yr(1994, 1996, "es"), "v6role": "CEO y Director de Tecnología de la Información",
            "v6p1": "Empresa de TI de Massachusetts que ofrecía estrategias integrales y servicios tecnológicos a organizaciones globales líderes. Lideró el desarrollo de infraestructura escalable y operaciones de TI globales.",
            "v6highlight": "Estrategia de TI e infraestructura global",
            "v7year": yr(1989, 1994, "es"), "v7role": "Fundador y CEO",
            "v7p1": "Uno de los mayores fabricantes europeos de sistemas satelitales de transcepción digital. Lideró investigación, desarrollo de sistemas operativos, aplicaciones de software de red y estrategia técnica general.",
            "v7highlight": "Líder europeo en sistemas satelitales",
            "v8year": yr(1984, 1989, "es"), "v8role": "Ingeniero electrónico · Categoría máxima (6.ª)",
            "v8p1": "Desarrollo y creación de sistemas satelitales de transcepción para transmitir información clasificada a buques militares. Reconocido como ingeniero electrónico del más alto nivel en un astillero de 93.000 empleados.",
            "v8highlight": "Ingeniería de sistemas satelitales militares",
        },
        "career": {
            "t1year": yr(2021, "present", "es"), "t1title": "Digital Invest Inc.", "t1role": "Fundador y CEO",
            "t1desc": "Fundó y escaló la empresa desde su inicio hasta una exitosa salida a bolsa. Lideró todo el proceso de oferta pública — estructuración legal, cumplimiento financiero, roadshows con inversores y coordinación con la SEC. Dirigió el diseño, construcción y operación de múltiples centros de datos en EE. UU. y Europa. Construyó sistemas de software empresariales para automatización, monitorización predictiva y control centralizado de datos. Logró un crecimiento financiero constante, posicionando la empresa entre las 10 mejores de medicina de precisión en EE. UU. (2023).",
            "t2year": yr(2001, 2019, "es"), "t2title": "GovTech, defensa y programas estatales", "t2role": "Asesor tecnológico principal / Arquitecto de programas",
            "t2desc": "Dirigió la estrategia y ejecución tecnológica de programas clasificados y de alta sensibilidad con agencias gubernamentales de EE. UU., sistemas de defensa aliados y empresas estatales. Encabezó proyectos técnicos complejos para empresas de propiedad estatal en múltiples sectores. Tras el 11 de septiembre de 2001, lideró iniciativas gubernamentales a gran escala centradas en big data, comunicaciones seguras, analítica predictiva e integración de datos a nivel nacional — incluido el diseño, construcción y operación de centros de datos de alto rendimiento en Estados Unidos y Europa. Interactuó con oficiales de programas militares, proveedores tecnológicos y entidades reguladoras.",
            "t3year": yr(2008, 2014, "es"), "t3title": "Biotechnology Group Inc.", "t3role": "CEO y CTO",
            "t3desc": "Lideró pruebas y análisis de ADN, automatización de perfiles genéticos e investigación genética humana integral. Inició proyectos de pruebas genéticas en Ucrania, Rusia y los países bálticos. Colaboró con Harvard Medical School y Stanford Biomath para desarrollar informes genéticos comprensibles adoptados por laboratorios líderes en todo el mundo.",
            "t4year": yr(2000, 2012, "es"), "t4title": "Proyectos de telecomunicaciones", "t4role": "VP de Tecnología / CTO regional — Europa del Este y CEI",
            "t4desc": "Dirigió despliegues de infraestructura nacional en Canadá, Italia, Suiza, Ucrania y las repúblicas bálticas. Supervisó a más de 1.000 ingenieros y personal de despliegue en operaciones de telecomunicaciones, incluidos sistemas de conmutación, expansión de banda ancha y conectividad transfronteriza. Implementó sistemas centrales de redundancia de red, optimización de disponibilidad y enrutamiento inteligente.",
            "t5year": yr(2006, 2011, "es"), "t5title": "XIBI Group Inc.", "t5role": "Fundador y CEO · Consejo de administración",
            "t5desc": "Fundó una empresa tecnológica especializada en almacenamiento de datos y gestión de big data para grandes organizaciones comerciales y gubernamentales. Estableció la empresa como proveedor de confianza de soluciones de datos empresariales.",
            "t6year": yr(2000, 2004, "es"), "t6title": "DataPeer Inc.", "t6role": "Fundador y CEO",
            "t6desc": "Estableció una empresa de gestión y almacenamiento de datos para pymes. Desarrolló soluciones tecnológicas únicas para un seguimiento más rápido de la información y un acceso más sencillo a los datos para usuarios finales e instituciones gubernamentales en todo el mundo.",
            "t7year": yr(1996, 2000, "es"), "t7title": "9 Net Avenue Inc.", "t7role": "Fundador y CEO",
            "t7desc": "Construyó una de las mayores empresas de hosting del mundo. En 2000, adquirida por Concentric Networks (NASDAQ: CNTX) y luego por XO Communications (NASDAQ: XOXO), alcanzando un valor de mercado máximo de 19,5 mil millones de dólares.",
            "t8year": yr(1994, 1996, "es"), "t8title": "Elitan United Inc.", "t8role": "CEO y Director de Tecnología de la Información",
            "t8desc": "Lideró estrategias integrales de TI y servicios tecnológicos para organizaciones globales líderes desde Massachusetts en un período de rápida expansión, construyendo infraestructura escalable y operaciones de TI globales.",
            "t9year": yr(1989, 1994, "es"), "t9title": "Astra Corp", "t9role": "Fundador y CEO",
            "t9desc": "Fundó uno de los mayores fabricantes europeos de sistemas satelitales de transcepción digital. Lideró investigación, desarrollo de sistemas operativos, aplicaciones de software de red y estrategia técnica general, obteniendo reconocimiento internacional.",
            "t10year": yr(1984, 1989, "es"), "t10title": "Astillero de Nikolaev", "t10role": "Ingeniero electrónico — 6.ª categoría (máxima)",
            "t10desc": "Desarrolló y creó sistemas satelitales de transcepción para transmitir información clasificada a buques militares. Reconocido como ingeniero electrónico del más alto nivel en un astillero de 93.000 empleados — el inicio de una distinguida carrera en tecnología e innovación.",
            "s1title": "Liderazgo ejecutivo", "s1desc": "Gestión dual CEO/CTO en empresas públicas y privadas, desde startup hasta IPO y más allá.",
            "s2title": "IPO y escalado financiero", "s2desc": "Ejecución integral de ofertas públicas — estructuración legal, coordinación con la SEC, roadshows con inversores y cumplimiento normativo.",
            "s3title": "Arquitectura de plataformas", "s3desc": "Diseño de sistemas escalables para automatización empresarial, monitorización predictiva y control centralizado de datos.",
            "s4title": "Infraestructura segura", "s4desc": "Desarrollo y operación de centros de datos para plataformas gubernamentales, militares y comerciales de alta seguridad.",
        },
        "recognition": {
            "a1title": "Emprendedor del año", "a1desc": "Entrepreneur Magazine, 1999 — 2001 — liderazgo y logros innovadores en plataformas e infraestructura.",
            "a2title": "Top 10 empresa de medicina de precisión en EE. UU.", "a2desc": "Digital Invest Inc. reconocida entre las 10 mejores empresas de medicina de precisión y salud digital de América — 2023.",
            "a3title": "Who's Who in America", "a3desc": "Incluido, 1999 — 2018 — por logros excepcionales en creación y desarrollo empresarial.",
            "a4title": "Who's Who in the World", "a4desc": "Incluido, 2000 — 2004 — entre líderes globales en ciencia, ingeniería e innovación empresarial.",
            "a5title": "Who's Who in Science & Engineering", "a5desc": "Incluido, 2000 — 2014 — por contribuciones a la tecnología, sistemas satelitales e infraestructura digital.",
            "a6title": "Ingeniero electrónico — 6.ª categoría", "a6desc": "Máximo reconocimiento en el Astillero de Nikolaev (93.000 empleados) por ingeniería de sistemas satelitales de transcepción.",
            "ip1year": "Patente", "ip1title": "Sistemas HDTV satelitales digitales", "ip1role": "Posteriormente adquirida por Sony",
            "ip1desc": "Obtuvo una patente en el campo de sistemas de televisión de alta definición (HDTV) por satélite digital. La patente fue posteriormente adquirida por Sony Corporation, validando la importancia comercial de la innovación.",
            "ip2year": "Publicaciones", "ip2title": "Trabajos técnicos", "ip2role": "Sistemas satelitales y ópticos",
            "ip2desc": "Autor de trabajos técnicos sobre sistemas satelitales y ópticos de transmisión de datos. Sus contribuciones abarcan procesamiento de señales, modelado de simulación y plataformas de automatización aplicadas en telecomunicaciones, infraestructura nacional y salud digital.",
            "ip3year": "Investigación", "ip3title": "Colaboraciones internacionales", "ip3role": "EE. UU. y Europa",
            "ip3desc": "Participó en colaboraciones de investigación internacional e iniciativas de transferencia de conocimiento. Desarrolló sistemas de ingeniería embebidos para adquisición de datos, diagnósticos predictivos y orquestación en la nube en múltiples industrias.",
            "edu1title": "Doctor en Ciencias Técnicas", "edu1desc": "2009 — Universidad Estatal Técnica Marina de Ucrania",
            "edu2title": "Doctorado en Tecnologías de la Información", "edu2desc": "2004 — Universidad Estatal Técnica Marina de Ucrania",
            "edu3title": "Maestrías", "edu3desc": "Electrónica, sistemas satelitales digitales y economía",
            "press1title": "Healthcare Tech Outlook", "press1role": "Reportaje sobre Digital Invest Inc.",
            "press1desc": "Digital Invest Inc. destacada como una de las empresas líderes de América en medicina de precisión y salud digital, reconocida por enfoques innovadores para transformar la medicina mediante IA, ML y tecnologías de ADN.",
            "press1link": "Leer reportaje →",
            "press2title": "Top Precision Medicine Solutions", "press2role": "Reconocimiento del sector",
            "press2desc": "Nombrada entre las principales empresas de soluciones de medicina de precisión, destacando el papel de Digital Invest en el avance de enfoques biomatemáticos en la atención sanitaria moderna.",
            "press2link": "Ver listado →",
        },
        "contact": {"infoEyebrow": "Información de contacto"},
    },
}

# Due to file size, load remaining languages from external JSON if present,
# otherwise the script embeds them inline below.
REMAINING_LANGS_FILE = os.path.join(os.path.dirname(__file__), "page_content_langs.json")

def count_leaves(obj):
    if isinstance(obj, dict):
        return sum(count_leaves(v) for v in obj.values())
    return 1


def load_lang_files():
    langs_dir = os.path.join(os.path.dirname(__file__), "langs")
    loaded = {}
    if os.path.isdir(langs_dir):
        for name in sorted(os.listdir(langs_dir)):
            if name.endswith(".json"):
                code = name[:-5]
                with open(os.path.join(langs_dir, name), encoding="utf-8") as f:
                    loaded[code] = json.load(f)
    return loaded


def main():
    content = {"en": build_en()}
    content.update(TRANSLATIONS)
    content.update(load_lang_files())

    missing = [lang for lang in LANGS if lang not in content]
    if missing:
        raise SystemExit(f"Missing languages: {missing}")

    out = os.path.join(os.path.dirname(__file__), "..", "js", "page-content.js")
    with open(out, "w", encoding="utf-8") as f:
        f.write("const PAGE_CONTENT = ")
        f.write(json.dumps(content, ensure_ascii=False, indent=2))
        f.write(";\n")

    for lang in LANGS:
        print(f"{lang}: {count_leaves(content[lang])} keys")

    print(f"Wrote {out}")


if __name__ == "__main__":
    main()
