"""
youtube_researcher.py
---------------------
Searches YouTube for the best FREE tutorials for enterprise AI tools.
No API key required. Ranks by view count. Filters short clips (< 10 min).

Usage:
    venv/bin/python3 youtube_researcher.py                    # all 5 tools
    venv/bin/python3 youtube_researcher.py --tool 3           # tool #3 by number
    venv/bin/python3 youtube_researcher.py --tool "Bedrock"   # tool by name (partial)

Output:
    Prints top results + saves output/youtube_research.json
"""

import json, os, sys
import yt_dlp

OUTPUT_PATH = os.path.join(os.path.dirname(__file__), "output", "youtube_research.json")

TOOLS = [
    {
        "name": "Gemini Enterprise (Google)",
        "queries": [
            "Gemini Enterprise Google Workspace AI tutorial 2025 free",
            "Google Gemini AI enterprise beginners tutorial 2025",
        ],
    },
    {
        "name": "ChatGPT Enterprise (OpenAI)",
        "queries": [
            "ChatGPT Enterprise OpenAI tutorial 2025 free beginners",
            "OpenAI API tutorial enterprise 2025",
        ],
    },
    {
        "name": "Claude Enterprise (Anthropic)",
        "queries": [
            "Anthropic Claude enterprise tutorial 2025 free",
            "Claude API tutorial beginners 2025",
        ],
    },
    {
        "name": "Microsoft Azure AI Foundry",
        "queries": [
            "Azure AI Foundry tutorial 2025 free beginners",
            "Microsoft Azure OpenAI enterprise tutorial 2025",
        ],
    },
    {
        "name": "Amazon Bedrock (AWS)",
        "queries": [
            "Amazon Bedrock enterprise tutorial 2025 free",
            "AWS Bedrock AI tutorial beginners 2025",
        ],
    },
]

MIN_DURATION_SEC = 600
MAX_RESULTS_PER_QUERY = 8
TOP_PER_TOOL = 3


def seconds_to_hhmm(secs):
    if not secs:
        return "?"
    m, s = divmod(int(secs), 60)
    h, m = divmod(m, 60)
    return f"{h}:{m:02d}:{s:02d}" if h else f"{m}:{s:02d}"


def format_views(n):
    if not n:
        return "?"
    if n >= 1_000_000:
        return f"{n/1_000_000:.1f}M"
    if n >= 1_000:
        return f"{n/1_000:.0f}K"
    return str(n)


def search_youtube(query, limit):
    ydl_opts = {"quiet": True, "extract_flat": True}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        r = ydl.extract_info(f"ytsearch{limit}:{query}", download=False)
        return r.get("entries", [])


def research_tool(tool):
    candidates = []
    seen_ids = set()
    for query in tool["queries"]:
        for v in search_youtube(query, MAX_RESULTS_PER_QUERY):
            vid_id = v.get("id") or v.get("url", "")
            if vid_id in seen_ids:
                continue
            seen_ids.add(vid_id)
            duration = v.get("duration") or 0
            views = v.get("view_count") or 0
            if duration < MIN_DURATION_SEC:
                continue
            candidates.append({
                "title":     v.get("title", ""),
                "channel":   v.get("channel", v.get("uploader", "")),
                "views":     views,
                "views_fmt": format_views(views),
                "duration":  seconds_to_hhmm(duration),
                "url":       v.get("url") or f"https://www.youtube.com/watch?v={v.get('id','')}",
            })
    candidates.sort(key=lambda x: x["views"], reverse=True)
    return candidates[:TOP_PER_TOOL]


def select_tools(arg):
    """Return list of tools matching the --tool argument (number or partial name)."""
    if arg is None:
        return TOOLS
    if arg.isdigit():
        idx = int(arg) - 1
        if 0 <= idx < len(TOOLS):
            return [TOOLS[idx]]
        print(f"שגיאה: מספר כלי חייב להיות בין 1 ל-{len(TOOLS)}")
        sys.exit(1)
    matches = [t for t in TOOLS if arg.lower() in t["name"].lower()]
    if not matches:
        print(f"שגיאה: לא נמצא כלי עם השם '{arg}'")
        print("כלים זמינים:")
        for i, t in enumerate(TOOLS, 1):
            print(f"  {i}. {t['name']}")
        sys.exit(1)
    return matches


def print_results(tool_name, results):
    print(f"\n{'='*60}")
    print(f"  {tool_name}")
    print(f"{'='*60}")
    if not results:
        print("  לא נמצאו תוצאות מתאימות.")
        return
    for i, v in enumerate(results, 1):
        print(f"\n  #{i}  {v['title']}")
        print(f"       ערוץ: {v['channel']}")
        print(f"       צפיות: {v['views_fmt']}  |  משך: {v['duration']}")
        print(f"       {v['url']}")


def main():
    # Parse --tool argument
    tool_arg = None
    if "--tool" in sys.argv:
        idx = sys.argv.index("--tool")
        if idx + 1 < len(sys.argv):
            tool_arg = sys.argv[idx + 1]
        else:
            print("שגיאה: חסר ערך אחרי --tool")
            sys.exit(1)

    selected = select_tools(tool_arg)
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)

    # Load existing results so we don't overwrite other tools
    existing = {}
    if os.path.exists(OUTPUT_PATH):
        with open(OUTPUT_PATH, encoding="utf-8") as f:
            existing = json.load(f)

    for tool in selected:
        top = research_tool(tool)
        existing[tool["name"]] = top
        print_results(tool["name"], top)

    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(existing, f, ensure_ascii=False, indent=2)

    print(f"\n\nהתוצאות נשמרו: {OUTPUT_PATH}")
    return existing


if __name__ == "__main__":
    main()
