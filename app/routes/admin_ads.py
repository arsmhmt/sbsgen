


from fastapi import APIRouter, Depends, Request, Form, HTTPException, status
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from app.utils.auth_utils import get_current_user, get_db
from app.models import Ad

router = APIRouter(prefix="/admin/ads", tags=["admin_ads"])
templates = Jinja2Templates(directory="templates")

def admin_required(user=Depends(get_current_user)):
    if not getattr(user, "is_admin", False):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin access required.")
    return user


# List ads
@router.get("/")
def list_ads(request: Request, db: Session = Depends(get_db), user=Depends(admin_required)):
    ads = db.query(Ad).order_by(Ad.slot_type, Ad.display_order).all()
    return templates.TemplateResponse("admin/ads.html", {"request": request, "ads": ads})

# Create ad (GET: form, POST: submit)
@router.get("/create")
def create_ad_form(request: Request, user=Depends(admin_required)):
    return templates.TemplateResponse("admin/ad_form.html", {"request": request, "ad": None})

@router.post("/create")
def create_ad(
    request: Request,
    slot_type: str = Form(...),
    image_url: str = Form(...),
    link_url: str = Form(...),
    display_order: int = Form(...),
    is_active: bool = Form(False),
    db: Session = Depends(get_db),
    user=Depends(admin_required)
):
    ad = Ad(
        slot_type=slot_type,
        image_url=image_url,
        link_url=link_url,
        display_order=display_order,
        is_active=is_active
    )
    db.add(ad); db.commit()
    return RedirectResponse("/admin/ads/", status_code=status.HTTP_303_SEE_OTHER)

# Edit ad
@router.get("/{ad_id}/edit")
def edit_ad_form(ad_id: int, request: Request, db: Session = Depends(get_db), user=Depends(admin_required)):
    ad = db.query(Ad).filter_by(id=ad_id).first()
    if not ad:
        raise HTTPException(status_code=404, detail="Ad not found")
    return templates.TemplateResponse("admin/ad_form.html", {"request": request, "ad": ad})

@router.post("/{ad_id}/edit")
def edit_ad(
    ad_id: int,
    request: Request,
    slot_type: str = Form(...),
    image_url: str = Form(...),
    link_url: str = Form(...),
    display_order: int = Form(...),
    is_active: bool = Form(False),
    db: Session = Depends(get_db),
    user=Depends(admin_required)
):
    ad = db.query(Ad).filter_by(id=ad_id).first()
    if not ad:
        raise HTTPException(status_code=404, detail="Ad not found")
    ad.slot_type = slot_type
    ad.image_url = image_url
    ad.link_url = link_url
    ad.display_order = display_order
    ad.is_active = is_active
    db.commit()
    return RedirectResponse("/admin/ads/", status_code=status.HTTP_303_SEE_OTHER)

# Delete ad
@router.post("/{ad_id}/delete")
def delete_ad(ad_id: int, db: Session = Depends(get_db), user=Depends(admin_required)):
    ad = db.query(Ad).filter_by(id=ad_id).first()
    if not ad:
        raise HTTPException(status_code=404, detail="Ad not found")
    db.delete(ad); db.commit()
    return RedirectResponse("/admin/ads/", status_code=status.HTTP_303_SEE_OTHER)

# Track ad impression
@router.post("/impression/{ad_id}")
def track_impression(ad_id: int, db: Session = Depends(get_db)):
    ad = db.query(Ad).filter_by(id=ad_id).first()
    if not ad:
        raise HTTPException(status_code=404, detail="Ad not found")
    ad.impressions = getattr(ad, "impressions", 0) + 1
    db.commit()
    return {"ad_id": ad_id, "impressions": ad.impressions}

# Show ad statistics (impressions/clicks)
@router.get("/stats/{ad_id}")
def ad_stats(ad_id: int, db: Session = Depends(get_db), user=Depends(admin_required)):
    ad = db.query(Ad).filter_by(id=ad_id).first()
    if not ad:
        raise HTTPException(status_code=404, detail="Ad not found")
    return {
        "ad_id": ad_id,
        "impressions": getattr(ad, "impressions", 0),
        "clicks": getattr(ad, "clicks", 0),
        "preview": ad.image_url
    }
