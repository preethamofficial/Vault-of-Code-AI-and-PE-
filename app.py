import os
import json
import time
import uuid
from datetime import datetime
from flask import Flask, request, render_template, redirect, url_for, send_from_directory, flash
try:
    import openai
except Exception:
    openai = None
from utils import mock_answer_question, mock_summarize_text, mock_generate_creative

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET", "change-me-123")

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
os.makedirs(DATA_DIR, exist_ok=True)
HISTORY_FILE = os.path.join(DATA_DIR, "history.json")
FEEDBACK_FILE = os.path.join(DATA_DIR, "feedback.log")

OPENAI_KEY = os.environ.get("OPENAI_API_KEY")
if OPENAI_KEY and openai:
    openai.api_key = OPENAI_KEY

def save_history(entry):
    history = []
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            try:
                history = json.load(f)
            except:
                history = []
    history.append(entry)
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(history, f, indent=2)

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    if request.method == "POST":
        function = request.form.get("function")
        temperature = float(request.form.get("temperature") or 0.5)
        prompt_template = request.form.get("prompt_template") or ""
        user_input = request.form.get("user_input", "")
        uploaded_file = request.files.get("upload_file")
        file_text = ""
        if uploaded_file and uploaded_file.filename:
            try:
                file_text = uploaded_file.read().decode("utf-8", errors="ignore")
            except:
                file_text = ""
        # Construct prompt
        if function == "answer":
            prompt = prompt_template or f"Answer the question concisely: {user_input}"
            if OPENAI_KEY and openai:
                try:
                    resp = openai.ChatCompletion.create(
                        model="gpt-3.5-turbo",
                        messages=[{"role":"user","content":prompt}],
                        temperature=temperature,
                        max_tokens=400
                    )
                    result = resp["choices"][0]["message"]["content"].strip()
                except Exception as e:
                    result = f"OpenAI API error: {e}"
            else:
                result = mock_answer_question(user_input)
        elif function == "summarize":
            text_to_summarize = file_text or user_input
            prompt = prompt_template or f"Summarize the following text:\n\n{text_to_summarize}"
            if OPENAI_KEY and openai and text_to_summarize.strip():
                try:
                    resp = openai.ChatCompletion.create(
                        model="gpt-3.5-turbo",
                        messages=[{"role":"user","content":prompt}],
                        temperature=temperature,
                        max_tokens=300
                    )
                    result = resp["choices"][0]["message"]["content"].strip()
                except Exception as e:
                    result = f"OpenAI API error: {e}"
            else:
                result = mock_summarize_text(text_to_summarize)
        elif function == "creative":
            prompt = prompt_template or f"Write creative content based on: {user_input}"
            if OPENAI_KEY and openai:
                try:
                    resp = openai.ChatCompletion.create(
                        model="gpt-3.5-turbo",
                        messages=[{"role":"user","content":prompt}],
                        temperature=temperature,
                        max_tokens=500
                    )
                    result = resp["choices"][0]["message"]["content"].strip()
                except Exception as e:
                    result = f"OpenAI API error: {e}"
            else:
                result = mock_generate_creative(user_input)
        else:
            result = "Unknown function selected."

        # Save conversation to history
        entry = {
            "id": str(uuid.uuid4()),
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "function": function,
            "user_input": user_input if user_input else ("[file uploaded]" if file_text else ""),
            "result": result
        }
        save_history(entry)

    # Load prompt templates for the UI
    prompts = []
    try:
        with open(os.path.join(os.path.dirname(__file__), "prompts.json"), "r", encoding="utf-8") as f:
            prompts = json.load(f)
    except:
        prompts = []
    return render_template("index.html", result=result, prompts=prompts)

@app.route("/history")
def history():
    history = []
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            try:
                history = json.load(f)
            except:
                history = []
    return render_template("history.html", history=history)

@app.route("/feedback", methods=["POST"])
def feedback():
    helpful = request.form.get("helpful")
    notes = request.form.get("notes", "")
    entry = {"timestamp": datetime.utcnow().isoformat() + "Z", "helpful": helpful, "notes": notes}
    with open(FEEDBACK_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry) + "\\n")
    flash("Thanks for your feedback!")
    return redirect(url_for("index"))

@app.route("/download/history")
def download_history():
    if os.path.exists(HISTORY_FILE):
        return send_from_directory(os.path.dirname(HISTORY_FILE), os.path.basename(HISTORY_FILE), as_attachment=True)
    return "No history found.", 404

if __name__ == "__main__":
    app.run(debug=True, port=5000)
