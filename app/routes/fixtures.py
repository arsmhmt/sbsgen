from fastapi import APIRouter, Query
from app.services.api_football import fetch_fixtures

router = APIRouter()

@router.get("/")
async def get_fixtures(league_id: int = Query(..., description="League ID (from API-Football)")):
    fixtures = fetch_fixtures(league_id)
    return {"fixtures": fixtures}
