import os
from dotenv import load_dotenv

load_dotenv()

from app import create_app, db

app = create_app()


if __name__ == "__main__":
    flask_env = os.getenv("FLASK_ENV", "production")
    debug_mode = os.getenv("FLASK_DEBUG", "False").lower() in ("1", "true", "yes")
    if flask_env != "production":
        with app.app_context():
            db.create_all()
    app.run(debug=debug_mode)


