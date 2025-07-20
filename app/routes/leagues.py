from fastapi import APIRouter, Query
from app.services.api_football import fetch_leagues_by_sport

router = APIRouter()

@router.get("/")
async def get_leagues(sport: str = Query(..., description="Sport type (e.g., football)")):
    leagues = fetch_leagues_by_sport(sport)
    return {"leagues": leagues}
