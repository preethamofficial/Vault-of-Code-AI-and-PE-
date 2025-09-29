"""
CLI interface for the AI Assistant project.
Run: python run_cli.py
"""
import os
import json
from utils import mock_answer_question, mock_summarize_text, mock_generate_creative

def main():
    print("AI Assistant — CLI demo")
    while True:
        print("\nChoose function:")
        print("1. Answer Questions")
        print("2. Summarize Text")
        print("3. Generate Creative Content")
        print("4. Exit")
        ch = input("Select: ").strip()
        if ch == "4":
            break
        if ch == "1":
            q = input("Enter your question: ")
            print("--- Result ---")
            print(mock_answer_question(q))
        elif ch == "2":
            t = input("Paste (or type) text to summarize: ")
            print("--- Summary ---")
            print(mock_summarize_text(t))
        elif ch == "3":
            s = input("Enter a creative seed (one line): ")
            print("--- Creative ---")
            print(mock_generate_creative(s))
        else:
            print("Invalid choice.")

if __name__ == '__main__':
    main()
