from flask_login import UserMixin
from app import db

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    name = db.Column(db.String(150))
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    is_admin = db.Column(db.Boolean, default=False)


    # Relationship: referrals
    referrals = db.relationship('Referral', backref='user', lazy='dynamic')

    # Relationship: betslips
    betslips = db.relationship('Betslip', back_populates='user', lazy='dynamic')

    def __repr__(self):
        return f"<User {self.email}>"
