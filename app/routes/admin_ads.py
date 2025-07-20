# app/routes/admin_ads.py
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app import db
from app.models import Ad

admin_ads = Blueprint("admin_ads", __name__, url_prefix="/admin/ads")

def admin_only(func):
    @login_required
    def wrapper(*args, **kwargs):
        if not getattr(current_user, "is_admin", False):
            flash("Access denied.", "danger")
            return redirect(url_for("user.dashboard"))
        return func(*args, **kwargs)
    wrapper.__name__ = func.__name__
    return wrapper

@admin_ads.route("/")
@admin_only
def list_ads():
    ads = Ad.query.order_by(Ad.slot_type, Ad.display_order).all()
    return render_template("admin/ads.html", ads=ads)

@admin_ads.route("/create", methods=["GET","POST"])
@admin_only
def create_ad():
    if request.method=="POST":
        ad = Ad(
            slot_type=request.form["slot_type"],
            image_url=request.form["image_url"],
            link_url=request.form["link_url"],
            display_order=int(request.form["display_order"]),
            is_active = bool(request.form.get("is_active"))
        )
        db.session.add(ad); db.session.commit()
        flash("Ad created.", "success")
        return redirect(url_for("admin_ads.list_ads"))
    return render_template("admin/ad_form.html", ad=None)

@admin_ads.route("/<int:ad_id>/edit", methods=["GET","POST"])
@admin_only
def edit_ad(ad_id):
    ad = Ad.query.get_or_404(ad_id)
    if request.method=="POST":
        ad.slot_type = request.form["slot_type"]
        ad.image_url = request.form["image_url"]
        ad.link_url  = request.form["link_url"]
        ad.display_order = int(request.form["display_order"])
        ad.is_active = bool(request.form.get("is_active"))
        db.session.commit()
        flash("Ad updated.", "success")
        return redirect(url_for("admin_ads.list_ads"))
    return render_template("admin/ad_form.html", ad=ad)

@admin_ads.route("/<int:ad_id>/delete", methods=["POST"])
@admin_only
def delete_ad(ad_id):
    ad = Ad.query.get_or_404(ad_id)
    db.session.delete(ad); db.session.commit()
    flash("Ad deleted.", "info")
    return redirect(url_for("admin_ads.list_ads"))
