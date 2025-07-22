import os
from app import create_app, db
from app.models import User, UserRole
from werkzeug.security import generate_password_hash

ADMIN_EMAIL = os.getenv("ADMIN_EMAIL")
ADMIN_USERNAME = os.getenv("ADMIN_USERNAME")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")

app = create_app()

with app.app_context():
    # Ensure superadmin role exists
    superadmin_role = UserRole.query.filter_by(name="superadmin").first()
    if not superadmin_role:
        superadmin_role = UserRole(name="superadmin", description="Super Administrator")
        db.session.add(superadmin_role)
        db.session.commit()
        print("Created 'superadmin' role.")
    else:
        print("'superadmin' role already exists.")

    # Ensure admin user exists
    user = User.query.filter_by(email=ADMIN_EMAIL).first()
    if not user:
        user = User(
            email=ADMIN_EMAIL,
            username=ADMIN_USERNAME,
            password_hash=generate_password_hash(ADMIN_PASSWORD),
            role=superadmin_role
        )
        db.session.add(user)
        db.session.commit()
        print(f"Created superadmin user: {ADMIN_EMAIL}")
    else:
        user.username = ADMIN_USERNAME
        user.password_hash = generate_password_hash(ADMIN_PASSWORD)
        user.role = superadmin_role
        db.session.commit()
        print(f"Updated superadmin user: {ADMIN_EMAIL}")

print("Done.")
