from fastapi import APIRouter, Query
from app.services.api_football import fetch_leagues_by_sport

router = APIRouter()


@router.get("/")
async def get_leagues(sport: str = Query(..., description="Comma-separated sport types (e.g., football,basketball)")):
    sport_list = [s.strip() for s in sport.split(",") if s.strip()]
    leagues = fetch_leagues_by_sport(sport_list)
    return {"leagues": leagues}
