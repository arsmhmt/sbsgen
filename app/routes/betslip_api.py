
from fastapi import APIRouter, Depends, Request, HTTPException, status
from fastapi.responses import RedirectResponse, JSONResponse
import requests
import os
from app.services.api_football import fetch_fixtures  # your service stub
import random  # remove once you have real odds
from app.utils.auth_utils import get_current_user, get_db
from sqlalchemy.orm import Session

router = APIRouter(prefix="/api", tags=["betslip"])

@router.get("/betslip-analytics")
def betslip_analytics(db: Session = Depends(get_db), user=Depends(get_current_user)):
    from datetime import datetime, timedelta
    today = datetime.utcnow().date()
    dates = [(today - timedelta(days=i)) for i in range(29, -1, -1)]
    date_labels = [d.strftime('%d %b') for d in dates]
    success_ratios = []
    Betslip = db.__class__.models['Betslip'] if hasattr(db.__class__, 'models') and 'Betslip' in db.__class__.models else None
    if not Betslip:
        from app.models.betslip import Betslip
    for d in dates:
        slips = db.query(Betslip).filter(
            Betslip.user_id == user.id,
            Betslip.created_at >= datetime.combine(d, datetime.min.time()),
            Betslip.created_at < datetime.combine(d + timedelta(days=1), datetime.min.time())
        ).all()
        total = len(slips)
        won = sum(1 for s in slips if s.status == 'won')
        ratio = (won / total * 100) if total > 0 else 0
        success_ratios.append(round(ratio, 1))
    all_slips = db.query(Betslip).filter(Betslip.user_id == user.id).all()
    total_all = len(all_slips)
    won_all = sum(1 for s in all_slips if s.status == 'won')
    user_win_pct = round(won_all / total_all * 100, 1) if total_all > 0 else None
    return {
        "dates": date_labels,
        "success_ratios": success_ratios,
        "user_win_pct": user_win_pct
    }

from fastapi import APIRouter, Depends, Request, HTTPException, status
from fastapi.responses import RedirectResponse
from fastapi.responses import JSONResponse
import requests
import os
from app.services.api_football import fetch_fixtures  # your service stub
import random  # remove once you have real odds
from app.utils.auth_utils import get_current_user, get_db
from sqlalchemy.orm import Session

router = APIRouter(prefix="/api", tags=["betslip"])
@router.get("/lang/{lang_code}")
def set_language(lang_code: str, request: Request):
    # Store language in session (FastAPI workaround: use cookies)
    if lang_code not in ["en", "tr"]:
        raise HTTPException(status_code=400, detail="Invalid language code")
    response = RedirectResponse(url="/", status_code=303)
    response.set_cookie(key="lang", value=lang_code, max_age=60*60*24*30)
    return response
API_URL = "https://v3.football.api-sports.io"
API_KEY = os.getenv("API_FOOTBALL_KEY")
HEADERS = {"x-apisports-key": API_KEY}



@router.get("/sports")
def get_sports():
    res = requests.get(f"{API_URL}/sports", headers=HEADERS)
    return res.json().get("response", [])


@router.get("/leagues")
def get_leagues():
    res = requests.get(f"{API_URL}/leagues", headers=HEADERS)
    return res.json().get("response", [])


@router.get("/markets")
def get_markets():
    # Static for now or from odds endpoint later
    return ["1X2", "Over/Under", "BTTS", "Double Chance"]


def get_user_quota(user):
    # Example: user.role, user.slip_count_today
    if getattr(user, "role", None) == "pro":
        return None  # Unlimited
    return 3  # Free users: 3 slips/day

@router.post("/betslip")
def generate_betslip(
    request: Request,
    league_ids: list = None,
    min_odd: float = 1.01,
    max_odd: float = 100.0,
    num_matches: int = 5,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    # Freemium control
    quota = get_user_quota(user)
    slip_count_today = getattr(user, "slip_count_today", 0)
    quota_reached = quota is not None and slip_count_today >= quota
    if quota_reached:
        return JSONResponse({
            "error": "Free quota reached. Upgrade to Pro for unlimited slips.",
            "quota_reached": True
        }, status_code=status.HTTP_429_TOO_MANY_REQUESTS)

    # 1) Fetch fixtures for each league
    fixtures = []
    for lid in league_ids or []:
        fixtures.extend(fetch_fixtures(int(lid)))

    # 2) Pick top fixtures by simulated “best odd” in range
    slip = []
    total = 1.0
    for fx in fixtures:
        if len(slip) >= num_matches:
            break
        # STUB: generate a random odd in range
        odd = round(random.uniform(min_odd, max_odd), 2)
        slip.append({
            "home_team": fx["teams"]["home"]["name"],
            "away_team": fx["teams"]["away"]["name"],
            "best_odd": {"market": "h2h", "value": odd}
        })
        total *= odd

    # 3) Call FastAPI AI microservice
    ai_payload = {
        "matches": [
            {"home_odds": m["best_odd"]["value"],
             "draw_odds": m["best_odd"]["value"] * 0.5,
             "away_odds": m["best_odd"]["value"] * 1.5}
            for m in slip
        ]
    }
    try:
        ai_resp = requests.post(
            "http://127.0.0.1:5001/predict",
            json=ai_payload,
            timeout=5
        )
        ai_resp.raise_for_status()
        win_pct = ai_resp.json().get("win_probability")
    except Exception:
        win_pct = None

    # Update user slip count (pseudo-code, implement actual DB logic)
    if quota is not None:
        user.slip_count_today = slip_count_today + 1
        db.commit()

    return {
        "slip": slip,
        "total_odds": round(total, 2),
        "win_probability": win_pct,
        "quota_reached": False
    }
