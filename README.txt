================================================================================
  AI TRAINING RESEARCH — README
  עודכן לאחרונה: 2026-06-21 (v7 — 50 קורסים, 10 לכל כלי)
================================================================================

--------------------------------------------------------------------------------
🌐 האתר הפעיל (Vercel)
--------------------------------------------------------------------------------

  https://ai-training-research.vercel.app

  - מתעדכן אוטומטית כל יום בשעה 09:00 (GitHub Actions → Vercel redeploy)
  - אין צורך לעשות כלום — הכל קורה לבד

================================================================================

--------------------------------------------------------------------------------
0. אתרי ההדרכה הראשיים — לאן להיכנס (כתובות מלאות)
--------------------------------------------------------------------------------

  ⭐ כניסה ישירה לכל פלטפורמת הדרכה — פשוט הכנס לדפדפן והתחל ללמוד:

  ┌─────────────────────────────────────────────────────────────────────────┐
  │  כלי                 שם האתר                 כתובת מלאה               │
  │  ─────────────────────────────────────────────────────────────────────  │
  │  Gemini Enterprise   Google Cloud Skills Boost  https://cloudskillsboost.google         │
  │  ChatGPT Enterprise  OpenAI Academy             https://academy.openai.com              │
  │  Claude Enterprise   Anthropic Learning Center  https://anthropic.skilljar.com          │
  │  Azure AI Foundry    Microsoft Learn            https://learn.microsoft.com             │
  │  Amazon Bedrock      AWS Skill Builder          https://skillbuilder.aws                │
  └─────────────────────────────────────────────────────────────────────────┘

  הערה: כל האתרים חינמיים לחלוטין. תעודות מסוימות דורשות הרשמה (ללא תשלום).

--------------------------------------------------------------------------------
1. על הפרויקט
--------------------------------------------------------------------------------
פרויקט Python המייצר דוח Word מקצועי בעברית RTL עם המלצות הדרכה
לחמשת כלי ה-AI הארגוניים המובילים. כל המשאבים חינמיים לחלוטין.

כלי ה-AI הנחקרים:
  1. Gemini Enterprise (Google)
  2. ChatGPT Enterprise (OpenAI)
  3. Claude Enterprise (Anthropic)
  4. Microsoft Azure AI Foundry
  5. Amazon Bedrock (AWS)

עיצוב הדוח (v4):
  - כותרת ראשית עם קו כחול
  - כותרת כלי: פס כחול כהה, טקסט לבן
  - טבלה מקצועית לכל כלי: שם קורס | מה תלמד + דירוג | רמה | משך
  - URL לחיץ מתחת לשם הקורס (Ctrl+Click פותח דפדפן)
  - שורת דירוג אפורה: מספר לומדים, ציון, מנויים ב-YouTube
  - קופסת המלצה: רקע תכלת + גבול כחול מימין
  - מפריד אפור בין סעיפים

--------------------------------------------------------------------------------
2. מבנה קבצים — Paths מלאים
--------------------------------------------------------------------------------
/Users/zeevgrinberg/Desktop/ai-training-research/
│
├── main.py              ← נקודת כניסה: --local (מהיר) או --crew (AI מחקר)
├── generate_report.py   ← תוכן + בניית Word מקצועי (v5 — עיקרי)
├── youtube_researcher.py← מחפש YouTube לפי view count עם yt-dlp (ללא API key)
├── crew.py              ← CrewAI: Research Agent + Writer Agent (חיפוש אינטרנט)
├── word_writer.py       ← מנוע RTL Word: טבלאות, hyperlinks, callouts, bullets
├── requirements.txt     ← תלויות Python (כולל yt-dlp)
├── .env                 ← מפתחות API (לא לשלוח ל-Git)
├── README.txt           ← קובץ זה
│
├── venv/                ← Python 3.11.15 (Homebrew)
│   └── bin/python3
│
└── output/
    └── המלצות_הדרכות_AI.docx  ← קובץ ה-Word הסופי

--------------------------------------------------------------------------------
3. הרצה
--------------------------------------------------------------------------------

  # מצב מהיר — דוח מוכן (שניות):
  cd /Users/zeevgrinberg/Desktop/ai-training-research
  venv/bin/python3 main.py --local

  # מצב AI — מחקר חי מהאינטרנט (5-10 דקות):
  venv/bin/python3 main.py

  # ישירות (ללא main.py):
  venv/bin/python3 generate_report.py

  # מחקר YouTube — מציאת הסרטונים הנצפים ביותר לכל כלי (2 דקות):
  venv/bin/python3 youtube_researcher.py
  # → שומר תוצאות ב-output/youtube_research.json

--------------------------------------------------------------------------------
4. ה-Agents (CrewAI — מצב --crew בלבד)
--------------------------------------------------------------------------------

[ Agent 1 — Research Agent ]
  Role    : AI Enterprise Training Research Specialist
  כלים    : SerperDevTool (Serper API)
  LLM     : GPT-4o
  תפקיד  : מחפש קורסים, הסמכות ומשאבים לכל 5 הכלים, 2+ חיפושים לכלי

[ Agent 2 — Writer Agent ]
  Role    : Senior Technical Writer in Hebrew
  כלים    : ללא
  LLM     : GPT-4o
  תפקיד  : כותב דוח Markdown מלא בעברית מממצאי המחקר

  ⚠️  הערה חשובה: ה-CrewAI Agent אינו מאמת קישורים בפועל ועשוי ליצור
      URLs שגויים. generate_report.py הוא המקור הראשי לתוכן, עם קישורים
      שנבדקו ידנית ב-2026-06-18.

--------------------------------------------------------------------------------
5. ה-Tasks
--------------------------------------------------------------------------------

[ Task 1 — research_task ]
  Agent   : Research Agent
  פלט     : רשימת קורסים עם URL, עלות, משך, רמה לכל 5 כלים

[ Task 2 — write_task ]
  Agent   : Writer Agent
  Context : פלט research_task
  פלט     : Markdown מלא בעברית → create_word_document() בmain.py

--------------------------------------------------------------------------------
6. word_writer.py — ארכיטקטורת RTL (v4)
--------------------------------------------------------------------------------

  RTL מופעל ב-4 שכבות:
  ┌─────────────────────────────────────────────────────────────────────────┐
  │  שכבה 1 — settings.xml    : <w:bidi/>  (כיוון RTL לכל הדוקומנט)        │
  │  שכבה 2 — docDefaults     : pPrDefault — bidi + jc=right + lang he-IL  │
  │  שכבה 3 — Normal style    : <w:bidi/> + jc=right                        │
  │  שכבה 4 — כל פסקה/run     : <w:rtl/> + lang he-IL + csFont + csSize    │
  └─────────────────────────────────────────────────────────────────────────┘

  פונקציות ציבוריות:
    new_document()                    ← Document() עם כל הגדרות RTL
    add_title_block(doc, title, sub)  ← כותרת עם קו תחתון כחול
    add_tool_heading(doc, num, name)  ← פס כחול כהה עם מספר + שם
    add_body(doc, text)               ← פסקת גוף RTL, Arial 12
    add_bullet(doc, text)             ← • עם hanging indent מימין
    add_courses_table(doc, courses)   ← טבלה RTL 4 עמודות + היפרלינקים
    add_callout(doc, title, text)     ← קופסת המלצה (תכלת + גבול כחול)
    add_divider(doc)                  ← קו אפור מפריד
    create_word_document(content)     ← Markdown → Word (מצב crew)

  היפרלינקים (v4 — חדש):
    - _add_hyperlink(paragraph, url, text, pt, color)
    - מוסיפה <w:hyperlink r:id="rIdX"> עם relationship חיצוני
    - URL ללא https:// מקבל אוטומטית https://
    - מיובאת: from docx.opc.constants import RELATIONSHIP_TYPE as RT
    - הקישור נרשם ב-word/_rels/document.xml.rels
    - Ctrl+Click בWord פותח את הדפדפן

  דירוג (v4 — חדש):
    - שדה "rating" בכל dict של קורס (אופציונלי)
    - מוצג כשורה אפורה קטנה (9pt) מתחת לתיאור בטבלה
    - דוגמה: "4.3/5 | 8,339 לומדים | עודכן ינואר 2026"

  טבלה RTL:
    - <w:bidiVisual/> על ה-table — col[0] = עמודה ימנית ביותר
    - col[0]: שם הקורס (bold) + URL לחיץ קטן מתחת (9pt כחול)
    - col[1]: מה תלמד (7.5cm) + שורת דירוג אפורה
    - col[2]: רמה (2cm)
    - col[3]: משך (2cm)
    - Header: רקע #1F497D, טקסט לבן
    - שורות: לסירוגין לבן / #EDF2FF

  Callout box:
    - רקע: #E8F4FD (תכלת בהיר)
    - גבול ימין: 3pt solid #2E75B6
    - כותרת bold כחולה + גוף רגיל

  גופנים:
    - w:ascii + w:hAnsi + w:cs = Arial  (latin + Complex Script לעברית)
    - w:sz + w:szCs = גודל פונט (half-points)
    - H1: 16pt | H2: 14pt | גוף: 12pt | טבלה: 11pt | URL/rating: 9pt

--------------------------------------------------------------------------------
7. generate_report.py — התוכן (v4)
--------------------------------------------------------------------------------

  כל קורס מוגדר כ-dict:
    {
      "name"   : str,        ← שם הקורס
      "url"    : str,        ← ללא https:// (מתווסף אוטומטית)
      "desc"   : str,        ← תיאור תוכן הקורס
      "level"  : str,        ← רמה: מתחיל / בינוני / מתקדם
      "dur"    : str,        ← משך: שעות / שבועות
      "rating" : str,        ← דירוג + לומדים + הערות (אופציונלי)
    }

  כל כלי מוגדר כ-dict:
    { "number": str, "name": str, "desc": str,
      "courses": [list of course dicts],
      "rec": (title, text) }

  קישורים מאומתים (2026-06-21) — 25 URLs (עם שמות אתרים):
  ┌──────────────────────────────────────────────────────────────────────────────────────────┐
  │ GEMINI ENTERPRISE                                                                         │
  │   שם האתר               : Google Workspace Training                                      │
  │   כתובת                 : https://workspace.google.com/training                          │
  │                                                                                           │
  │   שם האתר               : Google Cloud Skills Boost                                      │
  │   כתובת                 : https://cloudskillsboost.google                                │
  │                                                                                           │
  │   שם האתר               : Google Cloud Skills Boost — Prompt Design Path                 │
  │   כתובת                 : https://cloudskillsboost.google/paths/183                      │
  │                                                                                           │
  │   שם האתר               : Google AI Education Hub                                        │
  │   כתובת                 : https://ai.google/education                                     │
  │                                                                                           │
  │   שם האתר               : YouTube — Google Cloud (1.2M+ מנויים)                         │
  │   כתובת                 : https://youtube.com/@googlecloud                               │
  │                                                                                           │
  │ CHATGPT ENTERPRISE                                                                        │
  │   שם האתר               : OpenAI Academy                                                 │
  │   כתובת                 : https://academy.openai.com                                     │
  │                                                                                           │
  │   שם האתר               : OpenAI — הסמכה רשמית AI Foundations                           │
  │   כתובת                 : https://openai.com/index/introducing-openai-certification      │
  │                                                                                           │
  │   שם האתר               : DeepLearning.AI — ChatGPT Prompt Engineering                  │
  │   כתובת                 : https://deeplearning.ai/short-courses/chatgpt-prompt-engineering-for-developers│
  │                                                                                           │
  │   שם האתר               : DeepLearning.AI — Building Systems with ChatGPT API           │
  │   כתובת                 : https://deeplearning.ai/short-courses/building-systems-with-chatgpt│
  │                                                                                           │
  │   שם האתר               : YouTube — OpenAI (700K+ מנויים)                               │
  │   כתובת                 : https://youtube.com/@OpenAI                                    │
  │                                                                                           │
  │ CLAUDE ENTERPRISE                                                                         │
  │   שם האתר               : Anthropic Learning Center — Claude Platform 101               │
  │   כתובת                 : https://anthropic.skilljar.com/claude-platform-101            │
  │                                                                                           │
  │   שם האתר               : Anthropic Learning Center — Claude Code 101                   │
  │   כתובת                 : https://anthropic.skilljar.com/claude-code-101                │
  │                                                                                           │
  │   שם האתר               : Anthropic Learning Center — Claude in Amazon Bedrock          │
  │   כתובת                 : https://anthropic.skilljar.com/claude-in-amazon-bedrock       │
  │                                                                                           │
  │   שם האתר               : Anthropic Learning Center — AI Fluency for Business           │
  │   כתובת                 : https://anthropic.skilljar.com/ai-fluency-for-small-businesses│
  │                                                                                           │
  │   שם האתר               : Anthropic Learning Center — Introduction to Agent Skills      │
  │   כתובת                 : https://anthropic.skilljar.com/introduction-to-agent-skills   │
  │                                                                                           │
  │ AZURE AI FOUNDRY                                                                          │
  │   שם האתר               : Microsoft Learn — Develop Generative AI Apps in Foundry       │
  │   כתובת                 : https://learn.microsoft.com/en-us/training/paths/develop-generative-ai-apps│
  │                                                                                           │
  │   שם האתר               : Coursera — Microsoft AI Agent Fundamentals (3.8/5, 11K)       │
  │   כתובת                 : https://coursera.org/learn/microsoft-ai-agent-fundamentals    │
  │                                                                                           │
  │   שם האתר               : Coursera — Microsoft Generative AI Engineering (4.3/5)        │
  │   כתובת                 : https://coursera.org/professional-certificates/microsoft-generative-ai-engineering│
  │                                                                                           │
  │   שם האתר               : YouTube — Microsoft Azure (230K+ מנויים)                      │
  │   כתובת                 : https://youtube.com/@MicrosoftAzure                           │
  │                                                                                           │
  │   שם האתר               : Microsoft Learn — Azure AI Fundamentals AI-900                │
  │   כתובת                 : https://learn.microsoft.com/credentials/certifications/azure-ai-fundamentals│
  │                                                                                           │
  │ AMAZON BEDROCK                                                                            │
  │   שם האתר               : YouTube — freeCodeCamp (Enterprise AI with Bedrock, 6 שעות)  │
  │   כתובת                 : https://youtube.com/watch?v=HaUe2AN210g                       │
  │                                                                                           │
  │   שם האתר               : AWS Skill Builder (600+ קורסים חינמיים)                       │
  │   כתובת                 : https://skillbuilder.aws                                       │
  │                                                                                           │
  │   שם האתר               : Amazon Bedrock — Getting Started                              │
  │   כתובת                 : https://aws.amazon.com/bedrock/getting-started               │
  │                                                                                           │
  │   שם האתר               : YouTube — Amazon Web Services (1.1M+ מנויים)                  │
  │   כתובת                 : https://youtube.com/@amazonwebservices                         │
  │                                                                                           │
  │   שם האתר               : AWS Training — Machine Learning                               │
  │   כתובת                 : https://aws.amazon.com/training/learn-about/machine-learning  │
  └──────────────────────────────────────────────────────────────────────────────────────────┘

  להוספת כלי חדש:
    1. הוסף dict ל-TOOLS בgenerate_report.py (כולל שדה "rating")
    2. אמת את כל הקישורים עם curl לפני פרסום
    3. עדכן README.txt

--------------------------------------------------------------------------------
8. שינויים לפי גרסה
--------------------------------------------------------------------------------

  v1 — יצירה ראשונית: CrewAI + Word בסיסי
  v2 — RTL תיקונים ראשוניים + עברית
  v3 (2026-06-17):
    - תיקון RTL מלא (4 שכבות, כולל docDefaults)
    - הסרת em-dashes וסימני AI
    - אימות קישורים ראשוני
    - עיצוב מקצועי: טבלאות, callouts, כותרות צבעוניות
  v4 (2026-06-18):
    - _add_hyperlink(): כל 25 הURLים לחיצים אמיתיים (OOXML <w:hyperlink>)
    - שדה "rating" בכל קורס + תצוגה אפורה בטבלה
    - 6 קישורים תוקנו/הוחלפו:
        grow.google → ai.google/education
        skills.google.com/paths/249 → workspace.google.com/training
        @AzureDevs → @MicrosoftAzure (ערוץ רשמי)
        deeplearning.ai/courses/generative-ai-with-llms (paid) → aws.amazon.com/bedrock/getting-started
        deeplearning.ai/short-courses/agent-skills-with-anthropic (partly paid) → anthropic.skilljar.com/introduction-to-agent-skills
        explore.skillbuilder.aws/... (broken) → aws.amazon.com/training/learn-about/machine-learning
    - Anthropic Academy: עודכן מ-16 ל-20 קורסים
  v5 (2026-06-21):
    - הוספת סעיף 0: אתרי ההדרכה הראשיים — שמות אתרים + כתובות https:// מלאות לכל 5 הכלים
    - טבלת 25 URLs הורחבה: כל URL מציג כעת שם אתר קריא + כתובת מלאה עם https://
    - תיקון URL של Microsoft Learn (היה 404): learn.microsoft.com/training/azure/ai-foundry
      → learn.microsoft.com/en-us/training/paths/develop-generative-ai-apps (עודכן מאי 2026)
  v6 (2026-06-21):
    - פרסום ב-Vercel: https://ai-training-research.vercel.app
    - פילטר רמות: מתחיל / בינוני / מפתחים (client-side JS)
    - GitHub Actions: עדכון אוטומטי כל יום 09:00
  v7 (2026-06-21):
    - הרחבה ל-50 קורסים — 10 לכל כלי
    - Gemini: Google AI Essentials (1.8M), ML Crash Course, Gemini API Hub
    - ChatGPT: GenAI for Everyone (Andrew Ng, 806K), Prompt Eng (Vanderbilt, 687K),
               Business Thinkers, LangChain, OpenAI Cookbook
    - Claude: Agent Skills, Prompt Eng with Claude v3 (DeepLearning.AI), Anthropic GitHub
    - Azure: M365 Copilot Get Started, GitHub Copilot, Azure OpenAI dev path
    - Bedrock: Serverless LLM Apps (DeepLearning.AI), AWS AI Practitioner cert,
               Bedrock Workshop, Bedrock Samples GitHub

--------------------------------------------------------------------------------
9. סביבה ומפתחות API
--------------------------------------------------------------------------------

  קובץ .env: /Users/zeevgrinberg/Desktop/ai-training-research/.env

  OPENAI_API_KEY   — GPT-4o (מקור: worldcup-predictor)
  SERPER_API_KEY   — חיפוש אינטרנט serper.dev (מקור: worldcup-predictor)

  גרסאות:
    Python      : 3.11.15
    crewai      : 1.14.7
    openai      : 2.42.0
    python-docx : 1.2.0

================================================================================
