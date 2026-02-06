from flask import Blueprint, render_template, request, redirect, url_for, session
from app.core.extensions import supabase
from app.core.decorators import login_required
from app.services.mailer import send_credentials_email

auth_bp = Blueprint("auth", __name__)


# ✅ Helper: check profile complete
def is_profile_complete(user_id: str) -> bool:
    res = supabase.table("users") \
        .select("username, first_name,last_name,phone_no") \
        .eq("id", user_id) \
        .single() \
        .execute()

    if not res.data:
        return False

    return bool(
        res.data.get("username")
        and res.data.get("first_name")
        and res.data.get("last_name")
        and res.data.get("phone_no")
    )


# -----------------------------
# Register
# -----------------------------
@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    next_url = request.args.get("next", "/upload")

    if request.method == "POST":
        username = request.form.get("username", "").strip().lower()
        first_name = request.form.get("first_name", "").strip()
        last_name = request.form.get("last_name", "").strip()
        phone_no = request.form.get("phone_no", "").strip()
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "").strip()

        # ✅ Validation
        if not all([username, first_name, last_name, phone_no, email, password]):
            return render_template("register.html", error="All fields are required.", user=session.get("user"))

        if " " in username or len(username) < 3:
            return render_template(
                "register.html",
                error="Username must be at least 3 characters and contain no spaces.",
                user=session.get("user")
            )

        try:
            # ✅ Check username uniqueness
            existing_username = supabase.table("users").select("id").eq("username", username).execute()
            if existing_username.data:
                return render_template("register.html", error="Username already taken. Choose another one.", user=session.get("user"))

            # ✅ Register via Supabase Auth
            auth = supabase.auth.sign_up({"email": email, "password": password})

            if auth.user is None:
                return render_template("register.html", error="Email already exists. Please login instead.", user=session.get("user"))

            user_data = auth.user

            # ✅ Save additional fields
            supabase.table("users").upsert({
                "id": user_data.id,
                "email": user_data.email,
                "username": username,
                "first_name": first_name,
                "last_name": last_name,
                "phone_no": phone_no
            }).execute()

            try:
                send_credentials_email(user_data.email, username, password)
            except Exception as mail_err:
                print("❌ Email sending failed:", str(mail_err))
                # (optional) show on UI
                return render_template("register.html", error="Account created but email sending failed. Please contact support.", user=session.get("user"))

            # ✅ Store in session (NOW includes username for navbar)
            session["user"] = {
                "id": user_data.id,
                "email": user_data.email,
                "username": username
            }

            return redirect(next_url)

        except Exception as e:
            msg = str(e).lower()

            if "duplicate" in msg or "already registered" in msg or "user already" in msg:
                return render_template("register.html", error="This email is already registered. Please login.", user=session.get("user"))

            if "users_username_unique" in msg or "username" in msg:
                return render_template("register.html", error="Username already taken. Choose another one.", user=session.get("user"))

            return render_template("register.html", error=str(e), user=session.get("user"))

    return render_template("register.html", user=session.get("user"))


# -----------------------------
# Login (USERNAME + password)
# -----------------------------
@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    next_url = request.args.get("next", "/upload")

    if request.method == "POST":
        username = request.form.get("username", "").strip().lower()
        password = request.form.get("password", "").strip()

        if not username or not password:
            return render_template("login.html", error="Username and password are required.", user=session.get("user"))

        try:
            # ✅ Fetch email using username
            user_row = supabase.table("users") \
                .select("email, username") \
                .eq("username", username) \
                .single() \
                .execute()

            if not user_row.data:
                return render_template("login.html", error="Invalid username or password.", user=session.get("user"))

            email = user_row.data["email"]

            # ✅ Supabase login
            auth = supabase.auth.sign_in_with_password({"email": email, "password": password})

            if auth.user is None:
                return render_template("login.html", error="Invalid username or password.", user=session.get("user"))

            user_data = auth.user

            # ✅ Store tokens (optional)
            if auth.session:
                session["access_token"] = auth.session.access_token
                session["refresh_token"] = auth.session.refresh_token

            # ✅ Store session (include username)
            session["user"] = {
                "id": user_data.id,
                "email": user_data.email,
                "username": username
            }

            # ✅ Upsert user row (safe)
            supabase.table("users").upsert({
                "id": user_data.id,
                "email": user_data.email
            }).execute()

            return redirect(next_url)

        except Exception as e:
            return render_template("login.html", error=str(e), user=session.get("user"))

    return render_template("login.html", user=session.get("user"))


# -----------------------------
# Google Auth
# -----------------------------
@auth_bp.route("/auth/google")
def google_auth():
    next_url = request.args.get("next", "/upload")
    redirect_to = url_for("auth.google_callback", _external=True, next=next_url)

    res = supabase.auth.sign_in_with_oauth({
        "provider": "google",
        "options": {"redirect_to": redirect_to}
    })
    return redirect(res.url)


@auth_bp.route("/auth/callback")
def google_callback():
    code = request.args.get("code")
    next_url = request.args.get("next", "/upload")

    if not code:
        return redirect(url_for("auth.login"))

    auth = supabase.auth.exchange_code_for_session({"auth_code": code})
    user_data = auth.user

    # ✅ Upsert base user row
    supabase.table("users").upsert({
        "id": user_data.id,
        "email": user_data.email
    }).execute()

    # ✅ Get username from DB
    db_user = supabase.table("users").select("username").eq("id", user_data.id).single().execute()
    username = db_user.data.get("username") if db_user.data else None

    session["user"] = {
        "id": user_data.id,
        "email": user_data.email,
        "username": username
    }

    # ✅ Redirect to complete profile if missing fields
    if not is_profile_complete(user_data.id):
        return redirect(url_for("auth.complete_profile"))

    return redirect(next_url)


# -----------------------------
# Complete Profile (Google users mostly)
# -----------------------------
@auth_bp.route("/complete-profile", methods=["GET", "POST"])
@login_required
def complete_profile():
    user_id = session["user"]["id"]

    if request.method == "POST":
        username = request.form.get("username", "").strip().lower()
        first_name = request.form.get("first_name", "").strip()
        last_name = request.form.get("last_name", "").strip()
        phone_no = request.form.get("phone_no", "").strip()

        if not all([username, first_name, last_name, phone_no]):
            return render_template("complete_profile.html", error="All fields are required.", user=session.get("user"))

        if " " in username or len(username) < 3:
            return render_template("complete_profile.html", error="Username must be at least 3 characters and contain no spaces.", user=session.get("user"))

        # ✅ Ensure username unique
        existing_username = supabase.table("users").select("id").eq("username", username).execute()
        if existing_username.data:
            return render_template("complete_profile.html", error="Username already taken. Choose another.", user=session.get("user"))

        supabase.table("users").update({
            "username": username,
            "first_name": first_name,
            "last_name": last_name,
            "phone_no": phone_no
        }).eq("id", user_id).execute()

        # ✅ Update session username for navbar
        session["user"]["username"] = username

        return redirect(url_for("pdf.upload_pdf"))

    return render_template("complete_profile.html", user=session.get("user"))


# -----------------------------
# Forgot Password
# -----------------------------
@auth_bp.route("/forgot-password", methods=["GET", "POST"])
def forgot_password():
    if request.method == "POST":
        email = request.form.get("email", "").strip()

        if not email:
            return render_template("forgot_password.html", error="Email is required.", user=session.get("user"))

        try:
            supabase.auth.reset_password_email(email)
            return render_template("forgot_password.html", success="✅ Password reset email sent! Check your inbox.", user=session.get("user"))
        except Exception as e:
            return render_template("forgot_password.html", error=str(e), user=session.get("user"))

    return render_template("forgot_password.html", user=session.get("user"))


# -----------------------------
# Profile Page (Change Username)
# -----------------------------
@auth_bp.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    user_id = session["user"]["id"]

    # ✅ Fetch current user data
    res = supabase.table("users") \
        .select("username, first_name, last_name, phone_no, email") \
        .eq("id", user_id) \
        .single() \
        .execute()

    user_db = res.data if res.data else {}

    if request.method == "POST":
        new_username = request.form.get("username", "").strip().lower()

        if not new_username:
            return render_template("profile.html", user=session.get("user"), user_db=user_db, error="Username is required.")

        if " " in new_username or len(new_username) < 3:
            return render_template("profile.html", user=session.get("user"), user_db=user_db, error="Username must be at least 3 characters and contain no spaces.")

        if user_db.get("username") == new_username:
            return render_template("profile.html", user=session.get("user"), user_db=user_db, success="✅ Username is already updated.")

        # ✅ Check username unique
        existing = supabase.table("users").select("id").eq("username", new_username).execute()
        if existing.data:
            return render_template("profile.html", user=session.get("user"), user_db=user_db, error="Username already taken. Choose another.")

        # ✅ Update DB
        supabase.table("users").update({
            "username": new_username
        }).eq("id", user_id).execute()

        # ✅ Update session
        session["user"]["username"] = new_username

        user_db["username"] = new_username

        return render_template("profile.html", user=session.get("user"), user_db=user_db, success="✅ Username updated successfully.")

    return render_template("profile.html", user=session.get("user"), user_db=user_db)
