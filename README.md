# AI Assistant — Major Project (Prompt Engineering)

## Overview (simple language)
This project is a small web app (Flask) that shows how to build an AI Assistant with three features:
1. Answer Questions
2. Summarize Text (supports uploading .txt files)
3. Generate Creative Content (stories, poems, ideas)

The app works with the OpenAI API if you set an environment variable. If you don't set a key, the app uses realistic mock responses so you can try the interface and flow.

## What's included
- `app.py` — The Flask web application.
- `utils.py` — Helper code with mock responses and a simple summarizer.
- `templates/` — HTML templates for the UI.
- `static/` — CSS for simple styling.
- `prompts.json` — Example prompt templates to choose from.
- `run_cli.py` — A small CLI version to run on a terminal.
- `requirements.txt` — Python packages needed.
- `data/history.json` — Conversation history (created when you run the app).
- `data/feedback.log` — Feedback log.

## How to run (local)
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. (Optional) set your OpenAI API key:
   ```bash
   export OPENAI_API_KEY="sk-..."
   ```
   On Windows (PowerShell):
   ```powershell
   setx OPENAI_API_KEY "sk-..."
   ```
3. Run the app:
   ```bash
   python app.py
   ```
4. Open http://127.0.0.1:5000 in your browser.

If you don't set an API key, the web app will still work but return mock responses.

## Extra ideas to make it more realistic
- Add user accounts and authentication.
- Add file upload for PDFs (extract text).
- Add rate-limiting and quotas.
- Add analytics dashboard showing which prompts are used most.
- Containerize with Docker for easy deployment.

## Project outcome
A working web app that demonstrates prompt engineering, UI design, feedback loop, and prompt library — good for showing in a major project demo.

