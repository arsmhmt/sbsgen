from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
from app.services.api_football import fetch_fixtures

import random
from ai.predictor import predict_win_probability

router = APIRouter()

class BetslipRequest(BaseModel):
    league_ids: List[int]
    min_odd: float
    max_odd: float
    num_matches: int

@router.post("/")
async def generate_betslip(data: BetslipRequest):
    all_matches = []
    
    for league_id in data.league_ids:
        fixtures = fetch_fixtures(league_id)
        for match in fixtures:
            # Dummy odds for now — placeholder (we’ll get real odds later)
            match["odds"] = round(random.uniform(1.3, 3.5), 2)
            if data.min_odd <= match["odds"] <= data.max_odd:
                all_matches.append(match)

    if len(all_matches) < data.num_matches:
        raise HTTPException(status_code=400, detail="Not enough matches in the given range.")

    selected = random.sample(all_matches, data.num_matches)

    total_odds = round(sum([m["odds"] for m in selected]), 2)
    win_probability = predict_win_probability([m["odds"] for m in selected])

    return {
        "slip": selected,
        "total_odds": total_odds,
        "win_probability": win_probability
    }
    