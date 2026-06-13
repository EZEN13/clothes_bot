import google.generativeai as genai
from pathlib import Path
from config import GEMINI_API_KEY, MAX_HISTORY, MODEL_NAME

genai.configure(api_key=GEMINI_API_KEY)

_system_prompt: str | None = None


def load_system_prompt() -> str:
    global _system_prompt
    if _system_prompt is None:
        prompt = Path("prompts/system_prompt.txt").read_text(encoding="utf-8")
        catalog = Path("data/catalog.json").read_text(encoding="utf-8")
        _system_prompt = f"{prompt}\n\nКАТАЛОГ ТОВАРОВ:\n{catalog}"
    return _system_prompt


async def get_gemini_response(history: list[dict]) -> str:
    model = genai.GenerativeModel(
        model_name=MODEL_NAME,
        system_instruction=load_system_prompt()
    )
    messages = history[-MAX_HISTORY:]
    gemini_history = []
    for msg in messages[:-1]:
        role = "user" if msg["role"] == "user" else "model"
        gemini_history.append({"role": role, "parts": [msg["content"]]})

    chat = model.start_chat(history=gemini_history)
    response = chat.send_message(messages[-1]["content"])
    return response.text


def extract_tag(text: str, tag: str) -> dict | None:
    open_tag, close_tag = f"<{tag}>", f"</{tag}>"
    if open_tag not in text or close_tag not in text:
        return None
    start = text.index(open_tag) + len(open_tag)
    end = text.index(close_tag)
    result = {}
    for line in text[start:end].strip().split("\n"):
        if ":" in line:
            k, v = line.split(":", 1)
            result[k.strip()] = v.strip()
    return result


def clean_response(text: str) -> str:
    for tag in ["order_ready", "lead_ready"]:
        o, c = f"<{tag}>", f"</{tag}>"
        if o in text and c in text:
            s = text.index(o)
            e = text.index(c) + len(c)
            text = (text[:s] + text[e:]).strip()
    return text
