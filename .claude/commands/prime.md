Read the following files to fully understand this project, then produce a working brief:

1. Read CLAUDE.md
2. Read requirements.txt
3. Read data/overrides.json (note how many auto-replacements exist and for which tools)
4. Run: find . -maxdepth 2 -not -path './.git/*' -not -path './venv/*' -not -path './__pycache__/*' -not -path './docs/*' -not -path './output/*' | sort
5. Run: python3 --version
6. Check whether venv/ exists: ls venv/bin/python3 2>/dev/null && echo "venv OK" || echo "venv missing — run: python3.11 -m venv venv && pip install -r requirements.txt"
7. Check whether .env exists: ls .env 2>/dev/null && echo ".env present" || echo ".env missing — copy .env.example to .env and fill in API keys"

After reading everything, respond with a structured brief in this exact format:

---
## Project Brief — AI Training Research

**What it is:** [1-sentence description]

**Live site:** https://ai-training-research.vercel.app

**Current state:**
- Total courses: [count from generate_report.py]
- Auto-overrides active: [count from data/overrides.json]
- Last site rebuild: [check git log --oneline -3]

**Run commands:**
| Task | Command |
|------|---------|
| Rebuild website | `python3 generate_website.py` |
| Generate Word doc | `python3 main.py --local` |
| Refresh YouTube counts | `python3 youtube_researcher.py` |
| Search for better courses | `python3 course_updater.py` |
| AI research mode | `python3 main.py --crew` |

**Central files:**
- `generate_report.py` — edit this to add/remove/change courses
- `generate_website.py` — edit this to change site layout or styling
- `data/overrides.json` — auto-generated, do not edit manually
- `docs/index.html` — never edit, always regenerated

**Environment:**
- Python venv: [OK / missing]
- .env file: [present / missing — needs: OPENAI_API_KEY, SERPER_API_KEY]
- GitHub Secrets: OPENAI_API_KEY ✓, SERPER_API_KEY ✓ (already set)

**Before you change anything:**
1. Never edit `docs/index.html` directly — it gets overwritten
2. All CSS in `generate_website.py` is inside a Python f-string — use `{{` and `}}` for literal CSS braces
3. Course `url` fields must NOT include `https://` — the code adds it automatically
4. After any change to `generate_report.py` or `generate_website.py`, run `python3 generate_website.py` to rebuild
5. Never commit `.env` — it is gitignored

**Danger zones:** [list from CLAUDE.md]
---
