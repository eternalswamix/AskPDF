import os
from dotenv import load_dotenv

load_dotenv()

# ✅ Allow HTTP for OAuth (Crucial for localhost testing)
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

class Config:
    SECRET_KEY = os.getenv("FLASK_SECRET", "fallback_secret_key")

    SUPABASE_URL = os.getenv("SUPABASE_URL")
    SUPABASE_KEY = os.getenv("SUPABASE_KEY")

    if not SUPABASE_URL or not SUPABASE_KEY:
        raise ValueError("❌ SUPABASE_URL or SUPABASE_KEY missing in .env")

    GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
    GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
    BASE_URL = os.getenv("BASE_URL")

