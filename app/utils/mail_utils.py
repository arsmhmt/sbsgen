from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from pydantic import EmailStr
from dotenv import load_dotenv
import os

# Load environment variables from mail.env
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '../../mail.env'))

conf = ConnectionConfig(
    MAIL_USERNAME = os.getenv('MAIL_USERNAME'),
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD'),
    MAIL_FROM = os.getenv('MAIL_DEFAULT_SENDER'),
    MAIL_PORT = int(os.getenv('MAIL_PORT', 587)),
    MAIL_SERVER = os.getenv('MAIL_SERVER'),
    MAIL_STARTTLS = os.getenv('MAIL_STARTTLS', 'True') == 'True',
    MAIL_SSL_TLS = os.getenv('MAIL_SSL_TLS', 'False') == 'True',
    USE_CREDENTIALS = True,
    VALIDATE_CERTS = True
)

fast_mail = FastMail(conf)

def send_verification_email(email: EmailStr, subject: str, body: str):
    message = MessageSchema(
        subject=subject,
        recipients=[email],
        body=body,
        subtype="html"
    )
    return fast_mail.send_message(message)
