from datetime import datetime
from app import db
from flask_login import UserMixin


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email       = db.Column(db.String(120), unique=True, nullable=False)
    # Add the name column here
    name        = db.Column(db.String(100), nullable=True) # Added name column
    password_hash = db.Column(db.String(255), nullable=True) # Made nullable for OAuth users
    is_pro      = db.Column(db.Boolean, default=False)
    is_admin    = db.Column(db.Boolean, default=False)

    free_slip_credits = db.Column(db.Integer, default=3)
    betslips = db.relationship('Betslip', backref='user', lazy='dynamic')

    def check_password(self, pw):
        from passlib.hash import bcrypt
        # Ensure password_hash exists before trying to verify
        if self.password_hash:
            return bcrypt.verify(pw, self.password_hash)
        return False # No password hash means no password set (e.g., OAuth user)

class Ad(db.Model):
    __tablename__ = 'ads'
    id = db.Column(db.Integer, primary_key=True)
    image_url   = db.Column(db.String(255), nullable=False)
    target_url  = db.Column(db.String(255), nullable=True)
    position    = db.Column(db.String(50), nullable=False)  # e.g. 'banner', 'sidebar'
    is_active   = db.Column(db.Boolean, default=True)
    created_at  = db.Column(db.DateTime, default=datetime.utcnow)
    display_order = db.Column(db.Integer, default=0)

class Betslip(db.Model):
    id          = db.Column(db.Integer, primary_key=True)
    user_id     = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    data        = db.Column(db.JSON, nullable=False)  # store selected matches & odds
    result      = db.Column(db.Float)  # win % after AI calculation
    created_at  = db.Column(db.DateTime, default=datetime.utcnow)
    status      = db.Column(db.String(32), nullable=False, default='pending')
    # ... etc. ...
