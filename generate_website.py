"""
generate_website.py
-------------------
Generates a professional Hebrew RTL website from the TOOLS data.
Output: output/index.html  (open directly in any browser, no server needed)

Usage:
    venv/bin/python3 generate_website.py
"""

import json, os, html as html_mod
from generate_report import TOOLS, INTRO

OUTPUT_HTML  = os.path.join(os.path.dirname(__file__), "docs", "index.html")
YOUTUBE_JSON = os.path.join(os.path.dirname(__file__), "output", "youtube_research.json")

TOOL_COLORS = {
    "01": {"bg": "#1a73e8", "light": "#e8f0fe", "label": "Google"},
    "02": {"bg": "#10a37f", "light": "#e6f7f3", "label": "OpenAI"},
    "03": {"bg": "#cc785c", "light": "#fdf0ec", "label": "Anthropic"},
    "04": {"bg": "#0078d4", "light": "#e6f2fc", "label": "Microsoft"},
    "05": {"bg": "#ff9900", "light": "#fff4e0", "label": "AWS"},
}

TOOL_ICONS = {
    "01": "G",
    "02": "⊕",
    "03": "A",
    "04": "⊞",
    "05": "⚡",
}

LEVEL_COLORS = {
    "מתחיל":              "#2e7d32",
    "מתחיל עד בינוני":   "#388e3c",
    "מתחיל עד מפתחים":   "#43a047",
    "בינוני":             "#1565c0",
    "בינוני עד מתקדם":   "#1976d2",
    "מפתחים":             "#6a1b9a",
    "מתקדם":              "#ad1457",
    "כל הרמות":           "#546e7a",
}


def e(s):
    return html_mod.escape(str(s))


def is_youtube(url):
    return "youtube.com" in url or "youtu.be" in url


def full_url(url):
    if url.startswith("http"):
        return url
    return "https://" + url


def level_badge(level):
    color = LEVEL_COLORS.get(level, "#546e7a")
    return (
        f'<span class="badge" style="background:{color}22;color:{color};'
        f'border:1px solid {color}44">{e(level)}</span>'
    )


def course_card(course, color):
    url = full_url(course["url"])
    yt = is_youtube(course["url"])
    rating = course.get("rating", "")
    border_color = "#ff0000" if yt else color
    yt_badge = (
        '<span class="yt-badge">▶ YouTube</span>' if yt else ""
    )

    return f"""
    <div class="card" style="border-right:4px solid {border_color}">
      <div class="card-header">
        <div class="card-title">{e(course['name'])} {yt_badge}</div>
        <a class="card-url" href="{e(url)}" target="_blank" rel="noopener">{e(course['url'])}</a>
      </div>
      <p class="card-desc">{e(course['desc'])}</p>
      <div class="card-meta">
        {level_badge(course['level'])}
        <span class="badge dur-badge">⏱ {e(course['dur'])}</span>
        {f'<span class="rating-text">{e(rating)}</span>' if rating else ''}
      </div>
    </div>"""


def sidebar_item(tool, color_info):
    num = tool["number"]
    icon = TOOL_ICONS.get(num, num)
    short = color_info["label"]
    full = tool["name"]
    bg = color_info["bg"]
    return f"""
        <div class="nav-item" data-tool="{e(num)}" onclick="showTool('{e(num)}')"
             style="--accent:{e(bg)}">
          <span class="nav-icon" style="background:{e(bg)}">{icon}</span>
          <div class="nav-labels">
            <span class="nav-short">{e(short)}</span>
            <span class="nav-full">{e(full)}</span>
          </div>
        </div>"""


def tool_section(tool):
    num = tool["number"]
    color_info = TOOL_COLORS.get(num, {"bg": "#333", "light": "#f5f5f5", "label": ""})
    bg = color_info["bg"]
    light = color_info["light"]
    cards_html = "\n".join(course_card(c, bg) for c in tool["courses"])
    rec_title, rec_body = tool["rec"]

    return f"""
  <section class="tool-section" id="tool-{e(num)}" style="display:none">
    <div class="tool-header" style="background:{e(bg)}">
      <span class="tool-num">{e(num)}</span>
      <h2 class="tool-name">{e(tool['name'])}</h2>
    </div>
    <p class="tool-desc">{e(tool['desc'])}</p>
    <div class="cards-grid">
{cards_html}
    </div>
    <div class="callout" style="background:{e(light)};border-right:4px solid {e(bg)}">
      <div class="callout-title" style="color:{e(bg)}">💡 {e(rec_title)}</div>
      <p class="callout-body">{e(rec_body)}</p>
    </div>
  </section>"""


def build_html():
    sidebar_items = "".join(
        sidebar_item(t, TOOL_COLORS.get(t["number"], {"bg": "#333", "label": ""}))
        for t in TOOLS
    )
    sections = "".join(tool_section(t) for t in TOOLS)
    first_num = TOOLS[0]["number"]

    return f"""<!DOCTYPE html>
<html lang="he" dir="rtl">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>המלצות הדרכה לכלי AI ארגוניים</title>
<style>
  *, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}

  body {{
    font-family: -apple-system, "Segoe UI", Arial, sans-serif;
    background: #f0f2f5;
    color: #1a1a1a;
    display: flex;
    min-height: 100vh;
    direction: rtl;
  }}

  /* ── Sidebar ── */
  .sidebar {{
    width: 240px;
    min-width: 240px;
    background: #12172b;
    display: flex;
    flex-direction: column;
    position: fixed;
    top: 0; right: 0; bottom: 0;
    overflow-y: auto;
    z-index: 100;
  }}

  .sidebar-logo {{
    padding: 28px 20px 20px;
    border-bottom: 1px solid #ffffff18;
  }}

  .sidebar-logo h1 {{
    font-size: 14px;
    font-weight: 600;
    color: #fff;
    line-height: 1.5;
  }}

  .sidebar-logo p {{
    font-size: 11px;
    color: #ffffff66;
    margin-top: 4px;
  }}

  .nav-label {{
    font-size: 10px;
    font-weight: 600;
    letter-spacing: 1px;
    color: #ffffff44;
    text-transform: uppercase;
    padding: 20px 20px 8px;
  }}

  .nav-item {{
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 10px 16px;
    cursor: pointer;
    border-radius: 8px;
    margin: 2px 8px;
    transition: background 0.15s;
  }}

  .nav-item:hover {{ background: #ffffff12; }}

  .nav-item.active {{
    background: var(--accent, #1a73e8)22;
    border-right: 3px solid var(--accent, #1a73e8);
    padding-right: 13px;
  }}

  .nav-icon {{
    width: 34px;
    height: 34px;
    border-radius: 8px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 15px;
    font-weight: 700;
    color: #fff;
    flex-shrink: 0;
  }}

  .nav-labels {{ display: flex; flex-direction: column; overflow: hidden; }}
  .nav-short {{ font-size: 12px; font-weight: 600; color: #fff; }}
  .nav-full  {{ font-size: 10px; color: #ffffff66; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }}

  .sidebar-footer {{
    margin-top: auto;
    padding: 16px 20px;
    border-top: 1px solid #ffffff18;
    font-size: 10px;
    color: #ffffff33;
  }}

  /* ── Main ── */
  .main {{
    margin-right: 240px;
    flex: 1;
    display: flex;
    flex-direction: column;
  }}

  .topbar {{
    background: #fff;
    border-bottom: 1px solid #e0e0e0;
    padding: 16px 32px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    position: sticky;
    top: 0;
    z-index: 50;
  }}

  .topbar-title {{ font-size: 17px; font-weight: 600; color: #1a1a1a; }}
  .topbar-sub   {{ font-size: 12px; color: #888; margin-top: 2px; }}

  .topbar-badge {{
    background: #e8f5e9;
    color: #2e7d32;
    font-size: 11px;
    font-weight: 600;
    padding: 4px 12px;
    border-radius: 20px;
    border: 1px solid #a5d6a7;
  }}

  .content {{ padding: 32px; max-width: 900px; }}

  /* ── Tool header ── */
  .tool-header {{
    display: flex;
    align-items: center;
    gap: 16px;
    border-radius: 12px 12px 0 0;
    padding: 20px 28px;
    color: #fff;
  }}

  .tool-num {{
    font-size: 13px;
    font-weight: 700;
    background: #ffffff33;
    padding: 3px 10px;
    border-radius: 20px;
  }}

  .tool-name {{ font-size: 22px; font-weight: 700; }}

  .tool-desc {{
    font-size: 14px;
    color: #444;
    line-height: 1.7;
    padding: 20px 28px;
    background: #fff;
    border: 1px solid #e8e8e8;
    border-top: none;
    border-radius: 0 0 12px 12px;
    margin-bottom: 20px;
  }}

  /* ── Cards ── */
  .cards-grid {{ display: flex; flex-direction: column; gap: 14px; margin-bottom: 20px; }}

  .card {{
    background: #fff;
    border-radius: 10px;
    padding: 18px 20px;
    border: 1px solid #e8e8e8;
    transition: box-shadow 0.15s;
  }}

  .card:hover {{ box-shadow: 0 4px 16px #0001; }}

  .card-header {{ margin-bottom: 8px; }}
  .card-title  {{ font-size: 15px; font-weight: 600; color: #1a1a1a; margin-bottom: 4px; }}
  .card-url    {{ font-size: 12px; color: #1a73e8; text-decoration: none; }}
  .card-url:hover {{ text-decoration: underline; }}
  .card-desc   {{ font-size: 13px; color: #555; line-height: 1.65; margin-bottom: 12px; }}

  .card-meta   {{ display: flex; align-items: center; gap: 8px; flex-wrap: wrap; }}

  .badge {{
    font-size: 11px;
    font-weight: 600;
    padding: 3px 10px;
    border-radius: 20px;
    white-space: nowrap;
  }}

  .dur-badge {{ background: #f3f4f6; color: #555; border: 1px solid #ddd; }}

  .yt-badge {{
    font-size: 10px;
    font-weight: 700;
    background: #ff000015;
    color: #cc0000;
    border: 1px solid #ff000030;
    padding: 2px 8px;
    border-radius: 20px;
    margin-right: 8px;
  }}

  .rating-text {{ font-size: 11px; color: #888; }}

  /* ── Callout ── */
  .callout {{
    border-radius: 10px;
    padding: 18px 20px;
    margin-bottom: 40px;
  }}

  .callout-title {{ font-size: 14px; font-weight: 700; margin-bottom: 8px; }}
  .callout-body  {{ font-size: 13px; color: #444; line-height: 1.7; }}

  /* ── Intro panel ── */
  .intro-panel {{
    background: #fff;
    border-radius: 12px;
    border: 1px solid #e8e8e8;
    padding: 24px 28px;
    margin-bottom: 28px;
    font-size: 14px;
    color: #444;
    line-height: 1.8;
  }}
</style>
</head>
<body>

<nav class="sidebar">
  <div class="sidebar-logo">
    <h1>המלצות הדרכה<br>לכלי AI ארגוניים</h1>
    <p>כל המשאבים חינמיים | יוני 2026</p>
  </div>
  <div class="nav-label">כלי AI</div>
  {sidebar_items}
  <div class="sidebar-footer">AI Training Research v5</div>
</nav>

<div class="main">
  <div class="topbar">
    <div>
      <div class="topbar-title">מרכז הדרכה לכלי AI ארגוניים</div>
      <div class="topbar-sub">5 כלים · 25 קורסים מאומתים · כולם חינמיים</div>
    </div>
    <span class="topbar-badge">✓ חינמי לחלוטין</span>
  </div>

  <div class="content">
    <div class="intro-panel">{e(INTRO)}</div>
{sections}
  </div>
</div>

<script>
  function showTool(num) {{
    document.querySelectorAll('.tool-section').forEach(s => s.style.display = 'none');
    document.querySelectorAll('.nav-item').forEach(n => n.classList.remove('active'));
    const sec = document.getElementById('tool-' + num);
    if (sec) sec.style.display = 'block';
    const nav = document.querySelector('[data-tool="' + num + '"]');
    if (nav) nav.classList.add('active');
    window.scrollTo({{ top: 0, behavior: 'smooth' }});
  }}
  showTool('{first_num}');
</script>
</body>
</html>"""


if __name__ == "__main__":
    os.makedirs(os.path.dirname(OUTPUT_HTML), exist_ok=True)
    html = build_html()
    with open(OUTPUT_HTML, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"האתר נוצר: {OUTPUT_HTML}")
    print("פתח בדפדפן: open docs/index.html")
