from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.models import User
from app.utils.mail_utils import send_verification_email
from app.utils.rate_limit import check_rate_limit
from app.utils.token_utils import generate_verification_token
from app.utils.auth_utils import get_current_user, get_db
from app.utils.audit_log import log_email_send
from app.utils.i18n import get_text

router = APIRouter()

@router.post("/api/send-verification-email")
async def send_verification(req: Request, db: Session = Depends(get_db)):
    check_rate_limit(req)
    user: User = get_current_user(req)
    lang = req.headers.get('Accept-Language', 'en')[:2]
    if not user:
        log_email_send('unknown', False, 'Unauthorized')
        raise HTTPException(status_code=401, detail=get_text('email_error', lang))
    data = await req.json()
    email = data.get("email", user.email)
    subject = get_text('verify_subject', lang)
    token = generate_verification_token(user)
    verify_url = f"https://smartbetslip.com/verify?token={token}"  # Use HTTPS in production
    body = f"<h3>{get_text('verify_body', lang)}</h3>"
    body += f'<a href="{verify_url}">Verify Email</a>'
    try:
        await send_verification_email(email, subject, body)
        log_email_send(email, True)
        return JSONResponse(content={"success": True, "message": get_text('email_sent', lang)})
    except Exception as e:
        log_email_send(email, False, str(e))
        return JSONResponse(content={"success": False, "message": get_text('email_error', lang)}, status_code=500)
