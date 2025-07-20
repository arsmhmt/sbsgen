import pickle
import numpy as np
from typing import List

# Load model on import
with open("ai/smartslip_model.pkl", "rb") as f:
    model = pickle.load(f)

def predict_win_probability(odds: List[float]) -> float:
    # Features: average odds, total odds, match count
    avg_odds = sum(odds) / len(odds)
    total_odds = sum(odds)
    features = np.array([[avg_odds, total_odds, len(odds)]])
    
    prob = model.predict_proba(features)[0][1]  # probability of class "win"
    return round(prob * 100, 1)  # percentage
