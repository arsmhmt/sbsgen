
from flask import Blueprint, render_template
from flask_login import login_required, current_user

admin_bp = Blueprint('admin', __name__, url_prefix='/admin120724')

@admin_bp.route('/betslips')
@login_required
def betslips():
    if not current_user.is_admin:
        return render_template('errors/403.html'), 403
    return render_template('admin/betslips.html')

@admin_bp.route('/dashboard')
@login_required
def dashboard():
    if not current_user.is_admin:
        return render_template('errors/403.html'), 403
    return render_template('admin/dashboard.html')

@admin_bp.route('/users')
@login_required
def users():
    if not current_user.is_admin:
        return render_template('errors/403.html'), 403
    return render_template('admin/users.html')

@admin_bp.route('/payments')
@login_required
def payments():
    if not current_user.is_admin:
        return render_template('errors/403.html'), 403
    return render_template('admin/payments.html')

@admin_bp.route('/payment_errors')
@login_required
def payment_errors():
    if not current_user.is_admin:
        return render_template('errors/403.html'), 403
    return render_template('admin/payment_errors.html')

@admin_bp.route('/ads')
@login_required
def ads():
    if not current_user.is_admin:
        return render_template('errors/403.html'), 403
    return render_template('admin/ads.html')
