"""
course_updater.py
-----------------
Daily script: searches for stronger AI courses and replaces the weakest
course per tool when a significantly better alternative is found.

Uses: Serper API (search) + OpenAI GPT-4o mini (evaluation)
Output: writes/updates data/overrides.json
        sends Telegram summary when replacements happen

Required env vars (GitHub Secrets):
    SERPER_API_KEY    — serper.dev API key
    OPENAI_API_KEY    — OpenAI API key
    TELEGRAM_BOT_TOKEN — optional, for change notifications
    TELEGRAM_CHAT_ID   — optional, your Telegram chat/user ID
"""

import json
import os
import re
import sys
import copy
import requests
from pathlib import Path

# ── Config ────────────────────────────────────────────────────────────────────

SERPER_API_KEY    = os.environ.get("SERPER_API_KEY", "")
OPENAI_API_KEY    = os.environ.get("OPENAI_API_KEY", "")
TELEGRAM_TOKEN    = os.environ.get("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHAT_ID  = os.environ.get("TELEGRAM_CHAT_ID", "")

BASE_DIR       = Path(__file__).parent
OVERRIDES_FILE = BASE_DIR / "data" / "overrides.json"

# New course must score at least this many points above the weakest current one
MIN_IMPROVEMENT = 2

# English search query per tool number
TOOL_SEARCHES = {
    "01": "Google Gemini AI free course 2025 2026 highly rated Coursera OR DeepLearning",
    "02": "ChatGPT OpenAI free AI course 2025 2026 best rated Coursera OR DeepLearning",
    "03": "Anthropic Claude AI free course 2025 2026 best",
    "04": "Microsoft Azure AI free course 2025 2026 highly rated Coursera OR Microsoft Learn",
    "05": "Amazon Bedrock AWS AI free course 2025 2026 highly rated Coursera OR DeepLearning",
}

# URL fragments — courses whose URL contains any of these are never auto-replaced
PINNED_FRAGMENTS = [
    "academy.openai.com",
    "introducing-openai-certification",
    "anthropic.skilljar.com/claude-platform-101",
    "anthropic.skilljar.com/ai-fluency",
    "skillbuilder.aws",
    "aws.amazon.com/bedrock/getting-started",
    "learn.microsoft.com/credentials/certifications/azure-ai-fundamentals",
    "cloudskillsboost.google/paths/183",
    "aws.amazon.com/certification/certified-ai-practitioner",
    "cloudskillsboost.google",       # Google's main skills platform — always keep
    "workspace.google.com/training", # Google Workspace official
    "ai.google/education",           # Google AI hub
]

# ── Overrides I/O ─────────────────────────────────────────────────────────────

def load_overrides():
    OVERRIDES_FILE.parent.mkdir(parents=True, exist_ok=True)
    if OVERRIDES_FILE.exists():
        return json.loads(OVERRIDES_FILE.read_text(encoding="utf-8"))
    return {"overrides": []}


def save_overrides(data):
    OVERRIDES_FILE.write_text(
        json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8"
    )


# ── Scoring ───────────────────────────────────────────────────────────────────

def is_pinned(url: str) -> bool:
    return any(frag in url for frag in PINNED_FRAGMENTS)


def heuristic_score(course: dict) -> int:
    """Return a 1-10 quality score based on the rating string and url."""
    rating = course.get("rating", "")
    score = 5

    # Learner count: "1.8M+ לומדים" or "806K+ לומדים"
    m = re.search(r"(\d+(?:\.\d+)?)([KMkm])\+?\s*לומד", rating)
    if m:
        n, unit = float(m.group(1)), m.group(2).upper()
        learners = n * 1_000_000 if unit == "M" else n * 1_000
        if learners >= 1_000_000: score = max(score, 9)
        elif learners >= 500_000:  score = max(score, 8)
        elif learners >= 100_000:  score = max(score, 7)
        elif learners >= 10_000:   score = max(score, 6)

    # Star rating: "4.8/5"
    m = re.search(r"(\d\.\d)/5", rating)
    if m:
        stars = float(m.group(1))
        if stars >= 4.7:  score = max(score, 8)
        elif stars >= 4.5: score = max(score, 7)

    # Quality signals in rating text
    if any(w in rating for w in ["badge", "Badge", "תעודה"]):  score = max(score, 7)
    if any(w in rating for w in ["רשמי", "Official", "official"]): score = max(score, 7)
    if "חינמי לחלוטין" in rating: score = max(score, 6)

    # Major platforms always score at least 7
    url = course.get("url", "")
    if any(p in url for p in ["coursera.org", "deeplearning.ai", "learn.microsoft.com",
                               "anthropic.skilljar", "skillbuilder.aws"]):
        score = max(score, 7)

    return min(score, 10)


# ── Serper search ─────────────────────────────────────────────────────────────

def serper_search(query: str) -> list[dict]:
    """Return up to 8 organic search results."""
    resp = requests.post(
        "https://google.serper.dev/search",
        headers={"X-API-KEY": SERPER_API_KEY, "Content-Type": "application/json"},
        json={"q": query, "num": 8, "hl": "en"},
        timeout=20,
    )
    resp.raise_for_status()
    results = []
    for r in resp.json().get("organic", []):
        results.append({
            "title":   r.get("title", ""),
            "url":     r.get("link", ""),
            "snippet": r.get("snippet", ""),
        })
    return results


# ── GPT-4o mini evaluation ────────────────────────────────────────────────────

def gpt_evaluate(tool_name: str, current_courses: list, candidates: list,
                 weakest: dict, weakest_score: int) -> dict:
    """Ask GPT-4o mini whether any candidate beats the weakest course."""
    from openai import OpenAI
    client = OpenAI(api_key=OPENAI_API_KEY)

    current_summary = "\n".join(
        f"- {c['name']} | score {heuristic_score(c)}/10 | level: {c['level']} | {c.get('rating','')[:70]}"
        for c in current_courses
    )

    candidates_text = "\n".join(
        f"{i+1}. {r['title']}\n   URL: {r['url']}\n   {r['snippet'][:180]}"
        for i, r in enumerate(candidates)
    )

    prompt = f"""You are a quality assessor for AI training courses for "{tool_name}".

CURRENT COURSES (weakest = "{weakest['name']}", heuristic score {weakest_score}/10):
{current_summary}

SEARCH CANDIDATES:
{candidates_text}

TASK:
Find ONE candidate that is (a) clearly better than the weakest current course,
(b) not a duplicate of any current course, and (c) free to access (or free to audit).

Scoring rubric (1-10):
- 9-10: Major MOOC platform (Coursera, DeepLearning.AI), 500K+ learners, official cert/badge
- 7-8: Reputable source, 50K+ learners or official company course, free
- 5-6: Good content but smaller audience
- 1-4: Blog, irrelevant, paid-only, non-English

Only recommend replacement if candidate score >= {weakest_score + MIN_IMPROVEMENT}.

Respond with valid JSON only:
{{
  "should_replace": true | false,
  "reason": "one English sentence",
  "candidate_score": <int 1-10>,
  "new_course": {{
    "name": "<short English course name>",
    "url": "<exact URL without https://>",
    "desc": "<2-3 sentences in Hebrew RTL about what the course teaches>",
    "level": "<one of: מתחיל | מתחיל עד בינוני | בינוני | מפתחים | כל הרמות>",
    "dur": "<duration in Hebrew, e.g. 6 שעות | 45 דקות | 4 שבועות>",
    "rating": "<key stats: platform, learner count, price — in Hebrew>"
  }}
}}
If should_replace is false, new_course can be null."""

    resp = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
        response_format={"type": "json_object"},
        timeout=30,
    )
    return json.loads(resp.choices[0].message.content)


# ── Telegram ─────────────────────────────────────────────────────────────────

def send_telegram(text: str):
    if not TELEGRAM_TOKEN or not TELEGRAM_CHAT_ID:
        print(f"[Telegram disabled] {text[:120]}")
        return
    try:
        requests.post(
            f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage",
            json={"chat_id": TELEGRAM_CHAT_ID, "text": text, "parse_mode": "HTML"},
            timeout=10,
        )
    except Exception as exc:
        print(f"[Telegram error] {exc}")


# ── Main ─────────────────────────────────────────────────────────────────────

def main():
    if not SERPER_API_KEY or not OPENAI_API_KEY:
        print("SERPER_API_KEY or OPENAI_API_KEY not set — skipping course update")
        sys.exit(0)

    sys.path.insert(0, str(BASE_DIR))
    from generate_report import TOOLS

    overrides_data = load_overrides()
    # Build a lookup: replace_url → new_course (already-applied overrides)
    active_overrides = {o["replace_url"]: o["new_course"] for o in overrides_data["overrides"]}

    changes = []

    for tool in TOOLS:
        num       = tool["number"]
        tool_name = tool["name"]
        base_courses = tool["courses"]

        print(f"\n── {tool_name} ──")

        # Apply existing overrides to get current effective course list
        effective = [
            copy.deepcopy(active_overrides.get(c["url"], c))
            for c in base_courses
        ]

        # Identify weakest non-pinned course
        scoreable = [
            (i, c, heuristic_score(c))
            for i, c in enumerate(effective)
            if not is_pinned(c["url"])
        ]
        if not scoreable:
            print("  All courses pinned — skipping")
            continue

        scoreable.sort(key=lambda x: x[2])
        w_idx, weakest, weakest_score = scoreable[0]
        print(f"  Weakest: '{weakest['name']}' (score {weakest_score}/10)")

        # Search for candidates
        query      = TOOL_SEARCHES.get(num, f"{tool_name} AI free course 2026")
        candidates = serper_search(query)
        print(f"  Search returned {len(candidates)} results")

        # Remove URLs already in the current list
        current_urls = {c["url"] for c in effective}
        candidates = [r for r in candidates if r["url"] not in current_urls]
        if not candidates:
            print("  All candidates already in course list")
            continue

        # Ask GPT-4o mini
        try:
            result = gpt_evaluate(tool_name, effective, candidates, weakest, weakest_score)
        except Exception as exc:
            print(f"  GPT error: {exc}")
            continue

        print(f"  GPT: should_replace={result.get('should_replace')} — {result.get('reason','')}")

        if not result.get("should_replace"):
            continue

        new_course = result.get("new_course")
        if not new_course:
            continue

        # Strip https:// if GPT included it
        new_course["url"] = re.sub(r"^https?://", "", new_course["url"].strip())

        # Safety: skip if URL looks too short or suspicious
        if len(new_course["url"]) < 10 or " " in new_course["url"]:
            print(f"  Suspicious URL '{new_course['url']}' — skipping")
            continue

        # Remove any previous override for the same weakest URL
        overrides_data["overrides"] = [
            o for o in overrides_data["overrides"]
            if o["replace_url"] != weakest["url"]
        ]

        overrides_data["overrides"].append({
            "tool_number":          num,
            "tool_name":            tool_name,
            "replace_url":          weakest["url"],
            "replaced_course_name": weakest["name"],
            "candidate_score":      result.get("candidate_score", 0),
            "new_course":           new_course,
        })

        active_overrides[weakest["url"]] = new_course

        changes.append(
            f"<b>{tool_name}</b>\n"
            f"  ❌ הוסר: {weakest['name']} (ציון {weakest_score}/10)\n"
            f"  ✅ נוסף: {new_course['name']} (ציון {result.get('candidate_score',0)}/10)\n"
            f"  🔗 {new_course['url']}"
        )
        print(f"  ✅ Replacing '{weakest['name']}' → '{new_course['name']}'")

    save_overrides(overrides_data)
    print(f"\nDone. {len(changes)} replacement(s) made.")

    if changes:
        msg = (
            "🎓 <b>AI Training Site — עדכון קורסים אוטומטי</b>\n\n"
            + "\n\n".join(changes)
            + "\n\n🌐 ai-training-research.vercel.app"
        )
        send_telegram(msg)


if __name__ == "__main__":
    main()
