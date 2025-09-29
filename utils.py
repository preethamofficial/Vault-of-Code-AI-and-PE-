import re
import random
import textwrap

def mock_answer_question(question: str) -> str:
    q = question.lower()
    # Simple rule-based answers for a few common question types
    if "capital of" in q:
        country = q.split("capital of")[-1].strip(" ?")
        capitals = {
            "france": "Paris",
            "india": "New Delhi",
            "japan": "Tokyo",
            "brazil": "Brasília",
            "canada": "Ottawa",
        }
        return f"The capital of {country.title()} is {capitals.get(country.strip(), 'unknown (no API key set)')}."
    if "who is" in q or q.startswith("who"):
        return "I don't have internet access here, but if you provide details I can try to summarize or explain."
    if "how to" in q or "how do i" in q:
        return "Break the task into small steps, try one step at a time, and test as you go."
    # Default fallback: make a short, helpful-sounding reply
    sample = [
        "Good question — here's a concise answer based on general knowledge.",
        "I can't call the cloud API because no key is set. Here's a mock answer to illustrate the format.",
        "This is a placeholder answer. Replace OPENAI_API_KEY with your key to get real AI responses."
    ]
    return random.choice(sample)

def mock_summarize_text(text: str, max_sentences=3) -> str:
    if not text or not text.strip():
        return "No text provided to summarize."
    # Very simple summarizer: split into sentences and take first few meaningful ones
    sentences = re.split(r'(?<=[.!?])\\s+', text.strip())
    sentences = [s.strip() for s in sentences if len(s.strip())>10]
    summary = " ".join(sentences[:max_sentences])
    if len(sentences) > max_sentences:
        summary += " ..."
    return summary

def mock_generate_creative(prompt: str) -> str:
    # Simple short story generator using a few templates
    characters = ["A curious child", "An old sailor", "A brave coder", "A lonely dragon", "An adventurous cat"]
    settings = ["in a quiet village", "on a floating island", "inside a secret library", "at the edge of the sea", "under neon lights"]
    hooks = [
        "finds a map that leads to something unexpected.",
        "meets someone who changes their view of the world.",
        "discovers a small machine that talks.",
        "learns that a story they read is coming true.",
        "decides to fix something everyone else ignores."
    ]
    c = random.choice(characters)
    s = random.choice(settings)
    h = random.choice(hooks)
    story = f"{c} {s} {h} They learn an important lesson and the day ends with a hopeful twist."
    return story
