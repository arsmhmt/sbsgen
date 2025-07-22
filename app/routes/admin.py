from flask import Blueprint, render_template, redirect, url_for, flash, request, abort
from flask_login import login_user, logout_user, login_required, current_user
from app.models import User, Betslip, AuditLog

from app import db
from app.forms import AdminLoginForm
from werkzeug.security import check_password_hash

admin_bp = Blueprint("admin", __name__, url_prefix="/admin120724")



from functools import wraps
from flask import flash
def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not current_user.is_authenticated:
            flash("Access denied.", "danger")
            return redirect(url_for("admin.admin_login"))
        # Ensure role is loaded and check name
        role_name = None
        if hasattr(current_user, "role") and current_user.role:
            role_name = getattr(current_user.role, "name", None)
        if role_name not in ["admin", "superadmin"]:
            flash("Access denied.", "danger")
            return redirect(url_for("admin.admin_login"))
        return f(*args, **kwargs)
    return decorated

# List all betslips (Admin feature, paginated)
@admin_bp.route("/betslips")
@login_required
@admin_required
def betslips():
    page = request.args.get("page", 1, type=int)
    per_page = 20
    betslips = Betslip.query.order_by(Betslip.created_at.desc()).paginate(page=page, per_page=per_page, error_out=False)
    return render_template("admin/betslips.html", betslips=betslips)

# Set user to pro (upgrade user)
@admin_bp.route("/set_pro/<int:user_id>", methods=["POST"])
@login_required
@admin_required
def set_pro_user(user_id):
    target_user = User.query.filter_by(id=user_id).first()
    if not target_user:
        return {"error": "User not found"}, 404
    from app.models.user_roles import UserRole
    pro_role = UserRole.query.filter_by(name="pro").first()
    if not pro_role:
        return {"error": "Pro role not found"}, 404
    target_user.role = pro_role
    db.session.commit()
    return redirect(url_for("admin.users"))

# List all users (Admin feature)
@admin_bp.route("/users")
@login_required
@admin_required
def users():
    users = User.query.order_by(User.created_at.desc()).all()
    return render_template("admin/users.html", users=users)

# Show number of users and dashboard
@admin_bp.route("/dashboard")
@login_required
@admin_required
def admin_dashboard():
    stats = {
        "total_users": User.query.count(),
        "paid_users": User.query.join(User.role).filter_by(name="pro").count() if hasattr(User, 'role') else 0,
        "total_slips": Betslip.query.count(),
        "revenue": 0.0  # Replace with actual revenue logic if available
    }
    recent_slips = Betslip.query.order_by(Betslip.created_at.desc()).limit(10).all()
    logs = AuditLog.query.order_by(AuditLog.timestamp.desc()).limit(20).all()
    return render_template("admin/dashboard.html", stats=stats, recent_slips=recent_slips, logs=logs)


# Promote user to admin (JSON)

@admin_bp.route("/login", methods=["GET", "POST"])
def admin_login():
    form = AdminLoginForm()
    if current_user.is_authenticated:
        # Check if user has admin or superadmin role
        role_name = None
        if hasattr(current_user, "role") and current_user.role:
            role_name = getattr(current_user.role, "name", None)
        if role_name in ["admin", "superadmin"]:
            return redirect(url_for("admin.admin_dashboard"))
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        from app.models.user_roles import UserRole
        # Accept both 'admin' and 'superadmin' roles
        admin_roles = UserRole.query.filter(UserRole.name.in_(["admin", "superadmin"]))
        user = User.query.filter_by(email=email).filter(User.role_id.in_([r.id for r in admin_roles])).first() if admin_roles else None
        if user and hasattr(user, 'password_hash') and check_password_hash(user.password_hash, password):
            login_user(user)
            return redirect(url_for("admin.admin_dashboard"))
        else:
            flash("Invalid admin credentials.", "danger")
            return redirect(url_for("admin.admin_login"))
    return render_template("admin/login.html", form=form)

@admin_bp.route("/logout")
@login_required
@admin_required
def admin_logout():
    logout_user()
    flash("Admin logged out.", "info")
    return redirect(url_for("admin.admin_login"))

@admin_bp.route("/promote/<int:user_id>", methods=["POST"])
@login_required
@admin_required
def promote_user(user_id):
    target_user = User.query.filter_by(id=user_id).first()
    if not target_user:
        return {"error": "User not found"}, 404
    target_user.role = "admin"
    db.session.commit()
    return {"user_id": user_id, "is_admin": True}

# Placeholder payments route to resolve BuildError
@admin_bp.route("/payments")
@login_required
@admin_required
def payments():
    # You can create a template 'admin/payments.html' or just return a placeholder for now
    return render_template("admin/payments.html")
