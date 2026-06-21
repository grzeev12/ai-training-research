"""
main.py — שתי דרכי הפעלה:

  1. python main.py
     מריץ את CrewAI לחפש באינטרנט ומייצר Word מהפלט (5-10 דקות).

  2. python main.py --local
     מייצר Word מיידית מהתוכן המוכן ב-generate_report.py (שניות).
"""

import os, sys
from dotenv import load_dotenv

load_dotenv()


def run_crew():
    from crew import build_crew
    from word_writer import create_word_document

    print("[1/2] מחקר מהאינטרנט — זה לוקח כמה דקות...")
    result = build_crew().kickoff()
    print("[2/2] יוצר קובץ Word...")
    return create_word_document(str(result))


def run_local():
    from generate_report import generate
    print("יוצר דוח מהתוכן המוכן...")
    return generate()


if __name__ == "__main__":
    mode = "--local" if "--local" in sys.argv else "--crew"
    path = run_local() if mode == "--local" else run_crew()
    print(f"\nהדוח נשמר: {path}")
