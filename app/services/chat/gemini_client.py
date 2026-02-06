import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

# ✅ Safe limit: prevents embedding API errors on huge text
MAX_EMBED_CHARS = 10000

def get_client(api_key=None):
    """Returns a GenAI client using user key or system default."""
    key = api_key or os.getenv("GEMINI_API_KEY")
    if not key:
        raise ValueError("No Gemini API Key provided (User or System).")
    return genai.Client(api_key=key)


def get_embedding(text: str, api_key=None):
    safe_text = (text or "").strip()
    if len(safe_text) > MAX_EMBED_CHARS:
        safe_text = safe_text[:MAX_EMBED_CHARS]

    client = get_client(api_key)
    try:
        res = client.models.embed_content(
            model="models/text-embedding-004", # ✅ Explicit model path
            contents=safe_text
        )
        return res.embeddings[0].values
    except Exception as e:
        # If user key fails, maybe fallback? For now, we error out as it's cleaner debugging.
        raise e


def generate_text(prompt: str, api_key=None):
    client = get_client(api_key)
    res = client.models.generate_content(
        model="gemini-2.5-flash-lite",
        contents=prompt
    )
    return res.text
