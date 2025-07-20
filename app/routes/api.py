from app.models.betslip import Betslip
from app.models.betslip import Betslip
from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.models import User
from datetime import datetime
from ai.predictor import generate_betslip as ai_generate_betslip
from app.utils.usage_guard import check_credits
from app.routes.api import get_current_user, get_db

router = APIRouter()

@router.post("/api/betslip")
async def generate_betslip(req: Request, db: Session = Depends(get_db)):
    user: User = get_current_user(req)
    await check_credits(user)

    # Example: get betslip input from request JSON
    data = await req.json()
    betslip_input = data.get("betslip_input")
    if not betslip_input:
        raise HTTPException(status_code=400, detail="Missing betslip input")

    # Generate betslip using AI predictor (replace with your actual logic)
    # Should return selected_matches, total_odds, win_prob
    result = ai_generate_betslip(betslip_input)
    selected_matches = result.get("matches")
    total_odds = result.get("total_odds")
    win_prob = result.get("win_probability")

    # Save new betslip
    new_slip = Betslip(
        user_id=user.id,
        total_odds=total_odds,
        win_probability=win_prob,
        matches=selected_matches
    )
    db.add(new_slip)
    # Update user usage
    user.credits_used += 1
    user.last_used = datetime.utcnow()
    db.commit()
    db.refresh(new_slip)

    return JSONResponse(content={
        "success": True,
        "slip_id": new_slip.id,
        "total_odds": total_odds,
        "win_probability": win_prob,
        "matches": selected_matches
    })

@router.get("/api/credit-info")
def get_credit_info(req: Request, db: Session = Depends(get_db)):
    user: User = get_current_user(req)
    today = datetime.utcnow().date()

    if user.last_used is None or user.last_used.date() != today:
        user.credits_used = 0
        db.commit()

    return {
        "pro": user.is_pro,
        "remaining": "∞" if user.is_pro else user.daily_credits - user.credits_used
    }

@router.get("/api/recent-betslips")
def get_recent_betslips(req: Request, db: Session = Depends(get_db)):
    user = get_current_user(req)
    slips = db.query(Betslip).filter_by(user_id=user.id).order_by(Betslip.created_at.desc()).limit(5).all()
    return [
        {
            "id": s.id,
            "created_at": s.created_at.isoformat(),
            "total_odds": s.total_odds,
            "win_probability": s.win_probability,
            "match_count": len(s.matches)
        } for s in slips
    ]