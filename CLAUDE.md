# CLAUDE.md — AI Training Research

## What This Project Does

Generates and publishes a Hebrew RTL website listing the **50 best free AI training courses** for 5 enterprise AI tools (Gemini, ChatGPT, Claude, Azure AI, Amazon Bedrock) — 10 courses per tool.

**Live site:** https://ai-training-research.vercel.app

Two outputs:
1. **`docs/index.html`** — static website served by Vercel, rebuilt daily
2. **`output/המלצות_הדרכות_AI.docx`** — professional Word document (Hebrew RTL)

---

## Tech Stack

| Layer | Tech |
|-------|------|
| Site generator | Python 3.11 (pure stdlib + f-strings, no framework) |
| Hosting | Vercel (static, `outputDirectory: docs`) |
| Word engine | `python-docx` with custom RTL/Hebrew support |
| YouTube research | `yt-dlp` (no API key needed) |
| Course updates | Serper API (search) + OpenAI GPT-4o mini (evaluation) |
| AI research mode | CrewAI + Serper |
| CI/CD | GitHub Actions — runs daily at 09:00 Israel time |

---

## Directory Structure

```
ai-training-research/
├── generate_report.py      ← SOURCE OF TRUTH: all 50 courses (TOOLS list, INTRO, SUMMARY)
├── generate_website.py     ← Builds docs/index.html from TOOLS + overrides
├── word_writer.py          ← RTL Word engine (Hebrew, right-to-left, 4-layer RTL)
├── youtube_researcher.py   ← Fetches YouTube view counts via yt-dlp
├── course_updater.py       ← Daily: finds stronger courses via Serper + GPT-4o mini
├── main.py                 ← Entry point: --local (Word from hardcoded data) or --crew (AI research)
├── crew.py                 ← CrewAI research agent (used by main.py --crew)
├── requirements.txt        ← Python dependencies
├── .env                    ← Local API keys (NOT committed to git)
├── .env.example            ← Template for .env (committed)
├── data/
│   └── overrides.json      ← Auto-generated course replacements (committed, not sensitive)
├── docs/
│   └── index.html          ← Generated static site (committed, deployed by Vercel)
├── output/
│   ├── המלצות_הדרכות_AI.docx  ← Generated Word doc (gitignored)
│   └── youtube_research.json   ← YouTube view counts cache
├── vercel.json             ← Tells Vercel: serve from docs/, no build command
├── .vercelignore           ← Excludes *.py from Vercel's build
└── .github/workflows/
    └── daily_update.yml    ← GitHub Actions: 09:00 Israel time cron
```

---

## Installation

```bash
# 1. Clone and enter
git clone https://github.com/grzeev12/ai-training-research
cd ai-training-research

# 2. Create virtualenv (Python 3.11 required)
python3.11 -m venv venv

# 3. Activate
source venv/bin/activate          # macOS/Linux
# venv\Scripts\activate           # Windows

# 4. Install dependencies
pip install -r requirements.txt

# 5. Create .env from template
cp .env.example .env
# Then fill in your API keys in .env
```

---

## Running

### Generate the website (main daily task)
```bash
python3 generate_website.py
# → writes docs/index.html
# → open docs/index.html in browser to preview
```

### Generate the Word document
```bash
python3 main.py --local
# → writes output/המלצות_הדרכות_AI.docx (seconds)

python3 main.py --crew
# → uses CrewAI to research online, then generates Word (5-10 min)
```

### Refresh YouTube view counts
```bash
python3 youtube_researcher.py
# → writes output/youtube_research.json
```

### Run the course updater (requires API keys)
```bash
python3 course_updater.py
# → searches for stronger courses, updates data/overrides.json if found
# → requires SERPER_API_KEY + OPENAI_API_KEY in .env
```

---

## Environment Variables

All vars go in `.env` locally. For GitHub Actions, add as **Repository Secrets** at:
`Settings → Secrets and variables → Actions`

| Variable | Used by | Required? |
|----------|---------|-----------|
| `OPENAI_API_KEY` | `course_updater.py`, `crew.py` | Yes (for auto-updates and --crew mode) |
| `SERPER_API_KEY` | `course_updater.py`, `crew.py` | Yes (for auto-updates and --crew mode) |
| `OPENAI_MODEL_NAME` | `crew.py` | No (defaults to gpt-4o) |
| `TELEGRAM_BOT_TOKEN` | `course_updater.py` | No (optional notifications) |
| `TELEGRAM_CHAT_ID` | `course_updater.py` | No (optional notifications) |

Without `OPENAI_API_KEY` and `SERPER_API_KEY`, `generate_website.py` and `main.py --local` still work — only the auto-course-updater and AI research mode require them.

**GitHub Secrets already configured:** `OPENAI_API_KEY`, `SERPER_API_KEY`

---

## Code Conventions

- **Python 3.11**, no type annotations required
- **No framework** — the site is built with f-strings in `build_html()`
- **RTL Hebrew** — all user-facing text is in Hebrew. Direction is `rtl`. Keep it.
- **All CSS is inline** inside the Python f-string in `generate_website.py`. Double-brace `{{}}` for literal CSS braces.
- **No HTML files are edited manually** — always edit `generate_website.py` and regenerate
- **No course URLs with `https://`** — the `url` field in course dicts stores bare URLs (e.g. `coursera.org/learn/...`). `full_url()` adds `https://` at render time.
- **Level values** must be one of: `מתחיל`, `מתחיל עד בינוני`, `מתחיל עד מפתחים`, `בינוני`, `בינוני עד מתקדם`, `מפתחים`, `מתקדם`, `כל הרמות`
- **`python3`** — not `python` (Python 2 may be on PATH on some systems)

---

## How Courses Are Managed

### Manual edits (source of truth)
Edit `generate_report.py` → `TOOLS` list. Each course is a dict:
```python
{
    "name":   "Course Name",
    "url":    "coursera.org/learn/...",   # no https://
    "desc":   "Hebrew description...",
    "level":  "מתחיל",
    "dur":    "6 שעות",
    "rating": "4.8/5 | 806K לומדים | Google | Coursera",
}
```
After editing, run `python3 generate_website.py` to rebuild.

### Automatic overrides (daily)
`course_updater.py` writes replacements to `data/overrides.json`.
`generate_website.py` applies overrides on top of `TOOLS` at build time.
Overrides never touch `generate_report.py` — they are a separate layer.

### Pinned courses (never auto-replaced)
Courses whose URL contains: `academy.openai.com`, `anthropic.skilljar.com/claude-platform-101`, `skillbuilder.aws`, `learn.microsoft.com/credentials/certifications/azure-ai-fundamentals`, `cloudskillsboost.google`, etc. See `PINNED_FRAGMENTS` in `course_updater.py`.

---

## Danger Zones — Read Before Changing

1. **`generate_report.py`** — The master course list. Verify every URL before adding. A broken URL goes live on the public site.

2. **`generate_website.py` f-string CSS** — CSS is inside a Python f-string. All `{` and `}` that are CSS (not Python vars) must be doubled: `{{` and `}}`. Forgetting this breaks the generator with a `KeyError`.

3. **`data/overrides.json`** — Committed to git. Contains auto-generated course replacements. Do not edit manually unless you know the schema. If corrupted, replace with `{"overrides": []}`.

4. **`docs/index.html`** — Never edit this file manually. It is always regenerated. Your changes will be overwritten by the next `generate_website.py` run.

5. **`.env`** — Must never be committed. It is in `.gitignore`. The `COMPOSIO_API_KEY` in `.env` is a leftover from another project — not used here.

6. **`vercel.json`** — Must keep `"buildCommand": ""` (empty string). If a build command is set, Vercel will try to execute Python and fail.

7. **Level strings** — If you add a level string not in `LEVEL_GROUP` in `generate_website.py`, the card will default to `beginner` group silently. Add new levels to both `LEVEL_GROUP` and `LEVEL_COLORS`.

---

## Daily Automation (GitHub Actions)

Runs every day at **09:00 Israel time** (UTC+3 summer = `cron: '0 6 * * *'`):

1. `youtube_researcher.py` — refreshes view counts
2. `course_updater.py` — searches for stronger courses, updates `data/overrides.json`
3. `generate_website.py` — rebuilds `docs/index.html`
4. Commits and pushes changed files → Vercel auto-redeploys in ~30s

**What the auto-updater changes:** `data/overrides.json` only — never `generate_report.py`.
**What it never replaces:** pinned courses (official portals, certifications).
**Replacement threshold:** new course must score 2+ points above the weakest current course (GPT-4o mini scoring, 1–10 scale).

---

## Common Issues

| Problem | Cause | Fix |
|---------|-------|-----|
| `ModuleNotFoundError: docx` | python-docx not installed | `pip install -r requirements.txt` |
| `KeyError: 'some-key'` in generate_website.py | Unescaped `{` or `}` in CSS f-string | Double the brace: `{{` / `}}` |
| Vercel build fails "Found main.py" | .vercelignore missing or wrong | Check `.vercelignore` has `*.py` |
| Course level not showing in filter | Level string not in `LEVEL_GROUP` | Add to `LEVEL_GROUP` and `LEVEL_COLORS` in `generate_website.py` |
| `course_updater.py` exits silently | Missing `SERPER_API_KEY` or `OPENAI_API_KEY` | Add to `.env` or GitHub Secrets |
| Override not applied to site | `data/overrides.json` URL doesn't match exactly | Check `replace_url` matches the exact `url` value in `TOOLS` |
| Word doc is LTR (not RTL) | RTL layers stripped | See `word_writer.py` — 4-layer RTL must all be present |
