import os
from flask import Blueprint, render_template, redirect, url_for, flash, request, session
from flask_login import login_user, logout_user, login_required, current_user
auth_bp = Blueprint("auth", __name__)

# --- Forgot Password Route ---
@auth_bp.route("/forgot_password")
def forgot_password():
    return render_template("auth/forgot_password.html")

# --- Reset Password Route ---
@auth_bp.route("/reset_password")
def reset_password():
    return render_template("auth/reset_password.html")

# --- Signup Route ---
@auth_bp.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        email = request.form.get("email")
        username = request.form.get("username")
        password = request.form.get("password")
        role = request.form.get("role", "user")
        if User.query.filter_by(email=email).first():
            flash("Email already registered.", "danger")
            return redirect(url_for("auth.signup"))
        if User.query.filter_by(username=username).first():
            flash("Username already taken.", "danger")
            return redirect(url_for("auth.signup"))
        hashed = bcrypt.hash(password)
        user = User(email=email, username=username, name=username, password_hash=hashed, email_verified=False)
        db.session.add(user)
        db.session.commit()
        # TODO: Send verification email here
        flash("Account created! Please log in.", "success")
        return redirect(url_for("auth.login"))
    return render_template("auth/signup.html")

# --- Login Route ---
from app.forms import LoginForm

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        user = User.query.filter_by(email=email).first()
        if user and hasattr(user, 'password_hash') and bcrypt.verify(password, user.password_hash):
            login_user(user)
            return redirect(url_for("user.dashboard"))
        else:
            flash("Invalid credentials.", "danger")
            return redirect(url_for("auth.login"))
    return render_template("auth/login.html", form=form)

# --- Logout Route ---
@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Logged out.", "info")
    return redirect(url_for("auth.login"))


# --- Email Verification Route ---
from itsdangerous import URLSafeTimedSerializer
from app.models import User
from app import db
from passlib.hash import bcrypt

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
