#!/usr/bin/env python3
"""Long-form English string translations for i18n string table."""
from i18n_constants import T

# fmt: off
LONG: dict[str, dict[str, str]] = {}

def Q(en, es, de, fr, ru, uk, zh, ar, he):
    LONG[en] = T(es, de, fr, ru, uk, zh, ar, he)

# Privacy policy
Q(
"This policy explains how mkofman.com handles information when you visit the site or send a message.",
"Esta política explica cómo mkofman.com maneja la información cuando visita el sitio o envía un mensaje.",
"Diese Richtlinie erklärt, wie mkofman.com Informationen behandelt, wenn Sie die Website besuchen oder eine Nachricht senden.",
"Cette politique explique comment mkofman.com traite les informations lorsque vous visitez le site ou envoyez un message.",
"Эта политика объясняет, как mkofman.com обрабатывает информацию, когда вы посещаете сайт или отправляете сообщение.",
"Ця політика пояснює, як mkofman.com обробляє інформацію, коли ви відвідуєте сайт або надсилаєте повідомлення.",
"本政策说明当您访问网站或发送消息时，mkofman.com如何处理信息。",
"توضح هذه السياسة كيف يتعامل mkofman.com مع المعلومات عند زيارة الموقع أو إرسال رسالة.",
"מדיניות זו מסבירה כיצד mkofman.com מטפל במידע כשאתם מבקרים באתר או שולחים הודעה.",
)
Q(
"When you submit a contact or footer form, we receive the fields you provide (such as name, email, and message). If analytics are enabled, we may collect anonymized usage data (pages visited, referrer, device type).",
"Al enviar un formulario de contacto o pie de página, recibimos los campos que proporciona (como nombre, email y mensaje). Si la analítica está habilitada, podemos recopilar datos de uso anonimizados (páginas visitadas, referrer, tipo de dispositivo).",
"Beim Absenden eines Kontakt- oder Footer-Formulars erhalten wir die von Ihnen angegebenen Felder (z. B. Name, E-Mail und Nachricht). Wenn Analytics aktiviert ist, können anonymisierte Nutzungsdaten erfasst werden (besuchte Seiten, Referrer, Gerätetyp).",
"Lorsque vous soumettez un formulaire de contact ou de pied de page, nous recevons les champs fournis (nom, email, message). Si l'analytique est activée, nous pouvons collecter des données d'usage anonymisées (pages visitées, referrer, type d'appareil).",
"При отправке контактной формы или формы в footer мы получаем указанные вами поля (имя, email, сообщение). Если analytics включена, мы можем собирать anonymized usage data (посещённые страницы, referrer, тип устройства).",
"Надсилаючи контактну форму або форму в footer, ми отримуємо зазначені вами поля (ім'я, email, повідомлення). Якщо analytics увімкнена, ми можемо збирати anonymized usage data (відвідані сторінки, referrer, тип пристрою).",
"提交联系或页脚表单时，我们会收到您提供的字段（如姓名、电子邮件和留言）。如启用分析，我们可能收集匿名使用数据（访问页面、来源、设备类型）。",
"عند إرسال نموذج اتصال أو تذييل، نتلقى الحقول التي تقدمها (مثل الاسم والبريد الإلكتروني والرسالة). إذا كانت التحليلات مفعّلة، قد نجمع بيانات استخدام anonymized (الصفحات الم visited، المصدر، نوع الجهاز).",
"בשליחת טופס יצירת קשר או תחתית, אנו מקבלים את השדות שסיפקתם (שם, אימייל, הודעה). אם analytics מופעל, אנו עשויים לאסוף נתוני שימוש anonymized (דפים שבוקרו, referrer, סוג מכשיר).",
)
Q(
"Form submissions are used to respond to your inquiry. Analytics help improve the website. We do not sell personal data.",
"Los envíos de formularios se usan para responder a su consulta. La analítica ayuda a mejorar el sitio. No vendemos datos personales.",
"Formularübermittlungen dienen der Beantwortung Ihrer Anfrage. Analytics hilft, die Website zu verbessern. Wir verkaufen keine personenbezogenen Daten.",
"Les soumissions servent à répondre à votre demande. L'analytique aide à améliorer le site. Nous ne vendons pas de données personnelles.",
"Данные форм используются для ответа на ваш запрос. Analytics помогает улучшать сайт. Мы не продаём personal data.",
"Дані форм використовуються для відповіді на ваш запит. Analytics допомагає покращувати сайт. Ми не продаємо personal data.",
"表单提交用于回复您的咨询。分析有助于改进网站。我们不出售个人数据。",
"تُستخدم إرسالات النماذج للرد على استفسارك. تساعد التحليلات في تحسين الموقع. لا نبيع البيانات الشخصية.",
"שליחות טפסים משמשות להשבת לפנייתכם. analytics עוזר לשפר את האתר. איננו מוכרים נתונים אישיים.",
)
Q(
"Forms may be processed by Formspree. Analytics may use Plausible or Google Analytics if configured. These providers have their own privacy policies.",
"Los formularios pueden procesarse mediante Formspree. La analítica puede usar Plausible o Google Analytics si está configurada. Estos proveedores tienen sus propias políticas de privacidad.",
"Formulare können über Formspree verarbeitet werden. Analytics kann Plausible oder Google Analytics nutzen, falls konfiguriert. Diese Anbieter haben eigene Datenschutzrichtlinien.",
"Les formulaires peuvent être traités par Formspree. L'analytique peut utiliser Plausible ou Google Analytics si configuré. Ces fournisseurs ont leurs propres politiques de confidentialité.",
"Формы могут обрабатываться через Formspree. Analytics может использовать Plausible или Google Analytics при наличии настройки. У этих провайдеров собственные privacy policies.",
"Форми можуть оброблятися через Formspree. Analytics може використовувати Plausible або Google Analytics за наявності налаштування. У цих провайдерів власні privacy policies.",
"表单可能由Formspree处理。分析可能使用Plausible或Google Analytics（如已配置）。这些提供商有各自的隐私政策。",
"قد تُعالج النماذج عبر Formspree. قد تستخدم التحليلات Plausible أو Google Analytics إذا تم تكوينها. لهذه الجهات سياسات خصوصية خاصة.",
"טפסים עשויים להיות מעובדים על ידי Formspree. analytics עשוי להשתמש ב-Plausible או Google Analytics אם מוגדר. לספקים אלה מדיניות פרטיות משלהם.",
)
Q(
"You may request access, correction, or deletion of your data by emailing mkofman@mkofman.com.",
"Puede solicitar acceso, corrección o eliminación de sus datos enviando un email a mkofman@mkofman.com.",
"Sie können Zugang, Berichtigung oder Löschung Ihrer Daten per E-Mail an mkofman@mkofman.com anfordern.",
"Vous pouvez demander l'accès, la correction ou la suppression de vos données en écrivant à mkofman@mkofman.com.",
"Вы можете запросить доступ, исправление или удаление данных, написав на mkofman@mkofman.com.",
"Ви можете запросити доступ, виправлення або видалення даних, написавши на mkofman@mkofman.com.",
"您可发送邮件至 mkofman@mkofman.com 请求访问、更正或删除您的数据。",
"يمكنك طلب الوصول إلى بياناتك أو تصحيحها أو حذفها عبر البريد mkofman@mkofman.com.",
"ניתן לבקש גישה, תיקון או מחיקה של הנתונים שלכם במייל mkofman@mkofman.com.",
)
Q(
"Questions about this policy: mkofman@mkofman.com",
"Preguntas sobre esta política: mkofman@mkofman.com",
"Fragen zu dieser Richtlinie: mkofman@mkofman.com",
"Questions sur cette politique : mkofman@mkofman.com",
"Вопросы по этой политике: mkofman@mkofman.com",
"Питання щодо цієї політики: mkofman@mkofman.com",
"有关本政策的问题：mkofman@mkofman.com",
"أسئلة حول هذه السياسة: mkofman@mkofman.com",
"שאלות על מדיניות זו: mkofman@mkofman.com",
)

# Thesis
Q(
"Technology changes quickly; the obligations of leadership do not. Durable enterprises unite ambition with discipline, evidence, and accountability.",
"La tecnología cambia rápido; las obligaciones del liderazgo, no. Las empresas duraderas unen ambición con disciplina, evidencia y responsabilidad.",
"Technologie ändert sich schnell; die Pflichten der Führung nicht. Beständige Unternehmen verbinden Ambition mit Disziplin, Evidenz und Accountability.",
"La technologie change vite ; les obligations du leadership, non. Les entreprises durables unissent ambition, discipline, preuves et responsabilité.",
"Технологии меняются быстро; обязательства лидерства — нет. Устойчивые компании соединяют амбиции с дисциплиной, доказательствами и подотчётностью.",
"Технології змінюються швидко; зобов'язання лідерства — ні. Стійкі компанії поєднують амбіції з дисципліною, доказами та підзвітністю.",
"技术变化迅速；领导力的义务不变。持久企业将雄心与纪律、证据和问责相结合。",
"تتغير التكنولوجيا بسرعة؛ التزامات القيادة لا. توحّد المؤسسات الدائمة الطموح مع الانضباط والأدلة والمساءلة.",
"טכנולוגיה משתנה במהירות; חובות המנהיגות — לא. ארגונים מתמשכים מאחדים שאפתנות עם משמעת, ראיות ואחריות.",
)
Q(
"A strategy is not a catalog of aspirations. It defines where to compete, what capabilities to build, what not to pursue, and how success will be measured.",
"Una estrategia no es un catálogo de aspiraciones. Define dónde competir, qué capacidades construir, qué no perseguir y cómo se medirá el éxito.",
"Strategie ist kein Katalog von Aspirationen. Sie definiert, wo zu konkurrieren ist, welche Fähigkeiten aufzubauen sind, was nicht verfolgt werden soll und wie Erfolg gemessen wird.",
"Une stratégie n'est pas un catalogue d'aspirations. Elle définit où concurrencer, quelles capacités construire, quoi ne pas poursuivre et comment le succès sera mesuré.",
"Стратегия — не каталог амбиций. Она определяет, где конкурировать, какие способности строить, чего не pursue и как измерять успех.",
"Стратегія — не каталог амбіцій. Вона визначає, де конкурувати, які спроможності будувати, чого не pursue і як вимірювати успіх.",
"战略不是愿望清单。它定义在哪里竞争、构建哪些能力、不 pursue 什么以及如何衡量成功。",
"الاستراتيجية ليست catalogاً للطموحات. تحدد أين تتنافس وما القدرات التي تبنيها وما لا ت Pursue وكيف يُقاس النجاح.",
"אסטרטegיה אינה קטalog של שאיפות. היא מגדירה היכן להת конкуруents, אילו יכולות לבנות, מה לא לרדוף וכיצד יימדד הצלחה.",
)
Q(
"Boards must understand how technology creates value, concentrates risk, and changes accountability. Delegating every technical question is itself a decision.",
"Los consejos deben entender cómo la tecnología crea valor, concentra riesgo y cambia la responsabilidad. Delegar cada pregunta técnica es en sí una decisión.",
"Boards müssen verstehen, wie Technologie Wert schafft, Risiko konzentriert und Accountability verändert. Jede technische Frage zu delegieren ist selbst eine Entscheidung.",
"Les conseils doivent comprendre comment la technologie crée de la valeur, concentre le risque et change la responsabilité. Déléguer chaque question technique est déjà une décision.",
"Советы директоров должны понимать, как технология создаёт ценность, концентрирует риск и меняет подотчётность. Делегирование каждого технического вопроса — само по себе решение.",
"Ради директорів мають розуміти, як технологія створює цінність, конcentрує ризик і змінює підзвітність. Делегування кожного технічного питання — само по собі рішення.",
"董事会必须理解技术如何创造价值、集中风险并改变问责。将每个技术问题外包本身就是决策。",
"يجب أن تفهم مجالس الإدارة كيف تخلق التكنولوجيا قيمة وتركّز المخاطر وتغيّر المساءلة. تفويض كل سؤال تقني قرار بحد ذاته.",
"דירקטוריונים חייבים להבין כיצד טכנולוגיה יוצרת ערך, מרכזת סיכון ומשנה אחריות. העברת כל שאלה טכנית לאחרים היא בעצמה החלטה.",
)
Q(
"Conviction matters, but markets, systems, and science must be tested. Leaders create mechanisms that expose assumptions before customers or regulators do.",
"La convicción importa, pero mercados, sistemas y ciencia deben probarse. Los líderes crean mecanismos que exponen supuestos antes que clientes o reguladores.",
"Überzeugung zählt, aber Märkte, Systeme und Wissenschaft müssen getestet werden. Führungskräfte schaffen Mechanismen, die Annahmen sichtbar machen, bevor Kunden oder Regulatoren es tun.",
"La conviction compte, mais marchés, systèmes et science doivent être testés. Les dirigeants créent des mécanismes qui exposent les hypothèses avant clients ou régulateurs.",
"Убеждённость важна, но рынки, системы и науку нужно проверять. Лидеры создают механизмы, выявляющие допущения раньше клиентов или регуляторов.",
"Переконання важливе, але ринки, системи та науку потрібно перевіряти. Лідери створюють механізми, що виявляють припущення раніше клієнтів або регуляторів.",
"信念重要，但市场、系统和科学必须被检验。领导者创建机制，在客户或监管者之前暴露假设。",
"الconviction مهم، لكن الأسواق والأنظمة والعلم يجب اختبارها. يخلق القادة آليات ت expose الافتراضات قبل العملاء أو المنظمين.",
"conviction חשוב, אך שווקים, מערכות ומדע חייבים להיבחן. מנהיגים יוצרים מנגנונים שחושפים הנחות לפני לקוחות או רגulators.",
)
Q(
"Technical architecture determines speed, resilience, security, and future options. Shortcuts become institutional constraints long after their original context disappears.",
"La arquitectura técnica determina velocidad, resiliencia, seguridad y opciones futuras. Los atajos se convierten en restricciones institucionales mucho después de que desaparece su contexto original.",
"Technische Architektur bestimmt Geschwindigkeit, Resilienz, Sicherheit und zukünftige Optionen. Abkürzungen werden zu institutionellen Zwängen lange nach ihrem ursprünglichen Kontext.",
"L'architecture technique détermine vitesse, résilience, sécurité et options futures. Les raccourcis deviennent des contraintes institutionnelles longtemps après leur contexte d'origine.",
"Техническая архитектура определяет скорость, устойчивость, безопасность и будущие опции. Shortcut'ы становятся институциональными ограничениями long after исчезновения их контекста.",
"Технічна архітектура визначає швидкість, стійкість, безпеку та майбутні опції. Shortcut'и стають інституційними обмеженнями long after зникнення їхнього контексту.",
"技术架构决定速度、韧性、安全和未来选项。捷径在其原始背景消失很久后仍会成为制度约束。",
"تحدد البنية التقنية السرعة والمرونة والأمن والخيارات المستقبلية. تصبح الاختصارات قيوداً مؤسسية long after اختفاء سياقها الأصلي.",
"ארכיטקטורה טכנית קובעת מהירות, חוסן, אבטחה ואפשרויות עתיד. קיצורי דרך הופכים לאילוצים מוסדיים long after שההקשר המקורי נעלם.",
)
Q(
"Trust is built through clear commitments, reliable execution, responsible data practices, and direct communication when conditions change.",
"La confianza se construye con compromisos claros, ejecución fiable, prácticas responsables de datos y comunicación directa cuando cambian las condiciones.",
"Vertrauen entsteht durch klare Zusagen, verlässliche Ausführung, verantwortungsvolle Datenpraxis und direkte Kommunikation, wenn sich Bedingungen ändern.",
"La confiance se construit par des engagements clairs, une exécution fiable, des pratiques responsables des données et une communication directe quand les conditions changent.",
"Доверие строится через ясные обязательства, надёжное исполнение, ответственную работу с данными и прямую коммуникацию при изменении условий.",
"Довіра будується через чіткі зobов'язання, надійне виконання, відповідальну роботу з даними та пряму комунікацію при зміні умов.",
"信任通过明确承诺、可靠执行、负责任的数据实践以及在条件变化时的直接沟通来建立。",
"يُبنى الثقة عبر التزامات واضحة وتنفيذ موثوق وممارسات بيانات مسؤولة وتواصل مباشر عند تغيّر الظروف.",
"אמון נבנה דרך התחייבויות ברורות, ביצוע אמין, פרaktikות נתונים אחראיות ותקשורת ישירה כשהתנאים משתנים.",
)
Q(
"Growth investment should reinforce differentiated capabilities and measurable demand, not substitute spending for product-market understanding.",
"La inversión en crecimiento debe reforzar capacidades diferenciadas y demanda medible, no sustituir el gasto por comprensión del producto-mercado.",
"Wachstumsinvestitionen sollten differenzierte Fähigkeiten und messbare Nachfrage stärken, nicht Ausgaben für Product-Market-Understanding ersetzen.",
"L'investissement de croissance doit renforcer des capacités différenciées et une demande mesurable, pas substituer les dépenses à la compréhension produit-marché.",
"Инвестиции в рост должны усиливать дифференцированные способности и измеримый спрос, а не заменять траты пониманием product-market.",
"Інвестиції в зростання мають посилювати диференційовані спроможності та вимірюваний попит, а не замінювати витрати розумінням product-market.",
"增长投资应强化差异化能力和可衡量需求，而非用支出替代产品-市场理解。",
"يجب أن تعزز استثمارات النمو القدرات المتمايزة والطلب القابل للقياس، لا أن تحل الإنفاق محل فهم product-market.",
"השקעות צמיחה צריכות לחזק יכולות differentiated וביקוש measurable, לא להחליף הוצאות בהבנת product-market.",
)
Q(
"The strongest leaders build systems, talent, and decision quality that endure beyond their own involvement.",
"Los líderes más sólidos construyen sistemas, talento y calidad de decisión que perduran más allá de su propia participación.",
"Die stärksten Führungskräfte bauen Systeme, Talent und Entscheidungsqualität, die über ihre eigene Beteiligung hinaus Bestand haben.",
"Les dirigeants les plus solides construisent des systèmes, des talents et une qualité de décision qui perdurent au-delà de leur propre participation.",
"Сильнейшие лидеры строят системы, таланты и качество решений, которые переживают их собственное участие.",
"Найсильніші лідери будують системи, таланти та якість рішень, які переживають їхню власну участь.",
"最强的领导者构建超越自身参与的系统、人才和决策质量。",
"يبني أقوى القادة أنظمة ومواهب وجودة قرار تدوم beyond مشاركتهم.",
"המנהיגים החזקים ביותר בונים מערכות, כישרונות ואיכות החלטה שנשארים מעבר למעורבותם.",
)
Q(
"The defining opportunity is not any single technology. It is the disciplined integration of AI, advanced data systems, biology, and automation into institutions people can trust.",
"La oportunidad definitoria no es una sola tecnología. Es la integración disciplinada de IA, sistemas avanzados de datos, biología y automatización en instituciones en las que la gente puede confiar.",
"Die entscheidende Chance ist nicht eine einzelne Technologie. Es ist die disziplinierte Integration von KI, fortgeschrittenen Datensystemen, Biologie und Automation in Institutionen, denen Menschen vertrauen können.",
"L'opportunité décisive n'est pas une seule technologie. C'est l'intégration disciplinée de l'IA, des systèmes de données avancés, de la biologie et de l'automatisation dans des institutions auxquelles on peut faire confiance.",
"Решающая возможность — не одна технология. Это дисциплинированная интеграция ИИ, продвинутых data systems, биологии и automation в institution, которым люди могут доверять.",
"Визначальна можливість — не одна технологія. Це дисциплінована інтеграція ШІ, просунутих data systems, біології та automation в institution, яким люди можуть довіряти.",
"决定性机遇不是任何单一技术，而是将AI、先进数据系统、生物学和自动化 disciplined 融入人们可信赖的机构。",
"الفرصة الحاسمة ليست technology واحدة. بل التكامل المنضبط للذكاء الاصطناعي وأنظمة البيانات المتقدمة والbiology والautomation في مؤسسات يمكن للناس الوثوق بها.",
"ההזדמנות המכרעת אינה technology בודדת. זו אינטegration ממושמעת של AI, מערכות נתונים מתקדמות, biology ו-automation במוסדות שאנשים יכולים לסמוך עליהם.",
)
Q(
"Announcements, pilots, and fashionable language do not equal capability. Innovation must improve an outcome that matters.",
"Anuncios, pilotos y lenguaje de moda no equivalen a capacidad. La innovación debe mejorar un resultado que importa.",
"Ankündigungen, Piloten und modische Sprache sind keine Fähigkeit. Innovation muss ein Ergebnis verbessern, das zählt.",
"Annonces, pilotes et langage à la mode ne font pas une capacité. L'innovation doit améliorer un résultat qui compte.",
"Анонсы, пилоты и модный язык не равны capability. Инновации должны улучшать результат, который имеет значение.",
"Анонси, пілоти та модна мова не дорівнюють capability. Інновації мають покращувати результат, який має значення.",
"公告、试点和时髦语言不等于能力。创新必须改善重要的结果。",
"الإعلانات وال pilots واللغة العصرية لا ت equal capability. يجب أن تحسّن الابتكار نتيجة مهمة.",
"הכרזות, pilots ושפה אופנתית לא שווים capability. חדשנות חייבת לשפר תוצאה שחשובה.",
)
Q(
"Scale magnifies unresolved weaknesses. Controls, culture, and accountability should mature before complexity makes correction costly.",
"La escala magnifica debilidades no resueltas. Controles, cultura y responsabilidad deben madurar antes de que la complejidad haga costosa la corrección.",
"Skalierung vergrößert ungelöste Schwächen. Controls, Kultur und Accountability sollten reifen, bevor Komplexität Korrektur kostspielig macht.",
"L'échelle amplifie les faiblesses non résolues. Contrôles, culture et responsabilité doivent mûrir avant que la complexité ne rende la correction coûteuse.",
"Масштаб увеличивает нерешённые слабости. Controls, culture и accountability должны созреть, пока complexity не сделает correction costly.",
"Масштаб збільшує невирішені слабкості. Controls, culture і accountability мають дозріти, поки complexity не зробить correction costly.",
"规模放大未解决的弱点。控制、文化和问责应在复杂性使纠正代价高昂之前成熟。",
"يضخّم الحجم نقاط الضعف غير المحلولة. يجب أن تنضج الضوابط والثقافة والمساءلة قبل أن تجعل التعقيدات التصحيح مكلفاً.",
"קנה מידה מגביר חולשות לא פתורות. controls, culture ו-accountability צריכים להתבגר לפני שcomplexity הופכת correction ליקר.",
)
Q(
"Executive confidence should not erase uncertainty. Strong decisions make assumptions visible and preserve options when facts change.",
"La confianza ejecutiva no debe borrar la incertidumbre. Las decisiones sólidas hacen visibles los supuestos y preservan opciones cuando cambian los hechos.",
"Executive Confidence soll Unsicherheit nicht tilgen. Starke Entscheidungen machen Annahmen sichtbar und bewahren Optionen, wenn Fakten sich ändern.",
"La confiance exécutive ne doit pas effacer l'incertitude. Les bonnes décisions rendent les hypothèses visibles et préservent les options quand les faits changent.",
"Executive confidence не должна стирать uncertainty. Сильные решения делают assumptions visible и сохраняют options при изменении facts.",
"Executive confidence не повинна стирати uncertainty. Сильні рішення роблять assumptions visible і зберігають options при зміні facts.",
"高管信心不应消除不确定性。强有力的决策使假设可见，并在事实变化时保留选项。",
"لا ينبغي أن تمحو confidence التنفيذية uncertainty. القرارات القوية تجعل الافتراضات visible وتحفظ options عند تغيّر الحقائق.",
"confidence מנהלית לא צריכה למחוק uncertainty. החלטות חזקות הופכות assumptions ל-visible ושומרות options כשfacts משתנים.",
)

# Speaking catalog
Q(
"Executive Conversations for Consequential Change",
"Conversaciones ejecutivas para el cambio trascendental",
"Executive Conversations für konsequente Veränderung",
"Conversations exécutives pour un changement majeur",
"Исполнительные диалоги о значимых переменах",
"Виконавчі діалоги про значущі зміни",
"面向重大变革的高管对话",
"محادثات تنفيذية من أجل تغيير جوهري",
"שיחות מנהליות לשינוי משמעותי",
)
Q(
"Keynotes, board sessions, and leadership briefings tailored to the audience, sector, and decision context.",
"Keynotes, sesiones de consejo y briefings de liderazgo adaptados a la audiencia, sector y contexto de decisión.",
"Keynotes, Board-Sessions und Leadership-Briefings, zugeschnitten auf Publikum, Sektor und Entscheidungskontext.",
"Keynotes, sessions de conseil et briefings de leadership adaptés au public, secteur et contexte de décision.",
"Keynote, заседания советов директоров и leadership-бriefings с учётом аудитории, сектора и контекста решений.",
"Keynote, засідання рад директорів і leadership-briefings з урахуванням аудиторії, сектору та контексту рішень.",
"根据受众、行业和决策背景定制的主旨演讲、董事会会议和领导简报。",
"محاضرات رئيسية وجلسات مجلس إدارة و briefings قيادية م adapted للجمهور والقطاع وسياق القرار.",
"Keynotes, ישיבות דירקטוריון ו-briefings מנהיגותיים המותאמים לקהל, לsector ולהקשר ההחלטה.",
)
Q(
"Governing AI Before It Governs the Enterprise",
"Gobernar la IA antes de que gobierne la empresa",
"KI governen, bevor sie das Unternehmen regiert",
"Gouverner l'IA avant qu'elle ne gouverne l'entreprise",
"Управлять ИИ, прежде чем он начнёт управлять компанией",
"Керувати ШІ, перш ніж він почне керувати компанією",
"在AI治理企业之前治理AI",
"حوكمة الذكاء الاصطناعي قبل أن يحكم المؤسسة",
"לממשל AI לפני שהוא ימשול בארגון",
)
Q(
"From Technology Trend to Enterprise Strategy",
"De tendencia tecnológica a estrategia empresarial",
"Vom Technologietrend zur Unternehmensstrategie",
"De la tendance technologique à la stratégie d'entreprise",
"От технологического тренда к корпоративной стратегии",
"Від технологічного тренду до корпоративної стратегії",
"从技术趋势到企业战略",
"من trend التكنولوجيا إلى استراتيجية المؤسسة",
"מטרnd טכנולוגי לאסטרטegיה ארגונית",
)
Q(
"Building Companies Through Market Cycles",
"Construir empresas a través de ciclos de mercado",
"Unternehmen durch Marktzyklen aufbauen",
"Construire des entreprises à travers les cycles de marché",
"Строить компании через рыночные циклы",
"Будувати компанії через ринкові цикли",
"穿越市场周期构建企业",
"بناء الشركات عبر دورات السوق",
"בניית חברות דרך מחזורי שוק",
)
Q(
"Precision Medicine: Promise, Proof, and Responsibility",
"Medicina de precisión: promesa, prueba y responsabilidad",
"Precision Medicine: Versprechen, Beweis und Verantwortung",
"Médecine de précision : promesse, preuve et responsabilité",
"Precision medicine: обещание, доказательства и ответственность",
"Precision medicine: обіцянка, докази та відповідальність",
"精准医疗：承诺、证据与责任",
"الطب الدقيق: الوعد والدليل والمسؤولية",
"רפואת דיוק: הבטחה, הוכחה ואחריות",
)
Q(
"The Board's Role in Cyber and Technology Risk",
"El papel del consejo en riesgo cibernético y tecnológico",
"Die Rolle des Boards bei Cyber- und Technologierisiko",
"Le rôle du conseil dans le risque cyber et technologique",
"Роль совета директоров в cyber- и technology risk",
"Роль ради директорів у cyber- та technology risk",
"董事会在网络与技术风险中的角色",
"دور مجلس الإدارة في مخاطر السيبر والتكنولوجيا",
"תפקיד הדירקטוריון בסיכון סיiber וטכנולוגי",
)
Q(
"Engineering Trust into Digital Infrastructure",
"Ingeniería de confianza en infraestructura digital",
"Vertrauen in digitale Infrastruktur ingenieuren",
"Ingénierie de la confiance dans l'infrastructure numérique",
"Инженерия доверия в цифровой инфраструктуре",
"Інженерія довіри в цифровій інфраструктурі",
"将信任工程化融入数字基础设施",
"هندسة الثقة في البنية التحتية الرقمية",
"הנדסת אמון לתשתית דיגיטלית",
)
Q(
"Leading Across Borders and Disciplines",
"Liderar a través de fronteras y disciplinas",
"Führung über Grenzen und Disziplinen hinweg",
"Diriger au-delà des frontières et des disciplines",
"Лидерство через границы и дисциплины",
"Лідерство через кордони та дисципліни",
"跨越边界与学科的领导",
"القيادة عبر الحدود والتخصصات",
"מנהיגות מעבר לגבולות ולתחומים",
)
Q(
"From Founder to Institution Builder",
"De fundador a constructor de instituciones",
"Vom Gründer zum Institution Builder",
"Du fondateur au bâtisseur d'institution",
"От основателя к создателю institution",
"Від засновника до творця institution",
"从创始人到机构建设者",
"من مؤسس إلى باني مؤسسة",
"ממייסד לבונה מוסד",
)
Q("Boards, audit and risk committees", "Consejos, comités de auditoría y riesgo", "Boards, Audit- und Risikoausschüsse", "Conseils, comités d'audit et de risque", "Советы директоров, комитеты по аудиту и рискам", "Ради директорів, комітети з аудиту та ризиків", "董事会、审计与风险委员会", "مجالس الإدارة ولجان التدقيق والمخاطر", "דירקטוריונים, ועדות ביקורת וסיכונים")
Q("Board briefing or keynote", "Briefing de consejo o keynote", "Board-Briefing oder Keynote", "Briefing conseil ou keynote", "Briefing для совета или keynote", "Briefing для ради або keynote", "董事会简报或主题演讲", "briefing لمجلس الإدارة أو keynote", "briefing דירקטוריון או keynote")
Q("CEOs, executive teams, investors", "CEOs, equipos ejecutivos, inversores", "CEOs, Führungsteams, Investoren", "PDG, équipes exécutives, investisseurs", "CEO, executive-команды, инвесторы", "CEO, executive-команди, інвестори", "CEO、高管团队、投资者", "CEOs وفرق تنفيذية ومستثمرون", "CEOs, צוותים executive ומשקיעים")
Q("Keynote or executive workshop", "Keynote o taller ejecutivo", "Keynote oder Executive Workshop", "Keynote ou atelier exécutif", "Keynote или executive workshop", "Keynote або executive workshop", "主题演讲或高管工作坊", "keynote أو workshop تنفيذي", "keynote או workshop executive")
Q("Founders, growth leaders, private equity", "Fundadores, líderes de crecimiento, private equity", "Gründer, Wachstumsführer, Private Equity", "Fondateurs, leaders de croissance, private equity", "Основатели, лидеры роста, private equity", "Засновники, лідери зростання, private equity", "创始人、成长型领导者、私募股权", "مؤسسون وقادة نمو وprivate equity", "מייסדים, מנהיגי צמיחה ו-private equity")
Q("Fireside chat or keynote", "Charla íntima o keynote", "Fireside Chat oder Keynote", "Discussion ou keynote", "Fireside chat или keynote", "Fireside chat або keynote", "炉边对话或主题演讲", "fireside chat أو keynote", "fireside chat או keynote")
Q("Healthcare leaders, clinicians, innovators", "Líderes sanitarios, clínicos, innovadores", "Healthcare-Führungskräfte, Kliniker, Innovatoren", "Leaders santé, cliniciens, innovateurs", "Лидеры здравоохранения, клиницисты, innovatorы", "Лідери охорони здоров'я, клініцисти, innovatorи", "医疗领导者、临床医生、创新者", "قادة الرعاية الصحية وclinicians وinnovators", "מנהיגי בריאות, קlinicians ו-innovators")
Q("Industry keynote or panel", "Keynote sectorial o panel", "Branchen-Keynote oder Panel", "Keynote sectorielle ou panel", "Отраслевой keynote или panel", "Галузевий keynote або panel", "行业主题演讲或 panel", "keynote صناعي أو panel", "keynote ענפי או panel")
Q("Directors, general counsel, risk leaders", "Directores, consejo general, líderes de riesgo", "Directors, General Counsel, Risikoführung", "Administrateurs, directeurs juridiques, leaders risque", "Директора, general counsel, лидеры по рискам", "Директори, general counsel, лідери з ризиків", "董事、总法律顾问、风险领导者", "directors وgeneral counsel وقادة مخاطر", "directors, general counsel ומנהיגי סיכון")
Q("Board education session", "Sesión de formación de consejo", "Board-Education-Session", "Session de formation du conseil", "Образовательная сессия для совета директоров", "Освітня сесія для ради директорів", "董事会教育会议", "جلسة تثقيف لمجلس الإدارة", "מפגש חינוך לדירקטוריון")
Q("Technology and infrastructure organizations", "Organizaciones de tecnología e infraestructura", "Technologie- und Infrastrukturorganisationen", "Organisations technologiques et d'infrastructure", "Технологические и инфраструктурные организации", "Технологічні та інфраструктурні організації", "技术与基础设施机构", "منظمات التكنولوجيا والبنية التحتية", "ארגוני טכנולוגיה ותשתיות")
Q("Technical-executive keynote", "Keynote técnico-ejecutivo", "Technisch-executive Keynote", "Keynote technique-exécutive", "Технически-executive keynote", "Технічно-executive keynote", "技术-高管主题演讲", "keynote تقني-تنفيذي", "keynote טכני-executive")
Q("Global leadership teams and universities", "Equipos de liderazgo global y universidades", "Globale Führungsteams und Universitäten", "Équipes de direction globales et universités", "Глобальные leadership-команды и университеты", "Глобальні leadership-команди та університети", "全球领导团队和大学", "فرق قيادة عالمية وجامعات", "צוותי מנהיגות גלובליים ואוניברסיטאות")
Q("Keynote or moderated conversation", "Keynote o conversación moderada", "Keynote oder moderiertes Gespräch", "Keynote ou conversation modérée", "Keynote или moderated conversation", "Keynote або moderated conversation", "主题演讲或 moderated 对话", "keynote أو محادثة moderated", "keynote או שיחה moderated")
Q("Entrepreneurs and next-generation executives", "Emprendedores y ejecutivos de próxima generación", "Unternehmer und Führungskräfte der nächsten Generation", "Entrepreneurs et dirigeants de nouvelle génération", "Предприниматели и executive следующего поколения", "Підприємці та executive наступного покоління", "创业者和新一代高管", "رواد أعمال وتنفيذيون من الجيل التالي", "יזמים ומנהלים מהדור הבא")
Q("Workshop or fireside chat", "Taller o charla íntima", "Workshop oder Fireside Chat", "Atelier ou discussion", "Workshop или fireside chat", "Workshop або fireside chat", "工作坊或炉边对话", "workshop أو fireside chat", "workshop או fireside chat")

# fmt: on
