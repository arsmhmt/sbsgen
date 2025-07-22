
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, login_required, current_user
from app.models import User, Ad
from app import db
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


from app.forms import BetslipForm

@user_bp.route("/dashboard")
@login_required
def dashboard():
    ads = Ad.query.order_by(Ad.display_order).all()
    form = BetslipForm()
    # Example: populate choices dynamically (replace with DB/API as needed)
    form.league.choices = [("epl", "English Premier League"), ("laliga", "La Liga"), ("seriea", "Serie A")]
    form.market.choices = [("1x2", "1X2"), ("over_under", "Over/Under"), ("btts", "Both Teams To Score")]
    return render_template("user/dashboard.html", user=current_user, ads=ads, form=form)

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


# Add generate_betslip route to handle betslip generation from dashboard
@user_bp.route("/generate_betslip", methods=["POST"])
@login_required
def generate_betslip():
    # TODO: Implement actual betslip generation logic
    # For now, just flash a message and redirect back to dashboard
    flash("Betslip generation is not yet implemented.", "info")
    return redirect(url_for("user.dashboard"))


# Add referrals route to match sidebar link
@user_bp.route("/referrals")
@login_required
def referrals():
    return render_template("user/referrals.html", user=current_user)

# Add edit_profile route to match account.html link (merged GET/POST)
@user_bp.route("/edit_profile", methods=["GET", "POST"])
@login_required
def edit_profile():
    if request.method == "POST":
        username = request.form.get("username")
        if username and username != current_user.username:
            if User.query.filter_by(username=username).first():
                flash("Username already taken.", "danger")
            else:
                current_user.username = username
                db.session.commit()
                flash("Username updated!", "success")
        return redirect(url_for("user.account"))
    return render_template("user/edit_profile.html", user=current_user)

# Add change_password route to match account.html link
@user_bp.route("/change_password", methods=["GET", "POST"])
@login_required
def change_password():
    # TODO: Implement password change logic and form
    return render_template("user/change_password.html", user=current_user)
