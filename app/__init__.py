import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_dance.contrib.google import google
from dotenv import load_dotenv
from flask_migrate import Migrate # Import Flask-Migrate
from flask_wtf import CSRFProtect

load_dotenv()

# --- UPDATED DEBUG PRINTS ---
client_id_val = os.getenv('GOOGLE_CLIENT_ID')
client_secret_val = os.getenv('GOOGLE_CLIENT_SECRET')
oauthlib_insecure_val = os.getenv('OAUTHLIB_INSECURE_TRANSPORT')

print(f"DEBUG: GOOGLE_CLIENT_ID from .env: '{client_id_val}' (Type: {type(client_id_val)})")
print(f"DEBUG: GOOGLE_CLIENT_SECRET from .env: '{client_secret_val}' (Type: {type(client_secret_val)}, Length: {len(client_secret_val) if client_secret_val else 'None'})")
print(f"DEBUG: OAUTHLIB_INSECURE_TRANSPORT from .env: '{oauthlib_insecure_val}' (Type: {type(oauthlib_insecure_val)})")
# --- END DEBUG PRINTS ---

db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate() # Instantiate Flask-Migrate

def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY=os.getenv("FLASK_SECRET_KEY", "dev"),
        SQLALCHEMY_DATABASE_URI=os.getenv("DATABASE_URL"),
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
    )

    # Ensure instance folder exists
    try:
        os.makedirs(app.instance_path, exist_ok=True)
    except OSError:
        pass

    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)
    login_manager.login_view = 'auth.login'
    CSRFProtect(app)

    # FastAPI migration: Remove Flask Blueprint imports and registration
    # TODO: Replace with FastAPI router includes in main.py

    # Create DB tables (for development) - Commented out as migrations will handle this
    # with app.app_context():
    #     db.create_all()

    return app

@login_manager.user_loader
def load_user(user_id):
    from app.models import User
    return User.query.get(int(user_id))

