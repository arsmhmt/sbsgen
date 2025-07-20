from app import db
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

class Betslip(db.Model):
    __tablename__ = "betslips"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    total_odds = db.Column(db.Float)
    win_probability = db.Column(db.Float)
    matches = db.Column(db.JSON)

    status = db.Column(db.String(32), default='pending')

    user = db.relationship("User", back_populates="betslips")
