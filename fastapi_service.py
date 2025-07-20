# fastapi_service.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import joblib
import numpy as np

# Load trained model
model = joblib.load("smartslip_model.pkl")

app = FastAPI(title="SmartSlip Win Probability API")

class MatchOdds(BaseModel):
    home_odds: float
    draw_odds: float
    away_odds: float

class SlipRequest(BaseModel):
    matches: List[MatchOdds]

@app.post("/predict")
def predict_win_probability(slip: SlipRequest):
    try:
        features = []
        for m in slip.matches:
            avg = (m.home_odds + m.draw_odds + m.away_odds) / 3
            features.append([m.home_odds, m.draw_odds, m.away_odds, avg])

        X = np.array(features)
        probs = model.predict_proba(X)[:, 1]  # probability of "win"

        # Aggregate logic: higher match count = lower compound chance
        # Simple approximation: multiply single match chances
        overall_prob = np.prod(probs)
        return {"win_probability": round(overall_prob * 100, 2)}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Simulated API endpoints for frontend UI
@app.get("/api/sports")
def get_sports():
    return {
        "sports": [
            {"id": "soccer", "name": "Football"},
            {"id": "basketball", "name": "Basketball"},
            {"id": "tennis", "name": "Tennis"}
        ]
    }

@app.get("/api/leagues/{sport_id}")
def get_leagues(sport_id: str):
    league_data = {
        "soccer": [
            {"id": "premier_league", "name": "Premier League"},
            {"id": "super_lig", "name": "Süper Lig"}
        ],
        "basketball": [
            {"id": "nba", "name": "NBA"},
            {"id": "euroleague", "name": "EuroLeague"}
        ],
        "tennis": [
            {"id": "atp", "name": "ATP Tour"},
            {"id": "wta", "name": "WTA Tour"}
        ]
    }
    return {"leagues": league_data.get(sport_id, [])}

@app.get("/api/markets/{sport_id}")
def get_markets(sport_id: str):
    market_data = {
        "soccer": [
            {"id": "h2h", "name": "Match Result (1X2)"},
            {"id": "over_under", "name": "Over/Under"},
            {"id": "btts", "name": "Both Teams to Score"}
        ],
        "basketball": [
            {"id": "h2h", "name": "Match Winner"},
            {"id": "spread", "name": "Spread"}
        ],
        "tennis": [
            {"id": "h2h", "name": "Match Winner"},
            {"id": "set_betting", "name": "Set Betting"}
        ]
    }
    return {"markets": market_data.get(sport_id, [])}
