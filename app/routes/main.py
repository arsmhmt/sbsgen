
from flask import Blueprint, render_template
from datetime import datetime

main_bp = Blueprint("main", __name__)

@main_bp.route("/")
def index():
    return render_template("main/index.html", year=datetime.now().year)

@main_bp.route("/pricing")
def pricing():
    return render_template("main/pricing.html")

@main_bp.route("/features")
def features():
    return render_template("main/features.html")

@main_bp.route("/terms")
def terms():
    return render_template("terms.html")

@main_bp.route("/privacy")
def privacy():
    return render_template("privacy.html")
