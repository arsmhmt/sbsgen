from fastapi import APIRouter
from app.services.api_football import fetch_available_sports

router = APIRouter()

@router.get("/")
async def get_available_sports():
    return {"sports": fetch_available_sports()}
