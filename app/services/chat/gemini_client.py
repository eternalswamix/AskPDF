import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

# ✅ Safe limit: prevents embedding API errors on huge text
MAX_EMBED_CHARS = 10000

try:
    from google.api_core import exceptions
    GoogleAPIExceptions = (exceptions.ResourceExhausted, exceptions.InvalidArgument, exceptions.Unauthenticated)
except ImportError:
    # ✅ Fallback if google-api-core is missing (prevents Vercel crash)
    exceptions = None
    GoogleAPIExceptions = ()  # Empty tuple to use in except block


# ✅ Custom Exception for cleaner frontend handling
class GeminiAPIError(Exception):
    def __init__(self, message, original_error=None):
        super().__init__(message)
        self.original_error = original_error


def get_client(api_key=None):
    """Returns a GenAI client using user key or system default."""
    key = api_key or os.getenv("GEMINI_API_KEY")
    if not key:
        raise GeminiAPIError("No Gemini API Key provided. Please add one in your Profile.")
    return genai.Client(api_key=key)


def get_embedding(text: str, api_key=None):
    safe_text = (text or "").strip()
    if len(safe_text) > MAX_EMBED_CHARS:
        safe_text = safe_text[:MAX_EMBED_CHARS]

    try:
        client = get_client(api_key)
        res = client.models.embed_content(
            model="models/text-embedding-004", # ✅ Explicit model path
            contents=safe_text
        )
        return res.embeddings[0].values
    
    except GoogleAPIExceptions as e:
         # Map known Google exceptions to readable errors
        if exceptions and isinstance(e, exceptions.ResourceExhausted):
            raise GeminiAPIError("⚠️ Daily Quota Exceeded. Please use a different API Key or try again tomorrow.")
        if exceptions and isinstance(e, exceptions.InvalidArgument):
            raise GeminiAPIError("❌ Invalid API Key. Please update it in your Profile.")
        if exceptions and isinstance(e, exceptions.Unauthenticated):
            raise GeminiAPIError("❌ API Key authentication failed. Key might be expired.")
        # Fallback
        raise GeminiAPIError(f"Gemini API Error: {str(e)}", original_error=e)

    except Exception as e:
        raise GeminiAPIError(f"Embedding Error: {str(e)}", original_error=e)


def generate_text(prompt: str, api_key=None):
    try:
        client = get_client(api_key)
        res = client.models.generate_content(
            model="gemini-2.5-flash-lite",
            contents=prompt
        )
        return res.text
        
    except GoogleAPIExceptions as e:
         # Map known Google exceptions to readable errors
        if exceptions and isinstance(e, exceptions.ResourceExhausted):
            raise GeminiAPIError("⚠️ Daily Quota Exceeded. Please use a different API Key or try again tomorrow.")
        if exceptions and isinstance(e, exceptions.InvalidArgument):
            raise GeminiAPIError("❌ Invalid API Key. Please update it in your Profile.")
        if exceptions and isinstance(e, exceptions.Unauthenticated):
            raise GeminiAPIError("❌ API Authentication failed. Please check your key.")
        raise GeminiAPIError(f"Gemini API Error: {str(e)}", original_error=e)

    except Exception as e:
        raise GeminiAPIError(f"Generation Error: {str(e)}", original_error=e)
