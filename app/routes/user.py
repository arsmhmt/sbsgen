
from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_user, login_required, current_user
from app.models import User, Ad
from passlib.hash import bcrypt
from app.forms import LoginForm

user_bp = Blueprint("user", __name__)

# --- User Login Route ---
@user_bp.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            if hasattr(user, 'password_hash') and user.password_hash:
                if bcrypt.verify(form.password.data, user.password_hash):
                    login_user(user)
                    return redirect(url_for("user.dashboard"))
                else:
                    flash("Incorrect password. Please try again.", "danger")
            else:
                flash("This account was created with Google. Please use 'Sign in with Google'.", "warning")
        else:
            flash("No account found with that email.", "danger")
    return render_template("user/login.html", form=form)


@user_bp.route("/dashboard")
@login_required
def dashboard():
    ads = Ad.query.order_by(Ad.display_order).all()
    return render_template("user/dashboard.html", user=current_user, ads=ads)

# Add account route to match sidebar link
@user_bp.route("/account")
@login_required
def account():
    return render_template("user/account.html", user=current_user)

# Add betslips route to match sidebar link
@user_bp.route("/betslips")
@login_required
def betslips():
    return render_template("user/betslips.html", user=current_user)


# Add referrals route to match sidebar link
@user_bp.route("/referrals")
@login_required
def referrals():
    return render_template("user/referrals.html", user=current_user)

# Add edit_profile route to match account.html link
@user_bp.route("/edit_profile", methods=["GET", "POST"])
@login_required
def edit_profile():
    # TODO: Implement profile editing logic and form
    return render_template("user/edit_profile.html", user=current_user)

# Add change_password route to match account.html link
@user_bp.route("/change_password", methods=["GET", "POST"])
@login_required
def change_password():
    # TODO: Implement password change logic and form
    return render_template("user/change_password.html", user=current_user)
