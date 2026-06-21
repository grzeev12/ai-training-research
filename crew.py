import os
from crewai import Agent, Task, Crew, Process, LLM
from crewai_tools import SerperDevTool

search_tool = SerperDevTool()

llm = LLM(model="gpt-4o", api_key=os.getenv("OPENAI_API_KEY"))


def build_crew() -> Crew:
    research_agent = Agent(
        role="AI Enterprise Training Research Specialist",
        goal=(
            "Find the most current (2025-2026) training courses, certifications, "
            "and learning programs for enterprise AI tools. Search multiple times "
            "per tool to ensure comprehensive and up-to-date coverage."
        ),
        backstory=(
            "You are an expert at locating professional learning resources for enterprise AI platforms. "
            "You search systematically, always verifying information is current (2025-2026). "
            "You find official vendor programs, third-party platforms (Coursera, Udemy, "
            "LinkedIn Learning, Pluralsight, A Cloud Guru), free resources, and certifications. "
            "You always include estimated costs, duration, and skill level."
        ),
        tools=[search_tool],
        llm=llm,
        verbose=True,
        max_iter=15,
    )

    writer_agent = Agent(
        role="Senior Technical Writer in Hebrew",
        goal=(
            "Write a comprehensive, well-structured training recommendation report in Hebrew "
            "that Israeli technical teams can immediately act on."
        ),
        backstory=(
            "You are a senior technical writer specializing in Hebrew-language enterprise documentation. "
            "You write clear, professional Hebrew while keeping technical terms, product names, "
            "URLs, and platform names in English. You structure information logically with "
            "specific, actionable recommendations. Your reports are used by CTOs and "
            "technical leads to decide on training budgets."
        ),
        llm=llm,
        verbose=True,
    )

    research_task = Task(
        description=(
            "Search the internet thoroughly for training courses, certifications, and learning "
            "programs for EACH of the following 5 enterprise AI tools. "
            "Search at least twice per tool using different search queries.\n\n"
            "Tools to research:\n"
            "1. Gemini Enterprise / Google AI (Google AI Studio, Vertex AI, Google Cloud AI)\n"
            "2. ChatGPT Enterprise (OpenAI)\n"
            "3. Claude Enterprise (Anthropic)\n"
            "4. Microsoft Azure AI Foundry (formerly Azure OpenAI Service)\n"
            "5. Amazon Bedrock (AWS)\n\n"
            "For EACH tool find:\n"
            "- Official vendor training and certification programs with URLs\n"
            "- Courses on Coursera, Udemy, LinkedIn Learning, Pluralsight\n"
            "- Free resources: YouTube playlists, official docs tutorials, workshops\n"
            "- Professional certifications or badges\n"
            "- Approximate cost (free / paid amount)\n"
            "- Estimated duration\n"
            "- Skill level (beginner / intermediate / advanced)\n\n"
            "Focus exclusively on 2025-2026 content. Include direct URLs."
        ),
        agent=research_agent,
        expected_output=(
            "A detailed structured list for each of the 5 tools containing "
            "3-5 training options each, with name, platform, URL, cost, duration, and level."
        ),
    )

    write_task = Task(
        description=(
            "Based on the research, write a complete training recommendation report in HEBREW.\n\n"
            "LANGUAGE RULES:\n"
            "- Report body: Hebrew\n"
            "- Product names, course names, platform names, URLs, technical terms: keep in English\n\n"
            "OUTPUT FORMAT — use exactly these Markdown headings:\n\n"
            "# המלצות הדרכה לכלי AI ארגוניים\n\n"
            "## מבוא\n"
            "[2-3 משפטים בעברית]\n\n"
            "## 1. Gemini Enterprise (Google)\n"
            "### תיאור\n"
            "[תיאור קצר בעברית]\n"
            "### אפשרויות הדרכה\n"
            "- [Course Name] — [תיאור קצר] | פלטפורמה: X | עלות: X | רמה: X | משך: X\n"
            "[3-5 אפשרויות]\n"
            "### המלצה שלנו\n"
            "[איזו אפשרות הכי מתאימה לצוות טכני ישראלי ולמה]\n\n"
            "## 2. ChatGPT Enterprise (OpenAI)\n"
            "[same structure]\n\n"
            "## 3. Claude Enterprise (Anthropic)\n"
            "[same structure]\n\n"
            "## 4. Microsoft Azure AI Foundry\n"
            "[same structure]\n\n"
            "## 5. Amazon Bedrock (AWS)\n"
            "[same structure]\n\n"
            "## סיכום\n"
            "[2-3 משפטים עם המלצות מרכזיות]\n\n"
            "Write the full report — do not abbreviate or skip any section."
        ),
        agent=writer_agent,
        context=[research_task],
        expected_output=(
            "A complete Hebrew training recommendation report with all 5 tools covered, "
            "following the exact markdown structure specified."
        ),
    )

    return Crew(
        agents=[research_agent, writer_agent],
        tasks=[research_task, write_task],
        process=Process.sequential,
        verbose=True,
    )
