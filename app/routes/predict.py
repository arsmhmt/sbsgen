from fastapi import APIRouter, Request
from pydantic import BaseModel
from typing import List
from ai.predictor import predict_win_probability

router = APIRouter(prefix="/api", tags=["predict"])

class PredictRequest(BaseModel):
    home_odds: List[float]
    draw_odds: List[float]
    away_odds: List[float]

@router.post("/predict")
def predict(request: PredictRequest):
    # Combine odds for each match
    odds = []
    for h, d, a in zip(request.home_odds, request.draw_odds, request.away_odds):
        odds.append((h + d + a) / 3)
    win_prob = predict_win_probability(odds)
    return {"win_probability": win_prob}
