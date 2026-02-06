from flask import Flask
from app.core.config import Config
from app.core.extensions import supabase
from app.routes.main import main_bp
from app.routes.auth import auth_bp
from app.routes.pdf import pdf_bp
from app.routes.chat import chat_bp

def create_app():
    app = Flask(__name__, template_folder="templates")

    # Load config
    app.config.from_object(Config)

    # Initialize extensions
    from app.core.extensions import oauth
    oauth.init_app(app)
    
    oauth.register(
        name='google',
        client_id=Config.GOOGLE_CLIENT_ID,
        client_secret=Config.GOOGLE_CLIENT_SECRET,
        server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
        client_kwargs={
            'scope': 'openid email profile'
        }
    )

    # Logging
    from app.core.logging_config import setup_logging
    setup_logging()

    # Register blueprints
    from app.core.errors import errors_bp
    app.register_blueprint(errors_bp)

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(pdf_bp)
    app.register_blueprint(chat_bp)

    return app
