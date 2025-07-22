
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from app.models import User
from app import db
from werkzeug.security import generate_password_hash, check_password_hash

auth_bp = Blueprint("auth", __name__)

# --- Forgot Password Route ---
@auth_bp.route("/forgot_password", methods=["GET", "POST"])
def forgot_password():
    if request.method == "POST":
        email = request.form["email"]
        user = User.query.filter_by(email=email).first()
        if user:
            # TODO: Send password reset email
            flash("If this email is registered, a password reset link has been sent.", "info")
        else:
            flash("If this email is registered, a password reset link has been sent.", "info")
        return redirect(url_for("auth.login"))
    return render_template("auth/forgot_password.html")

from app.forms import SignupForm

@auth_bp.route("/signup", methods=["GET", "POST"])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        email = form.email.data
        username = form.username.data
        password = form.password.data
        role = form.role.data or "user"
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash("Email already registered.", "danger")
            return redirect(url_for("auth.signup"))

        hashed_password = generate_password_hash(password)
        new_user = User(email=email, username=username, password=hashed_password, role=role)
        db.session.add(new_user)
        db.session.commit()
        flash("Signup successful. Please log in.", "success")
        return redirect(url_for("auth.login"))
    return render_template("user/signup.html", form=form)

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for("user.dashboard"))
        flash("Invalid credentials.", "danger")
    return render_template("auth/login.html")


# --- Google Login (User Only) ---
from flask_dance.contrib.google import google
from flask import session

@auth_bp.route("/login/google/authorized")
def google_authorized():
    if not google.authorized:
        flash("Google login failed or was cancelled.", "danger")
        return redirect(url_for("auth.login"))
    resp = google.get("/oauth2/v2/userinfo")
    if not resp.ok:
        flash("Failed to fetch user info from Google.", "danger")
        return redirect(url_for("auth.login"))
    info = resp.json()
    email = info.get("email")
    username = info.get("name") or email.split("@")[0]
    user = User.query.filter_by(email=email).first()
    if not user:
        user = User(email=email, username=username, password="", role="user", oauth_provider="google")
        db.session.add(user)
        db.session.commit()
    login_user(user)
    flash("Logged in with Google!", "success")
    return redirect(url_for("user.dashboard"))


# --- Logout Route ---
@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Logged out successfully.", "info")
    return redirect(url_for("auth.login"))



# --- Email Verification Route ---
import os
from itsdangerous import URLSafeTimedSerializer

@auth_bp.route("/verify_email/<token>")
def verify_email(token):
    s = URLSafeTimedSerializer(os.getenv('SECRET_KEY', 'devkey'))
    try:
        email = s.loads(token, max_age=3600)
    except Exception:
        flash("Invalid or expired token.", "danger")
        return redirect(url_for("auth.login"))
    user = User.query.filter_by(email=email).first()
    if user:
        user.email_verified = True
        db.session.commit()
        flash("Email verified!", "success")
    else:
        flash("User not found.", "danger")
    return redirect(url_for("auth.login"))
