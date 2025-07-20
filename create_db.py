
from dotenv import load_dotenv
load_dotenv()
from app import create_app, db

app = create_app()
with app.app_context():
    db.create_all()
    print("✅ Database & tables created at", app.config["SQLALCHEMY_DATABASE_URI"])
