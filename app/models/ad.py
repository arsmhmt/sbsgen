# app/models/ad.py
from app import db
from datetime import datetime

class Ad(db.Model):
    __tablename__ = "ads"

    id = db.Column(db.Integer, primary_key=True)
    slot_type = db.Column(db.String(50), nullable=False)  # e.g. "banner", "sidebar_top", "sidebar_mid", "sidebar_bot"
    image_url = db.Column(db.String(500), nullable=False)
    link_url = db.Column(db.String(500), nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    display_order = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
