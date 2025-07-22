import os
from app import create_app, db
from app.models import User, UserRole

ADMIN_EMAIL = os.getenv("ADMIN_EMAIL")

app = create_app()

with app.app_context():
    user = User.query.filter_by(email=ADMIN_EMAIL).first()
    if not user:
        print(f"No user found with email: {ADMIN_EMAIL}")
    else:
        print(f"User: {user.email}")
        print(f"Username: {user.username}")
        print(f"Role: {user.role.name if user.role else 'None'} (role_id: {user.role_id})")
        print(f"Password hash: {user.password_hash[:20]}...")
        print(f"Is authenticated: {user.is_authenticated}")
        print(f"User ID: {user.id}")
    role = UserRole.query.filter_by(name="superadmin").first()
    if not role:
        print("No 'superadmin' role found.")
    else:
        print(f"Superadmin role exists. ID: {role.id}")
