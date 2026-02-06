from flask import Blueprint, render_template, session, redirect, url_for

main_bp = Blueprint("main", __name__)

@main_bp.route("/")
def index():
    return render_template("index.html", user=session.get("user"))

@main_bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("main.index"))
