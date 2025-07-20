

from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from app.utils.auth_utils import get_db
from app.utils.i18n import get_text

router = APIRouter()
templates = Jinja2Templates(directory="templates")
templates.env.globals['get_text'] = get_text


@router.get("/", response_class=HTMLResponse)
async def dashboard(request: Request):
    lang = request.cookies.get('lang') or request.query_params.get('lang') or 'en'
    return templates.TemplateResponse("dashboard.html", {"request": request, "lang": lang})

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
    lang = request.cookies.get('lang') or request.query_params.get('lang') or 'en'
    return templates.TemplateResponse("pricing.html", {"request": request, "lang": lang})
