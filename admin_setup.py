# admin_setup.py
"""
Run this script once after migrations to create the admin role and admin user from your .env file.
"""
import os
from app import create_app, db
from app.models import User
from app.models.user_roles import UserRole
from werkzeug.security import generate_password_hash

app = create_app()

ADMIN_EMAIL = os.getenv("ADMIN_EMAIL")
ADMIN_USERNAME = os.getenv("ADMIN_USERNAME")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")

with app.app_context():
    # Create admin role if it doesn't exist
    admin_role = UserRole.query.filter_by(name="admin").first()
    if not admin_role:
        admin_role = UserRole(name="admin", description="Administrator role")
        db.session.add(admin_role)
        db.session.commit()
        print("Created admin role.")
    else:
        print("Admin role already exists.")

    # Create admin user if it doesn't exist
    admin_user = User.query.filter_by(email=ADMIN_EMAIL).first()
    if not admin_user:
        admin_user = User(
            email=ADMIN_EMAIL,
            username=ADMIN_USERNAME,
            password_hash=generate_password_hash(ADMIN_PASSWORD),
            role=admin_role,
            email_verified=True
        )
        db.session.add(admin_user)
        db.session.commit()
        print(f"Created admin user: {ADMIN_EMAIL}")
    else:
        print("Admin user already exists.")
