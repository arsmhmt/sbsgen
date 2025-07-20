import os
from flask import Blueprint, flash, redirect, url_for, request, render_template
from flask_login import login_user, logout_user, login_required
from flask_dance.consumer import oauth_authorized
from flask_dance.contrib.google import make_google_blueprint, google
from app import db # Assuming db is initialized in __init__.py
from app.models import User
from app.forms import SignupForm # Assuming SignupForm is in app.forms
from passlib.hash import bcrypt # Assuming passlib is installed for bcrypt

# --- Initialize Blueprint for Auth Routes ---
auth_bp = Blueprint("auth", __name__)

# --- Forgot Password Route ---
@auth_bp.route("/forgot_password", methods=["GET", "POST"])
def forgot_password():
    return render_template("auth/forgot_password.html")

# --- Reset Password Route ---
@auth_bp.route("/reset_password", methods=["GET", "POST"])
def reset_password():
    return render_template("auth/reset_password.html")

# --- Configure Google OAuth via Flask-Dance ---
print("→ GOOGLE_CLIENT_ID (from auth.py):", os.getenv("GOOGLE_CLIENT_ID"))
print("→ GOOGLE_CLIENT_SECRET (from auth.py):", os.getenv("GOOGLE_CLIENT_SECRET"))
google_bp = make_google_blueprint(
    client_id=os.getenv("GOOGLE_CLIENT_ID"),
    client_secret=os.getenv("GOOGLE_CLIENT_SECRET"),
    scope=[
        "openid",
        "https://www.googleapis.com/auth/userinfo.email",
        "https://www.googleapis.com/auth/userinfo.profile"
    ],
    redirect_url="/user/"
)

# --- Register Google Blueprint with auth_bp ---
auth_bp.register_blueprint(google_bp, url_prefix="/login")

# --- Signal handler for Google OAuth success ---
@oauth_authorized.connect_via(google_bp)
def google_logged_in(blueprint, token):
    if not token:
        flash("Google login failed.", "danger")
        return False

    resp = blueprint.session.get("/oauth2/v2/userinfo")
    if not resp.ok:
        flash("Could not fetch your Google profile. Status: %s" % resp.status_code, "danger")
        return False

    info = resp.json()
    email = info["email"]
    name = info.get("name", email.split("@")[0])

    user = User.query.filter_by(email=email).first()
    if not user:
        user = User(email=email, name=name)
        db.session.add(user)
        db.session.commit()

    login_user(user)
    flash("Logged in as “%s”." % user.email, "success")
    return redirect(url_for("user.dashboard"))

# --- Signup Route ---
@auth_bp.route("/signup", methods=["GET", "POST"])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        if User.query.filter_by(email=form.email.data).first():
            flash("Email already registered.", "warning")
            return redirect(url_for("auth.signup"))

        hashed = bcrypt.hash(form.password.data)
        user = User(email=form.email.data, name=form.username.data, password_hash=hashed)
        db.session.add(user)
        db.session.commit()

        flash("Account created! Please log in.", "success")
        return redirect(url_for("user.login"))
    return render_template("auth/signup.html", form=form)

# --- Logout Route ---
@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You’ve been logged out.", "info")
    return redirect(url_for("auth.login"))

# --- Login Route (Redirects to Google OAuth) ---
@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    form = SignupForm()  # Replace with your actual LoginForm if you have one
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.verify(form.password.data, user.password_hash):
            login_user(user)
            return redirect(url_for("user.dashboard"))
        else:
            flash("Invalid email or password.", "danger")
    return render_template("auth/login.html", form=form)
