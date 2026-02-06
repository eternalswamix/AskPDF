from flask import Flask
from app.core.config import Config
from app.core.extensions import supabase
from app.routes.main_routes import main_bp
from app.routes.auth_routes import auth_bp
from app.routes.pdf_routes import pdf_bp
from app.routes.chat_routes import chat_bp

def create_app():
    app = Flask(__name__, template_folder="templates")

    # Load config
    app.config.from_object(Config)

    # Register blueprints
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(pdf_bp)
    app.register_blueprint(chat_bp)

    return app
