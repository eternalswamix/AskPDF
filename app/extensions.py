import os
from supabase import create_client
from app.config import Config

# ✅ Prefer service role for backend actions like Storage Upload
SUPABASE_SERVICE_KEY = os.getenv("SUPABASE_SERVICE_KEY")
SUPABASE_ANON_KEY = os.getenv("SUPABASE_KEY")

if not Config.SUPABASE_URL:
    raise ValueError("❌ SUPABASE_URL missing in .env")

if not SUPABASE_SERVICE_KEY and not SUPABASE_ANON_KEY:
    raise ValueError("❌ SUPABASE_SERVICE_KEY / SUPABASE_KEY missing in .env")

supabase = create_client(
    Config.SUPABASE_URL,
    SUPABASE_SERVICE_KEY or SUPABASE_ANON_KEY
)
