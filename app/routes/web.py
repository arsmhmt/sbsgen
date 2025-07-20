
from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from app.utils.auth_utils import get_db

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/", response_class=HTMLResponse)
async def dashboard(request: Request):
    return templates.TemplateResponse("dashboard.html", {"request": request})

# Ad click tracking endpoint
@router.post("/click/ad/{ad_id}")
def click_ad(ad_id: int, db: Session = Depends(get_db)):
    # Placeholder: increment click count for ad
    # ad = db.query(Ad).filter_by(id=ad_id).first()
    # if ad:
    #     ad.clicks += 1
    #     db.commit()
    return {"ad_id": ad_id, "clicked": True}

# Pricing page
@router.get("/pricing", response_class=HTMLResponse)
async def pricing(request: Request):
    return templates.TemplateResponse("pricing.html", {"request": request})
