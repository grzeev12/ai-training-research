# AI Training Research

**50 קורסים חינמיים לכלי AI ארגוניים — 10 לכל כלי.**

אתר עברי RTL המרכז את הקורסים החינמיים המומלצים ביותר לחמשת כלי ה-AI הארגוניים המובילים, עם פילטר לפי רמה (מתחיל / בינוני / מפתחים).

🌐 **[ai-training-research.vercel.app](https://ai-training-research.vercel.app)**

---

## כלי AI מכוסים

| # | כלי | ספק |
|---|-----|-----|
| 01 | Gemini Enterprise | Google |
| 02 | ChatGPT Enterprise | OpenAI |
| 03 | Claude Enterprise | Anthropic |
| 04 | Azure AI Foundry | Microsoft |
| 05 | Amazon Bedrock | AWS |

---

## התקנה מהירה

```bash
git clone https://github.com/grzeev12/ai-training-research
cd ai-training-research

python3.11 -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt

cp .env.example .env
# Edit .env and fill in your API keys
```

---

## הרצה

```bash
# בנה את האתר (docs/index.html)
python3 generate_website.py

# צור קובץ Word
python3 main.py --local

# רענן צפיות YouTube
python3 youtube_researcher.py

# חפש קורסים חזקים יותר (דורש SERPER_API_KEY + OPENAI_API_KEY)
python3 course_updater.py
```

---

## איך מוסיפים קורס

עריכת `generate_report.py` — הוסף dict לרשימת `"courses"` של הכלי הרלוונטי:

```python
{
    "name":   "שם הקורס",
    "url":    "coursera.org/learn/...",   # ללא https://
    "desc":   "תיאור בעברית של מה הקורס מלמד...",
    "level":  "מתחיל",                   # ראה רמות חוקיות למטה
    "dur":    "6 שעות",
    "rating": "4.8/5 | 806K לומדים | Google | Coursera",
}
```

רמות חוקיות: `מתחיל` · `מתחיל עד בינוני` · `בינוני` · `בינוני עד מתקדם` · `מפתחים` · `כל הרמות`

אחרי כל שינוי: `python3 generate_website.py`

---

## עדכון אוטומטי יומי

GitHub Actions רץ כל יום ב-09:00 (שעון ישראל):

1. `youtube_researcher.py` — מרענן מספרי צפיות
2. `course_updater.py` — מחפש קורסים חזקים יותר (Serper + GPT-4o mini)
3. `generate_website.py` — מייצר HTML מחדש
4. Commit + Push → Vercel מפרסם אוטומטית

**מה מתעדכן:** מספרי צפיות + החלפת קורסים חלשים אם נמצא קורס חזק ב-2+ נקודות.
**מה לא מתעדכן:** `generate_report.py` — רשימת הבסיס. תמיד ידנית.

---

## משתני סביבה

העתק `.env.example` ל-`.env` ומלא:

| משתנה | מטרה | חובה? |
|--------|-------|--------|
| `OPENAI_API_KEY` | GPT-4o mini בעדכון קורסים, CrewAI | לעדכון אוטומטי |
| `SERPER_API_KEY` | חיפוש גוגל בעדכון קורסים, CrewAI | לעדכון אוטומטי |
| `OPENAI_MODEL_NAME` | מודל CrewAI (ברירת מחדל: gpt-4o) | לא |
| `TELEGRAM_BOT_TOKEN` | התראות על שינויים | לא |
| `TELEGRAM_CHAT_ID` | יעד התראות Telegram | לא |

**GitHub Secrets** (לא ב-.env): `OPENAI_API_KEY`, `SERPER_API_KEY`, `TELEGRAM_BOT_TOKEN`, `TELEGRAM_CHAT_ID`

---

## מבנה קבצים

```
├── generate_report.py      ← מקור האמת: כל 50 הקורסים
├── generate_website.py     ← בונה docs/index.html
├── word_writer.py          ← מנוע Word RTL עברית
├── youtube_researcher.py   ← מחפש צפיות YouTube
├── course_updater.py       ← עדכון קורסים אוטומטי
├── main.py                 ← נקודת כניסה ראשית
├── crew.py                 ← CrewAI research agent
├── data/overrides.json     ← החלפות קורסים אוטומטיות
├── docs/index.html         ← האתר המוגמר (נוצר אוטומטית)
├── vercel.json             ← הגדרות Vercel
└── .github/workflows/
    └── daily_update.yml    ← GitHub Actions cron
```

---

## Claude Code

פרויקט זה מוגדר עם Claude Code. לאחר clone:

```bash
claude    # פתח Claude Code בתיקיית הפרויקט
/prime    # טען קונטקסט מלא של הפרויקט
```
