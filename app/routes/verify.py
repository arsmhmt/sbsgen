from fastapi import APIRouter, Request, HTTPException, Depends
from sqlalchemy.orm import Session
from app.utils.token_utils import verify_token
from app.models import User
from app.routes.api import get_db
from app.utils.audit_log import log_verification_attempt
from app.utils.i18n import get_text

router = APIRouter()

@router.get("/verify")
async def verify_email(token: str, db: Session = Depends(get_db), req: Request = None):
    lang = req.headers.get('Accept-Language', 'en')[:2] if req else 'en'
    try:
        payload = verify_token(token)
        user_id = payload["user_id"]
        user = db.query(User).filter_by(id=user_id).first()
        if not user:
            log_verification_attempt('unknown', False, 'User not found')
            return {"success": False, "message": get_text('verification_failed', lang)}
        if user.email_verified:
            log_verification_attempt(user.email, True, 'Already verified')
            return {"success": True, "message": get_text('already_verified', lang)}
        user.email_verified = True
        db.commit()
        log_verification_attempt(user.email, True)
        return {"success": True, "message": get_text('verification_success', lang)}
    except Exception as e:
        log_verification_attempt('unknown', False, str(e))
        return {"success": False, "message": get_text('verification_failed', lang)}
