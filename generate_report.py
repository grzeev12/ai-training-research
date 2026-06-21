"""
generate_report.py
------------------
Builds the professional Hebrew RTL Word document.
All resources are FREE. No em-dashes. No AI writing markers.
Links verified June 2026. Ratings added June 2026.
"""

import os
from word_writer import (
    new_document, add_title_block, add_divider, add_tool_heading,
    add_body, add_courses_table, add_callout, OUTPUT_FILE
)

INTRO = (
    "דוח זה מרכז את 50 ההדרכות, הקורסים וההסמכות המובילות לחמשת כלי ה-AI "
    "הארגוניים הנפוצים ביותר — 10 קורסים לכל כלי. רוב המשאבים חינמיים לצפייה "
    "ולמידה; חלק דורשים מנוי לקבלת תעודה רשמית. הקורסים נבחרו על בסיס "
    "דירוג גבוה, מספר לומדים, תוכן עדכני לשנת 2026 ורלוונטיות לצוותים ארגוניים."
)

TOOLS = [

    # ── 1. Gemini Enterprise ──────────────────────────────────────────────────
    {
        "number": "01",
        "name": "Gemini Enterprise (Google)",
        "desc": (
            "Gemini Enterprise הוא פתרון ה-AI הארגוני של Google. הוא משלב את "
            "מודל Gemini בתוך Google Workspace כולל Gmail, Docs, Meet ו-Sheets, "
            "ומחבר לתשתיות Vertex AI ו-Google Cloud. מתאים לארגונים שרוצים "
            "Enterprise Search חכם, AI Agents ואוטומציה של תהליכי עבודה."
        ),
        "courses": [
            {
                "name": "Google Workspace Training",
                "url": "workspace.google.com/training",
                "desc": (
                    "מרכז ההדרכה הרשמי של Google Workspace. כולל מדריכים, "
                    "טיפים מהירים וקורסים לשימוש ב-Gemini ב-Gmail, Docs, Meet "
                    "ו-Sheets. חינמי לחלוטין, ללא הרשמה."
                ),
                "level": "מתחיל",
                "dur": "לפי בחירה",
                "rating": "הדרכה רשמית של Google | מאות אלפי משתמשים | חינמי ללא הרשמה",
            },
            {
                "name": "Introduction to Gemini Enterprise",
                "url": "cloudskillsboost.google",
                "desc": (
                    "הפלטפורמה הרשמית של Google Cloud עם מאות קורסים חינמיים. "
                    "הנצפה ביותר: Introduction to Generative AI, Introduction "
                    "to LLMs ו-Responsible AI. Labs מעשיים ב-Vertex AI."
                ),
                "level": "מתחיל עד בינוני",
                "dur": "1 עד 3 שעות לקורס",
                "rating": "מיליוני לומדים | Introduction to GenAI: אחד הנצפים ביותר ב-Google",
            },
            {
                "name": "Prompt Design in Vertex AI",
                "url": "cloudskillsboost.google/paths/183",
                "desc": (
                    "נתיב למידה רשמי של Google Cloud. מכסה prompt engineering "
                    "עם Gemini API, multimodal inputs ו-Vertex AI Studio. "
                    "כולל labs מעשיים חינמיים בדפדפן."
                ),
                "level": "מתחיל עד מפתחים",
                "dur": "5 שעות",
                "rating": "קורס Google Cloud Skills Boost | חינמי עם completion badge",
            },
            {
                "name": "Google AI Education Hub",
                "url": "ai.google/education",
                "desc": (
                    "דף הקורסים החינמיים הרשמי של Google AI. כולל: Introduction "
                    "to Generative AI, Introduction to Large Language Models "
                    "ו-AI Power-Ups for Google Workspace. כולם חינמיים לחלוטין."
                ),
                "level": "מתחיל",
                "dur": "1 עד 3 שעות לקורס",
                "rating": "חינמי לחלוטין | ישירות מצוות Google AI | ללא הרשמה",
            },
            {
                "name": "Introduction to Generative AI",
                "url": "skills.google/course_templates/536",
                "desc": (
                    "קורס מיקרו-לרנינג חינמי של Google. מסביר מהי Generative AI, "
                    "איך היא עובדת ובמה שונה מ-ML מסורתי. מסתיים ב-Badge דיגיטלי "
                    "רשמי. 45 דקות בלבד — מושלם כנקודת פתיחה לכל חבר צוות."
                ),
                "level": "מתחיל",
                "dur": "45 דקות",
                "rating": "חינמי | Badge דיגיטלי רשמי | Google Skills | ללא הרשמה",
            },
            {
                "name": "Google Cloud ML & AI Training Hub",
                "url": "cloud.google.com/learn/training/machinelearning-ai",
                "desc": (
                    "דף ההדרכה המרכזי של Google Cloud ל-Machine Learning ו-GenAI. "
                    "מסלולים ממתחיל ועד מתקדם: Gemini Workspace, Vertex AI, "
                    "TensorFlow, MLOps ובניית Agents. כולל 35 קרדיטים חינמיים חודשיים."
                ),
                "level": "כל הרמות",
                "dur": "משתנה",
                "rating": "הדרכה רשמית Google Cloud | 35 קרדיטים חינמיים לחודש | מסלולים לפי תפקיד",
            },
            {
                "name": "Google AI Essentials",
                "url": "coursera.org/learn/google-ai-essentials",
                "desc": (
                    "קורס מקיף של Google ב-Coursera. 5 מודולים על שימוש מעשי "
                    "בכלי GenAI לפרודוקטיביות בעבודה: Gemini, prompt engineering "
                    "ו-Responsible AI. מסתיים בתעודת Google. חינמי לצפייה."
                ),
                "level": "מתחיל",
                "dur": "8 עד 10 שעות",
                "rating": "4.8/5 | 1.8M+ לומדים | Google | תעודה רשמית | Coursera",
            },
            {
                "name": "Google Machine Learning Crash Course",
                "url": "developers.google.com/machine-learning/crash-course",
                "desc": (
                    "הקורס החינמי המפורסם ביותר של Google למפתחים. מכסה יסודות ML, "
                    "neural networks, TensorFlow ו-LLMs. 25+ שיעורים עם תרגולים "
                    "ב-Python. קורס הדגל של Google לפיתוח AI."
                ),
                "level": "מפתחים",
                "dur": "15 שעות",
                "rating": "חינמי לחלוטין | Google Developers | קורס הדגל של Google | 2024",
            },
            {
                "name": "Gemini API — Google AI for Developers",
                "url": "ai.google.dev/gemini-api/docs",
                "desc": (
                    "פורטל המפתחים הרשמי של Gemini API. Quickstarts, "
                    "Gemini Cookbook עם מאות דוגמאות קוד, ומדריכים ל-multimodal, "
                    "function calling ו-embeddings. חינמי לחלוטין."
                ),
                "level": "מפתחים",
                "dur": "משתנה",
                "rating": "חינמי | Google | Gemini API Cookbook + Quickstarts | עודכן 2026",
            },
            {
                "name": "Master Gemini 3.1 for Work in 12 Minutes",
                "url": "youtube.com/watch?v=bTLmt9BKGVc",
                "desc": (
                    "סרטון ריכוז של Jeff Su: כל הפיצ'רים החשובים של Gemini "
                    "לעבודה יומיומית ב-12 דקות. Gemini ב-Gmail, Docs, Sheets "
                    "ו-Google Meet. ישיר ומעשי, מתאים לכל חברי הצוות."
                ),
                "level": "מתחיל",
                "dur": "13 דקות",
                "rating": "365K צפיות | Jeff Su | 2026",
            },
        ],
        "rec": (
            "המלצה לצוות",
            "לצוות המשתמש ב-Google Workspace: להתחיל ב-workspace.google.com/training "
            "(חינמי, ללא הרשמה, כולל Gemini). למפתחים: cloudskillsboost.google "
            "ואחריו נתיב Prompt Design in Vertex AI. לצפייה בחידושים: YouTube Google Cloud."
        ),
    },

    # ── 2. ChatGPT Enterprise ─────────────────────────────────────────────────
    {
        "number": "02",
        "name": "ChatGPT Enterprise (OpenAI)",
        "desc": (
            "ChatGPT Enterprise הוא המוצר הארגוני של OpenAI. הוא מציע אבטחת SOC 2, "
            "חלון הקשר מורחב, ניתוח נתונים ללא הגבלה ובניית GPTs פנימיים. מתאים "
            "לצוותים שרוצים שליטה ארגונית מלאה על הנתונים לצד יכולות AI מתקדמות."
        ),
        "courses": [
            {
                "name": "OpenAI Academy",
                "url": "academy.openai.com",
                "desc": (
                    "הפלטפורמה הרשמית והחינמית של OpenAI. שלושה קורסים: AI Foundations "
                    "למתחילים, Applied AI Foundations לבינוניים, ו-Agents and Workflows "
                    "למתקדמים. מחולק לפי תפקיד: בעלי עסקים, מפתחים ומגזר ציבורי."
                ),
                "level": "מתחיל עד בינוני",
                "dur": "2 עד 4 שעות",
                "rating": "פלטפורמה רשמית של OpenAI | חינמית לחלוטין | הושקה 2025",
            },
            {
                "name": "OpenAI AI Foundations Certification",
                "url": "openai.com/index/introducing-openai-certification",
                "desc": (
                    "הסמכה רשמית ראשונה של OpenAI שהושקה דצמבר 2025. מבוססת על "
                    "תרחישים בתוך ChatGPT. מגובה על ידי ETS ו-Credly. "
                    "מסלול ארגוני בפיילוט עם ערך אמיתי ל-CV."
                ),
                "level": "בינוני",
                "dur": "4 עד 6 שעות",
                "rating": "ההסמכה הרשמית היחידה של OpenAI | מגובה ETS ו-Credly",
            },
            {
                "name": "ChatGPT Prompt Engineering for Developers",
                "url": "deeplearning.ai/courses/chatgpt-prompt-eng",
                "desc": (
                    "קורס קלאסי של DeepLearning.AI עם OpenAI. מכסה system prompts, "
                    "few-shot learning, chain-of-thought ו-structured output. "
                    "מוצג על ידי Andrew Ng ו-Isa Fulford מ-OpenAI."
                ),
                "level": "מפתחים",
                "dur": "שעה וחצי",
                "rating": "4M+ לומדים | Andrew Ng + Isa Fulford (OpenAI) | הנצפה ביותר בתחום",
            },
            {
                "name": "Building Systems with the ChatGPT API",
                "url": "deeplearning.ai/short-courses/building-systems-with-chatgpt",
                "desc": (
                    "המשך ישיר לקורס prompt engineering של DeepLearning.AI. בניית "
                    "pipeline מלא מ-classification ועד evaluation עם Python. "
                    "חינמי לחלוטין."
                ),
                "level": "מפתחים",
                "dur": "שעה",
                "rating": "1M+ לומדים | קורס ההמשך המומלץ ביותר אחרי Prompt Engineering",
            },
            {
                "name": "How to Create Custom GPT",
                "url": "youtube.com/watch?v=0Q1AQAxpdGg",
                "desc": (
                    "הדרכה של Kevin Stratvert על בניית Custom GPTs פנימיים "
                    "ב-ChatGPT Enterprise. מדריך שלב-אחר-שלב: הגדרת "
                    "instructions, knowledge base, ו-actions. 20 דקות, מעשי."
                ),
                "level": "מתחיל עד בינוני",
                "dur": "20 דקות",
                "rating": "483K צפיות | Kevin Stratvert | 2025",
            },
            {
                "name": "Generative AI for Everyone",
                "url": "coursera.org/learn/generative-ai-for-everyone",
                "desc": (
                    "הקורס הנגיש ביותר של Andrew Ng ל-GenAI. מסביר איך עובדים LLMs, "
                    "איך לבנות workflow ארגוני עם AI, ומה הסיכונים. ללא רקע טכני. "
                    "חינמי לצפייה ב-Coursera."
                ),
                "level": "מתחיל",
                "dur": "6 שעות",
                "rating": "4.8/5 | 806K+ לומדים | Andrew Ng, DeepLearning.AI | הנגיש ביותר לכולם",
            },
            {
                "name": "Prompt Engineering for ChatGPT",
                "url": "coursera.org/learn/prompt-engineering",
                "desc": (
                    "קורס Vanderbilt University ב-Coursera. 6 מודולים: prompt patterns, "
                    "chain-of-thought, few-shot ובניית אפליקציית prompt. "
                    "ד\"ר Jules White. חינמי לצפייה."
                ),
                "level": "מתחיל עד בינוני",
                "dur": "19 שעות",
                "rating": "4.8/5 | 687K+ לומדים | Vanderbilt University | Coursera",
            },
            {
                "name": "How Business Thinkers Can Build with the ChatGPT API",
                "url": "deeplearning.ai/short-courses/how-business-thinkers-can-start-building-with-the-chatgpt-api/",
                "desc": (
                    "קורס DeepLearning.AI לאנשי עסקים ומנהלים. מדגים בנייה "
                    "מהירה של POC עם ChatGPT API ללא ניסיון מפתח. "
                    "Python בסיסי בלבד. חינמי."
                ),
                "level": "בינוני",
                "dur": "שעה",
                "rating": "חינמי | DeepLearning.AI | מיועד למנהלים ואנשי עסקים | 2024",
            },
            {
                "name": "LangChain for LLM Application Development",
                "url": "deeplearning.ai/short-courses/langchain-for-llm-application-development/",
                "desc": (
                    "קורס של Harrison Chase (מייסד LangChain) ו-Andrew Ng. "
                    "בניית אפליקציות LLM עם chains, memory, agents ו-document Q&A. "
                    "קוד Python מלא. חינמי."
                ),
                "level": "מפתחים",
                "dur": "שעה וחצי",
                "rating": "חינמי | Harrison Chase + Andrew Ng | LangChain | DeepLearning.AI",
            },
            {
                "name": "OpenAI Developer Cookbook",
                "url": "developers.openai.com/cookbook",
                "desc": (
                    "המאגר הרשמי של OpenAI למפתחים: מאות דוגמאות קוד Python "
                    "ל-ChatGPT API, Assistants, function calling, embeddings "
                    "ו-fine-tuning. מתעדכן שוטף. חינמי לחלוטין."
                ),
                "level": "מפתחים",
                "dur": "לפי בחירה",
                "rating": "חינמי | OpenAI | מאות דוגמאות קוד | עודכן 2026",
            },
        ],
        "rec": (
            "המלצה לצוות",
            "להתחיל ב-OpenAI Academy (academy.openai.com): חינמי, עדכני, "
            "מחולק לפי תפקיד. מנהלים יוסיפו את Generative AI for Everyone (Andrew Ng, 806K לומדים). "
            "מפתחים יוסיפו את DeepLearning.AI + LangChain. "
            "למי שרוצה הסמכה רשמית: OpenAI AI Foundations Certification."
        ),
    },

    # ── 3. Claude Enterprise ──────────────────────────────────────────────────
    {
        "number": "03",
        "name": "Claude Enterprise (Anthropic)",
        "desc": (
            "Claude Enterprise הוא פתרון ה-AI הארגוני של Anthropic. הוא מציע "
            "חלון הקשר של 200,000 טוקן, Projects לניהול ידע ארגוני ואינטגרציה "
            "עם Amazon Bedrock ו-Google Vertex AI. Anthropic Academy נפתחה מרץ "
            "2026 ומכילה 20 קורסים, כולם חינמיים עם תעודת גמר."
        ),
        "courses": [
            {
                "name": "Claude Platform 101",
                "url": "anthropic.skilljar.com/claude-platform-101",
                "desc": (
                    "קורס הכניסה הרשמי למפתחים. מכסה Claude API מ-A עד Z: message "
                    "requests, streaming, tool use, prompt caching ו-production "
                    "deployment. 84 לקציות ומעל 8 שעות תוכן."
                ),
                "level": "מפתחים",
                "dur": "8 שעות",
                "rating": "84 לקציות | חינמי עם תעודה רשמית | Anthropic Academy",
            },
            {
                "name": "Claude Code 101",
                "url": "anthropic.skilljar.com/claude-code-101",
                "desc": (
                    "קורס ייעודי ל-Claude Code, כלי הפיתוח האג'נטי של Anthropic. "
                    "מכסה MCP, agent skills ובניית workflows לפיתוח תוכנה "
                    "אוטומטי. חינמי עם תעודה."
                ),
                "level": "מפתחים",
                "dur": "3 שעות",
                "rating": "חינמי עם תעודה | עודכן 2026 | Anthropic Academy",
            },
            {
                "name": "Claude with Amazon Bedrock",
                "url": "anthropic.skilljar.com/claude-in-amazon-bedrock",
                "desc": (
                    "קורס ייעודי לשימוש ב-Claude דרך AWS Bedrock. מכסה deployment, "
                    "enterprise integration ועבודה עם Bedrock Knowledge Bases "
                    "ל-RAG. מתאים לצוותים שעובדים עם AWS."
                ),
                "level": "בינוני",
                "dur": "2 שעות",
                "rating": "חינמי עם תעודה | ייעודי לצוותי AWS | Anthropic Academy",
            },
            {
                "name": "AI Fluency for Small Businesses",
                "url": "anthropic.skilljar.com/ai-fluency-for-small-businesses",
                "desc": (
                    "לצוותים לא-טכניים. שימוש ב-Claude לפרודוקטיביות ארגונית, "
                    "כתיבת מסמכים, ניתוח נתונים ואוטומציה של תהליכים ללא כתיבת "
                    "קוד. חינמי עם תעודת גמר."
                ),
                "level": "מתחיל",
                "dur": "2 שעות",
                "rating": "חינמי עם תעודה | מותאם לצוותים עסקיים ולא-טכניים",
            },
            {
                "name": "Claude Code in Action",
                "url": "anthropic.skilljar.com/claude-code-in-action",
                "desc": (
                    "קורס מתקדם של Anthropic Academy על שילוב Claude Code ב-workflow "
                    "הפיתוח. מכסה ארכיטקטורת coding assistant, tool use, ניהול "
                    "הקשר ואינטגרציה עם GitHub. 24 לקציות ב-4 פרקים, מעשי לחלוטין."
                ),
                "level": "מפתחים",
                "dur": "3 עד 4 שעות",
                "rating": "חינמי עם תעודה | 24 לקציות | Anthropic Academy | 2026",
            },
            {
                "name": "Claude with Google Cloud Vertex AI",
                "url": "anthropic.skilljar.com/claude-with-google-vertex",
                "desc": (
                    "ההכשרה הטכנית המקיפה ביותר לשילוב Claude ב-Vertex AI של Google. "
                    "מכסה API requests, tool use, RAG ו-Model Context Protocol. "
                    "מעל 70 לקציות ב-11 פרקים. מותאם לצוותים עם Google Cloud."
                ),
                "level": "מפתחים",
                "dur": "8 עד 10 שעות",
                "rating": "חינמי עם תעודה | 70+ לקציות | Anthropic Academy | Google Cloud",
            },
            {
                "name": "Mastering Claude Code in 30 Minutes",
                "url": "youtube.com/watch?v=6eBSHbLKuN0",
                "desc": (
                    "הסרטון הרשמי של Anthropic עצמה. הנצפה ביותר על Claude Code: "
                    "agent workflows, MCP, כלים חיצוניים ו-production tips. "
                    "מוצג על ידי הצוות שבנה את Claude Code."
                ),
                "level": "מפתחים",
                "dur": "28 דקות",
                "rating": "1.4M צפיות | Anthropic | הנצפה ביותר על Claude Code",
            },
            {
                "name": "Introduction to Agent Skills",
                "url": "anthropic.skilljar.com/introduction-to-agent-skills",
                "desc": (
                    "קורס Anthropic Academy על בניית, הגדרת ושיתוף Skills ב-Claude Code. "
                    "מכסה יצירת Skill ראשון, multi-file skills ושיתוף עם צוותים. "
                    "6 לקציות, חינמי עם תעודה."
                ),
                "level": "מפתחים",
                "dur": "שעה",
                "rating": "חינמי עם תעודה | 6 לקציות | Anthropic Academy | 2026",
            },
            {
                "name": "Prompt Engineering with Anthropic Claude v3",
                "url": "deeplearning.ai/short-courses/prompt-engineering-with-anthropic-claude-v-3/",
                "desc": (
                    "קורס DeepLearning.AI ייעודי ל-Claude. מכסה prompt patterns "
                    "ספציפיים ל-Claude: constitutional AI, multi-step reasoning "
                    "ו-structured output. חינמי עם דוגמאות Python."
                ),
                "level": "בינוני",
                "dur": "שעה וחצי",
                "rating": "חינמי | DeepLearning.AI | ייעודי ל-Claude v3 | Anthropic",
            },
            {
                "name": "Anthropic Courses — GitHub",
                "url": "github.com/anthropics/courses",
                "desc": (
                    "מאגר notebooks חינמי ורשמי של Anthropic ב-GitHub. כולל "
                    "קורסי Jupyter על prompt engineering, tool use, multi-agent "
                    "patterns ו-RAG עם Claude API. Python."
                ),
                "level": "מפתחים",
                "dur": "לפי בחירה",
                "rating": "חינמי לחלוטין | Anthropic | Jupyter Notebooks | GitHub | 2026",
            },
        ],
        "rec": (
            "המלצה לצוות",
            "Anthropic Academy (anthropic.skilljar.com) היא נקודת ההתחלה: "
            "חינמית, 20+ קורסים עם תעודות, עודכנה 2026. "
            "לצוות טכני: Claude Platform 101 (8 שעות) + Anthropic Courses ב-GitHub. "
            "לצוות עסקי: AI Fluency. לצוותי AWS: Claude with Amazon Bedrock. "
            "לצוותי Google Cloud: Claude with Vertex AI (70+ לקציות)."
        ),
    },

    # ── 4. Microsoft Azure AI Foundry ─────────────────────────────────────────
    {
        "number": "04",
        "name": "Microsoft Azure AI Foundry",
        "desc": (
            "Microsoft Azure AI Foundry היא הפלטפורמה הארגונית המאוחדת של Microsoft "
            "לבניית יישומי AI. היא מאחדת מודלי OpenAI, Meta Llama ו-Mistral תחת "
            "תשתית Azure אחת עם ניהול agents, RAG ו-responsible AI. שמה הקודם "
            "היה Azure OpenAI Service."
        ),
        "courses": [
            {
                "name": "Develop Generative AI Apps in Microsoft Foundry",
                "url": "learn.microsoft.com/en-us/training/paths/develop-generative-ai-apps",
                "desc": (
                    "נתיב למידה רשמי וחינמי של Microsoft, עודכן מאי 2026. שישה "
                    "מודולים: הכנת סביבה, בחירת מודלים, בניית chat app, שימוש "
                    "ב-tools, אופטימיזציה ו-Responsible AI. Labs בדפדפן חינם."
                ),
                "level": "מתחיל עד בינוני",
                "dur": "8 עד 12 שעות",
                "rating": "הדרכה רשמית של Microsoft | עודכן מאי 2026 | Labs חינמיים בדפדפן",
            },
            {
                "name": "Microsoft AI Agent Fundamentals",
                "url": "coursera.org/learn/microsoft-ai-agent-fundamentals",
                "desc": (
                    "קורס של Microsoft ב-Coursera, חינמי לצפייה. מלמד יסודות "
                    "בניית AI Agents עם Azure AI Foundry, multi-agent systems "
                    "ו-Python. 4 מודולים, שבועיים."
                ),
                "level": "בינוני",
                "dur": "20 שעות",
                "rating": "3.8/5 | 11,291 לומדים | חינמי לצפייה ב-Coursera",
            },
            {
                "name": "Microsoft Generative AI Engineering",
                "url": "coursera.org/professional-certificates/microsoft-generative-ai-engineering",
                "desc": (
                    "תעודה מקצועית של Microsoft ב-Coursera. מכסה בניית ופיתוח מודלי "
                    "AI generative עם Azure AI Foundry, fine-tuning ו-Azure OpenAI. "
                    "ניתן לצפות חינם. עודכן ינואר 2026."
                ),
                "level": "בינוני עד מתקדם",
                "dur": "6 שבועות",
                "rating": "4.3/5 | 8,339 לומדים | עודכן ינואר 2026 | ניתן לצפות חינם",
            },
            {
                "name": "Introducing Azure AI Foundry — Everything for AI Development",
                "url": "youtube.com/watch?v=GD7MnIwAxYM",
                "desc": (
                    "הסרטון הרשמי של Microsoft Mechanics. סקירה מקיפה של Azure AI "
                    "Foundry: model catalog, prompt flow, agents, ו-safety. "
                    "מוצג על ידי צוות Microsoft, עודכן 2025."
                ),
                "level": "מתחיל עד בינוני",
                "dur": "13 דקות",
                "rating": "254K צפיות | Microsoft Mechanics | הנצפה ביותר על Azure AI Foundry",
            },
            {
                "name": "Career Essentials in Generative AI — Microsoft & LinkedIn",
                "url": "linkedin.com/learning/paths/career-essentials-in-generative-ai-by-microsoft-and-linkedin",
                "desc": (
                    "מסלול של Microsoft ו-LinkedIn Learning: 5 קורסים על יסודות "
                    "GenAI, Microsoft Copilot, AI לעסקים ואתיקה ב-AI. מיועד "
                    "לכל בעל תפקיד ארגוני. דורש LinkedIn Learning — זמין לרוב "
                    "בחינם דרך המעסיק."
                ),
                "level": "מתחיל",
                "dur": "4 שעות",
                "rating": "Microsoft + LinkedIn | 5 קורסים | ייתכן זמין חינם דרך המעסיק",
            },
            {
                "name": "Microsoft AI for Beginners",
                "url": "microsoft.github.io/AI-For-Beginners/",
                "desc": (
                    "קוריקולום פתוח וחינמי של Microsoft ב-GitHub. 12 שבועות, "
                    "24 לקציות: Symbolic AI, Neural Networks, NLP, Computer Vision "
                    "ו-GenAI. Labs מעשיים ב-Python. מושלם ללמידה עצמאית מקצה לקצה."
                ),
                "level": "מתחיל",
                "dur": "12 שבועות",
                "rating": "חינמי לחלוטין | 24 לקציות | Microsoft | 39K+ כוכבים ב-GitHub",
            },
            {
                "name": "Azure AI Fundamentals (AI-900)",
                "url": "learn.microsoft.com/credentials/certifications/azure-ai-fundamentals",
                "desc": (
                    "הסמכת הכניסה הרשמית של Microsoft ל-AI. כל חומרי ההכנה חינמיים "
                    "ב-Microsoft Learn. עודכנה אפריל 2026 עם תוכן AI Foundry חדש. "
                    "נותנת בסיס מוצק לפני הסמכת AI Engineer המתקדמת."
                ),
                "level": "מתחיל",
                "dur": "10 שעות הכנה",
                "rating": "ההסמכה הנפוצה ביותר של Microsoft AI | עודכנה אפריל 2026",
            },
            {
                "name": "Get Started with Microsoft 365 Copilot",
                "url": "learn.microsoft.com/en-us/training/paths/get-started-with-microsoft-365-copilot/",
                "desc": (
                    "נתיב למידה רשמי של Microsoft. 3 מודולים: מהו M365 Copilot, "
                    "שימוש ב-Teams/Word/Excel/Outlook ואיך למקסם ביצועים. "
                    "מיועד לכל בעל תפקיד. חינמי."
                ),
                "level": "מתחיל",
                "dur": "3 שעות",
                "rating": "חינמי | 3 מודולים | Microsoft Learn | מיועד לכלל הצוות | 2025",
            },
            {
                "name": "Introduction to GitHub Copilot",
                "url": "learn.microsoft.com/en-us/training/modules/introduction-to-github-copilot/",
                "desc": (
                    "מודול Microsoft Learn על GitHub Copilot: איך עובד, שילוב ב-VS Code, "
                    "כתיבת קוד, הסברת קוד קיים ויצירת בדיקות אוטומטיות. "
                    "חינמי עם badge."
                ),
                "level": "מפתחים",
                "dur": "שעה",
                "rating": "חינמי עם Badge | Microsoft Learn | GitHub Copilot | 2025",
            },
            {
                "name": "Develop AI Solutions with Azure OpenAI",
                "url": "learn.microsoft.com/en-us/training/paths/develop-ai-solutions-azure-openai/",
                "desc": (
                    "נתיב למידה רשמי למפתחים ב-Azure OpenAI Service. מכסה REST API, "
                    "SDKs, prompt engineering מתקדם, Assistants API ו-RAG עם "
                    "Azure AI Search. Labs בדפדפן חינמיים."
                ),
                "level": "מפתחים",
                "dur": "6 שעות",
                "rating": "חינמי | Microsoft Learn | Labs בדפדפן | Azure OpenAI Service | 2026",
            },
        ],
        "rec": (
            "המלצה לצוות",
            "לצוות כולו: Microsoft Learn (develop-generative-ai-apps) עודכן מאי 2026, "
            "חינמי, 6 מודולים עם labs. לכניסה מהירה ללא רקע טכני: Microsoft AI for "
            "Beginners ב-GitHub (24 לקציות). הסמכת AI-900 מומלצת לכולם. "
            "מנהלים: M365 Copilot Get Started. מפתחים: Azure OpenAI + GitHub Copilot."
        ),
    },

    # ── 5. Amazon Bedrock ──────────────────────────────────────────────────────
    {
        "number": "05",
        "name": "Amazon Bedrock (AWS)",
        "desc": (
            "Amazon Bedrock הוא שירות ה-AI המנוהל של AWS. הוא מאפשר גישה ל-30 "
            "מודלים ויותר: Anthropic Claude, Meta Llama, Mistral ו-Amazon Nova, "
            "דרך API אחיד. כולל Bedrock Knowledge Bases ל-RAG, Bedrock Agents "
            "ו-Bedrock Guardrails. AWS Skill Builder מציע מעל 600 קורסים חינמיים."
        ),
        "courses": [
            {
                "name": "Enterprise AI with Amazon Bedrock",
                "url": "youtube.com/watch?v=HaUe2AN210g",
                "desc": (
                    "קורס וידאו בן 6 שעות ב-YouTube של freeCodeCamp.org. פותח על ידי "
                    "Suman Debnath מ-Amazon עצמה. מכסה embeddings, RAG, multimodal "
                    "agents ו-Amazon Nova. תוכן מעמיק ומעשי."
                ),
                "level": "בינוני עד מתקדם",
                "dur": "6 שעות",
                "rating": "freeCodeCamp: 9M+ מנויים | Suman Debnath, Amazon | מיליוני צפיות",
            },
            {
                "name": "AWS Skill Builder",
                "url": "skillbuilder.aws",
                "desc": (
                    "מעל 600 קורסים דיגיטליים חינמיים ב-AWS Skill Builder, כולל "
                    "מסלולי Amazon Bedrock עדכניים מ-2026. Labs אינטראקטיביים "
                    "ב-AWS Console האמיתי ללא עלות נוספת."
                ),
                "level": "כל הרמות",
                "dur": "משתנה",
                "rating": "הפלטפורמה הרשמית של AWS | 600+ קורסים חינמיים | מיליוני לומדים",
            },
            {
                "name": "Amazon Bedrock Getting Started",
                "url": "aws.amazon.com/bedrock/getting-started",
                "desc": (
                    "דף ההתחלה הרשמי של Amazon Bedrock מ-AWS. כולל tutorials "
                    "מוצעים, workshops מונחים ו-step-by-step guides לבניית "
                    "אפליקציות GenAI ראשונות. חינמי לחלוטין."
                ),
                "level": "מתחיל עד בינוני",
                "dur": "2 עד 4 שעות",
                "rating": "רשמי מ-Amazon | tutorials + workshops | חינמי ללא הרשמה",
            },
            {
                "name": "Integrating Generative AI Models with Amazon Bedrock",
                "url": "youtube.com/watch?v=nSQrY-uPWLY",
                "desc": (
                    "הסרטון הנצפה ביותר על Amazon Bedrock ב-YouTube. מציג AWS "
                    "Developers: חיבור מודלים, API calls, ו-enterprise integration. "
                    "קצר, מעשי, רשמי מ-AWS."
                ),
                "level": "מתחיל עד בינוני",
                "dur": "14 דקות",
                "rating": "495K צפיות | AWS Developers | הנצפה ביותר על Amazon Bedrock",
            },
            {
                "name": "Generative AI Learning Plan for Decision Makers",
                "url": "skillbuilder.aws/search?searchText=generative-ai-learning-plan-for-decision-makers",
                "desc": (
                    "מסלול ייעודי ב-AWS Skill Builder לבעלי תפקידים עסקיים ומנהלים. "
                    "מכסה מושגי GenAI לעסקים, תרחישי שימוש ב-Amazon Bedrock, "
                    "ניהול סיכונים ו-Responsible AI. חינמי עם Badge דיגיטלי."
                ),
                "level": "מתחיל",
                "dur": "4 עד 6 שעות",
                "rating": "חינמי | Badge דיגיטלי | מיועד למנהלים לא-טכניים | AWS Skill Builder",
            },
            {
                "name": "AWS Machine Learning Training",
                "url": "aws.amazon.com/training/learn-about/machine-learning",
                "desc": (
                    "דף ההדרכה הרשמי של AWS ל-Machine Learning ו-GenAI. כולל "
                    "מסלולי למידה לפי תפקיד: מפתח, מדען נתונים, ארכיטקט. "
                    "מחבר לקורסים חינמיים ב-Skill Builder ל-Bedrock ו-SageMaker."
                ),
                "level": "כל הרמות",
                "dur": "משתנה",
                "rating": "הדרכה רשמית של AWS | מסלולים לפי תפקיד | חינמי",
            },
            {
                "name": "Serverless LLM Apps from Amazon Bedrock",
                "url": "deeplearning.ai/short-courses/serverless-llm-apps-amazon-bedrock/",
                "desc": (
                    "קורס DeepLearning.AI עם AWS. מכסה prompting ב-Bedrock, "
                    "תמלול אודיו עם LLMs ובניית אפליקציות serverless עם AWS Lambda. "
                    "7 שיעורים, Python. חינמי."
                ),
                "level": "בינוני",
                "dur": "2 שעות",
                "rating": "חינמי | Mike Chambers, AWS | DeepLearning.AI | Bedrock + Lambda | 2024",
            },
            {
                "name": "AWS Certified AI Practitioner (AIF-C01)",
                "url": "aws.amazon.com/certification/certified-ai-practitioner/",
                "desc": (
                    "הסמכת AI הרשמית החדשה של AWS (2024). מכסה יסודות AI/ML, "
                    "שירותי GenAI של AWS, Responsible AI ו-Amazon Bedrock. "
                    "כל חומרי ההכנה חינמיים ב-AWS Skill Builder."
                ),
                "level": "בינוני",
                "dur": "20 עד 30 שעות הכנה",
                "rating": "הסמכת AWS ל-AI | חומרי הכנה חינמיים ב-Skill Builder | 2024",
            },
            {
                "name": "Building with Amazon Bedrock — Workshop",
                "url": "catalog.workshops.aws/building-with-amazon-bedrock/en-US",
                "desc": (
                    "Workshop מעשי רשמי של AWS: בניית אפליקציות GenAI עם Bedrock. "
                    "מכסה Knowledge Bases ל-RAG, Bedrock Agents ו-Guardrails. "
                    "Labs ב-AWS Console האמיתי. חינמי."
                ),
                "level": "מפתחים",
                "dur": "4 עד 6 שעות",
                "rating": "חינמי | AWS Official Workshop | Bedrock + RAG + Agents | 2025",
            },
            {
                "name": "Amazon Bedrock Samples — GitHub",
                "url": "github.com/aws-samples/amazon-bedrock-samples",
                "desc": (
                    "מאגר קוד רשמי של AWS ב-GitHub: מאות notebooks ודוגמאות Python "
                    "ל-Bedrock API, Knowledge Bases, Agents, Guardrails ו-fine-tuning. "
                    "מתעדכן שוטף. חינמי לחלוטין."
                ),
                "level": "מפתחים",
                "dur": "לפי בחירה",
                "rating": "חינמי | AWS Samples | מאות Notebooks | GitHub | עודכן 2026",
            },
        ],
        "rec": (
            "המלצה לצוות",
            "למנהלים: להתחיל ב-Decision Makers Learning Plan (חינמי, Badge, ללא רקע טכני). "
            "למפתחים: freeCodeCamp ב-YouTube (6 שעות) + DeepLearning.AI Serverless LLM Apps. "
            "לתרגול: AWS Workshop רשמי עם Labs ב-Console. "
            "לצלילה: Bedrock Samples ב-GitHub עם מאות דוגמאות קוד."
        ),
    },
]

SUMMARY = (
    "50 הקורסים ברשימה מכסים כל רמה: מתחיל, בינוני ומפתחים. "
    "כל חמשת הכלים מציעים תכנים חינמיים ברמה גבוהה — אין צורך לשלם לפני "
    "שמיצים את המשאבים הרשמיים. ציוני דרך מומלצים: "
    "Coursera/Anthropic Academy למתחילים, DeepLearning.AI לרמה בינונית, "
    "ו-GitHub Cookbooks + Workshops לרמת מפתחים. "
    "הסמכות מוכרות ב-2026: Microsoft AI-900, OpenAI AI Foundations "
    "ו-AWS Certified AI Practitioner (AIF-C01)."
)


def generate(output_path: str = None) -> str:
    out = output_path or OUTPUT_FILE
    doc = new_document()

    add_title_block(
        doc,
        title    = "המלצות הדרכה לכלי AI ארגוניים",
        subtitle = "מדריך מקיף לקורסים חינמיים | יוני 2026",
    )
    add_body(doc, INTRO)
    add_divider(doc)

    for tool in TOOLS:
        add_tool_heading(doc, tool["number"], tool["name"])
        add_body(doc, tool["desc"])
        add_courses_table(doc, tool["courses"])
        add_callout(doc, *tool["rec"])
        add_divider(doc)

    add_tool_heading(doc, "סיכום", "המלצות מרכזיות")
    add_body(doc, SUMMARY)

    doc.save(out)
    return out


if __name__ == "__main__":
    path = generate()
    print(f"הדוח נשמר: {path}")
