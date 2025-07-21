


from flask import Blueprint, render_template, redirect, url_for, flash, request, abort
from flask_login import login_required, current_user
from app.models import User, Betslip, AuditLog
from app import db

admin_bp = Blueprint("admin", __name__)

def admin_required():
    if not current_user.is_authenticated or not getattr(current_user, "is_admin", False):
        abort(403)

# Show number of users and dashboard
@admin_bp.route("/dashboard")
@login_required
def admin_dashboard():
    admin_required()
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
@admin_bp.route("/promote/<int:user_id>", methods=["POST"])
@login_required
def promote_user(user_id):
    admin_required()
    target_user = User.query.filter_by(id=user_id).first()
    if not target_user:
        return {"error": "User not found"}, 404
    target_user.is_admin = True
    db.session.commit()
    return {"user_id": user_id, "is_admin": True}
