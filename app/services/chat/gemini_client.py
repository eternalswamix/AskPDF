import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# ✅ Safe limit: prevents embedding API errors on huge text
MAX_EMBED_CHARS = 10000


def get_embedding(text: str):
    safe_text = (text or "").strip()
    if len(safe_text) > MAX_EMBED_CHARS:
        safe_text = safe_text[:MAX_EMBED_CHARS]

    res = client.models.embed_content(
        model="models/text-embedding-004", # ✅ Explicit model path
        contents=safe_text
    )
    return res.embeddings[0].values


def generate_text(prompt: str):
    res = client.models.generate_content(
        model="gemini-2.5-flash-lite",
        contents=prompt
    )
    return res.text
