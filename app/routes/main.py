from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def index():
    return {"message": "Welcome to SmartSlip!"}

@router.get("/pricing")
async def pricing():
    return {"message": "Pricing page"}

@router.get("/terms")
async def terms():
    return {"message": "Terms page"}

@router.get("/privacy")
async def privacy():
    return {"message": "Privacy page"}
