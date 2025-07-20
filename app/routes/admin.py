


from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.utils.auth_utils import get_current_user, get_db
from app.models import User

router = APIRouter(prefix="/admin120724", tags=["admin"])

def admin_required(user=Depends(get_current_user)):
    if not getattr(user, "is_admin", False):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin access required.")
    return user

# Show number of users
@router.get("/users_count")
def users_count(db: Session = Depends(get_db), user=Depends(admin_required)):
    count = db.query(User).count()
    return {"users_count": count}

# Show number of slips per day
@router.get("/slips_per_day")
def slips_per_day(db: Session = Depends(get_db), user=Depends(admin_required)):
    # Placeholder: Replace with actual query
    count = db.execute("SELECT COUNT(*) FROM betslips WHERE DATE(created_at) = CURRENT_DATE").scalar()
    return {"slips_today": count}

# Show popular leagues/sports
@router.get("/popular_leagues")
def popular_leagues(db: Session = Depends(get_db), user=Depends(admin_required)):
    # Placeholder: Replace with actual query
    leagues = ["Premier League", "La Liga", "Bundesliga"]
    return {"popular_leagues": leagues}

# Show ad clicks
@router.get("/ad_clicks")
def ad_clicks(db: Session = Depends(get_db), user=Depends(admin_required)):
    # Placeholder: Replace with actual query
    clicks = 123
    return {"ad_clicks": clicks}

# Toggle ads on/off by user
@router.post("/toggle_ads/{user_id}")
def toggle_ads(user_id: int, db: Session = Depends(get_db), user=Depends(admin_required)):
    target_user = db.query(User).filter_by(id=user_id).first()
    if not target_user:
        raise HTTPException(status_code=404, detail="User not found")
    target_user.ads_enabled = not getattr(target_user, "ads_enabled", True)
    db.commit()
    return {"user_id": user_id, "ads_enabled": target_user.ads_enabled}

# Promote user to admin
@router.post("/promote/{user_id}")
def promote_user(user_id: int, db: Session = Depends(get_db), user=Depends(admin_required)):
    target_user = db.query(User).filter_by(id=user_id).first()
    if not target_user:
        raise HTTPException(status_code=404, detail="User not found")
    target_user.is_admin = True
    db.commit()
    return {"user_id": user_id, "is_admin": True}
