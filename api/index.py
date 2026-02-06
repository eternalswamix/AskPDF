import os
import sys

# Add the current directory to Python path to ensure module resolution works
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from app import create_app
    app = create_app()
except Exception as e:
    # 🚨 CRITICAL: Catch errors during simplified startup and show them in browser
    from flask import Flask
    app = Flask(__name__)
    
    @app.route("/", defaults={"path": ""})
    @app.route("/<path:path>")
    def catch_all(path):
        import traceback
        trace = traceback.format_exc()
        return f"""
        <html>
            <head><title>Startup Error</title></head>
            <body style="font-family: monospace; padding: 20px; background: #1a1a1a; color: #ff5555;">
                <h1>⚠️ Application Failed to Start</h1>
                <h2>Error: {str(e)}</h2>
                <pre style="background: #000; padding: 15px; border-radius: 5px; overflow: auto;">{trace}</pre>
                <hr>
                <h3>Environment Variables Check:</h3>
                <ul>
                    <li>FLASK_ENV: {os.getenv('FLASK_ENV', 'Not Set')}</li>
                    <li>SUPABASE_URL: {'✅ Set' if os.getenv('SUPABASE_URL') else '❌ MISSING'}</li>
                    <li>SUPABASE_KEY: {'✅ Set' if os.getenv('SUPABASE_KEY') else '❌ MISSING'}</li>
                    <li>GOOGLE_CLIENT_ID: {'✅ Set' if os.getenv('GOOGLE_CLIENT_ID') else '❌ MISSING'}</li>
                </ul>
            </body>
        </html>
        """, 500