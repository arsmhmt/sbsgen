from flask_login import UserMixin
from app import db

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    username = db.Column(db.String(50), unique=True, nullable=True)
    name = db.Column(db.String(150))
    email_verified = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    is_admin = db.Column(db.Boolean, default=False)
    role_id = db.Column(db.Integer, db.ForeignKey('user_role.id'), nullable=True)

    role = db.relationship('UserRole', backref='users', lazy='joined')

    # Relationship: referrals
    referrals = db.relationship('Referral', backref='user', lazy='dynamic')

    # Relationship: betslips
    betslips = db.relationship('Betslip', back_populates='user', lazy='dynamic')

    def __repr__(self):
        return f"<User {self.email}>"
