from functools import wraps
from flask import session, redirect, url_for, request

def login_required(view_func):
    @wraps(view_func)
    def wrapper(*args, **kwargs):
        if "user" not in session:
            next_url = request.full_path.rstrip("?")
            return redirect(url_for("auth.login", next=next_url))
        return view_func(*args, **kwargs)
    return wrapper
