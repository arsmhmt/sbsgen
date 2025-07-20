# Placeholder for generate_betslip to fix ImportError
def generate_betslip(betslip_input):
    # TODO: Implement actual logic
    return {
        "matches": [],
        "total_odds": 0.0,
        "win_probability": 0.0
    }
import joblib
import numpy as np
from typing import List

# Load model on import
model = joblib.load("ai/smartslip_model.pkl")

def predict_win_probability(odds: List[float]) -> float:
    # Features: average odds, total odds, match count
    avg_odds = sum(odds) / len(odds)
    total_odds = sum(odds)
    features = np.array([[avg_odds, total_odds, len(odds)]])
    
    prob = model.predict_proba(features)[0][1]  # probability of class "win"
    return round(prob * 100, 1)  # percentage
