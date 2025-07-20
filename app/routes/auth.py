
import os
from fastapi import APIRouter, Depends, Request, status, Form
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from app.models import User
# from app.forms import SignupForm # FastAPI forms handled differently
from passlib.hash import bcrypt
from app.utils.auth_utils import get_db, get_current_user

router = APIRouter(prefix="/auth", tags=["auth"])
templates = Jinja2Templates(directory="templates")

# --- Forgot Password Route ---
@router.get("/forgot_password")
def forgot_password(request: Request):
    return templates.TemplateResponse("auth/forgot_password.html", {"request": request})

# --- Reset Password Route ---
@router.get("/reset_password")
def reset_password(request: Request):
    return templates.TemplateResponse("auth/reset_password.html", {"request": request})

# --- Google OAuth logic should be implemented using FastAPI and a library like Authlib or python-social-auth ---
# Placeholder for Google OAuth integration

# --- Signup Route ---
@router.get("/signup")
def signup_form(request: Request):
    return templates.TemplateResponse("auth/signup.html", {"request": request})

@router.post("/signup")
def signup(
    request: Request,
    email: str = Form(...),
    username: str = Form(...),
    password: str = Form(...),
    role: str = Form("user"),
    db: Session = Depends(get_db)
):
    # Replace with actual form validation
    if db.query(User).filter_by(email=email).first():
        # Replace with FastAPI flash/message system
        return RedirectResponse("/auth/signup", status_code=status.HTTP_303_SEE_OTHER)
    if db.query(User).filter_by(username=username).first():
        return RedirectResponse("/auth/signup", status_code=status.HTTP_303_SEE_OTHER)

    hashed = bcrypt.hash(password)
    user = User(email=email, username=username, name=username, password_hash=hashed, email_verified=False)
    db.add(user)
    db.commit()
    # TODO: Send verification email here
    return RedirectResponse("/auth/login", status_code=status.HTTP_303_SEE_OTHER)

# --- Logout Route ---
@router.get("/logout")
def logout(request: Request):
    # TODO: Implement logout logic for FastAPI
    return RedirectResponse("/auth/login", status_code=status.HTTP_303_SEE_OTHER)

# --- Login Route ---
@router.get("/login")
def login_form(request: Request):
    return templates.TemplateResponse("auth/login.html", {"request": request})

@router.post("/login")
def login(
    request: Request,
    email: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter_by(email=email).first()
    if user and bcrypt.verify(password, user.password_hash):
        # TODO: Implement session logic for FastAPI
        return RedirectResponse("/user/dashboard", status_code=status.HTTP_303_SEE_OTHER)
    else:
        # TODO: Add error message handling
        return RedirectResponse("/auth/login", status_code=status.HTTP_303_SEE_OTHER)

# --- Email Verification Route ---
@router.get("/verify_email/{token}")
def verify_email(token: str, db: Session = Depends(get_db)):
    from itsdangerous import URLSafeTimedSerializer
    s = URLSafeTimedSerializer(os.getenv('SECRET_KEY', 'devkey'))
    try:
        email = s.loads(token, max_age=3600)
    except Exception:
        # TODO: Add error message handling
        return RedirectResponse("/auth/login", status_code=status.HTTP_303_SEE_OTHER)
    user = db.query(User).filter_by(email=email).first()
    if user:
        user.email_verified = True
        db.commit()
        # TODO: Add success message handling
    else:
        # TODO: Add error message handling
        pass
    return RedirectResponse("/auth/login", status_code=status.HTTP_303_SEE_OTHER)
