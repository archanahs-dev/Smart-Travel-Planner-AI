"""Chat assistant that answers questions about the generated trip (Gemini)."""
import os

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

MODELS = [m for m in [os.getenv("GEMINI_MODEL"), "gemini-2.5-flash", "gemini-flash-latest"] if m]


def has_key():
    return bool(os.getenv("GEMINI_API_KEY"))


def ask_trip_assistant(question, plan_summary, history):
    if not has_key():
        return ("No API key found. Make sure the file is named exactly .env, sits next to app.py, "
                "contains GEMINI_API_KEY=your_key, and restart the app.")
    try:
        from google import genai
    except ImportError:
        return "The google-genai package is missing. Run: python -m pip install google-genai"

    recent = "\n".join(f"{m['role']}: {m['content']}" for m in history[-6:])
    prompt = (
        "You are a helpful travel assistant inside a Smart Travel Planner app. Answer ONLY using and "
        "building on the trip plan below. Be concise and practical. If the user asks to change the plan, "
        "suggest the changes in text. Do not invent prices; say they are estimates.\n\n"
        f"TRIP PLAN:\n{plan_summary}\n\nCONVERSATION:\n{recent}\n\nUSER QUESTION: {question}"
    )
    client = genai.Client(api_key=os.getenv("GEMINI_API_KEY").strip())
    last_error = None
    for model in dict.fromkeys(MODELS):  # try each model once, in order
        try:
            return client.models.generate_content(model=model, contents=prompt).text
        except Exception as exc:
            last_error = f"{exc.__class__.__name__}: {exc}"
    return f"Gemini request failed. Details: {last_error}"