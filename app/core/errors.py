from flask import Blueprint, render_template
from werkzeug.exceptions import HTTPException
import logging

errors_bp = Blueprint('errors', __name__)
logger = logging.getLogger(__name__)

@errors_bp.app_errorhandler(404)
def not_found_error(error):
    if not str(error).startswith("404"): # Avoid double logging if needed
        logger.warning(f"404 Error: {error}")
    return render_template('404.html'), 404

@errors_bp.app_errorhandler(403)
def forbidden_error(error):
    logger.warning(f"403 Access Denied: {error}")
    return render_template('403.html'), 403

@errors_bp.app_errorhandler(500)
def internal_error(error):
    logger.error(f"500 Internal Server Error: {error}", exc_info=True)
    return render_template('500.html'), 500

@errors_bp.app_errorhandler(Exception)
def handle_exception(e):
    # Pass through HTTP errors
    if isinstance(e, HTTPException):
        return e
        
    logger.exception(f"Unhandled Exception: {e}")
    return render_template('500.html'), 500
