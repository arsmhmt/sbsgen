# train_model.py
import numpy as np
import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import joblib

# Sample historical odds dataset (you can replace this with your actual CSV or database)
data = [
    {"home_odds": 1.80, "draw_odds": 3.40, "away_odds": 4.20, "result": 1},  # win
    {"home_odds": 2.10, "draw_odds": 3.10, "away_odds": 3.50, "result": 0},
    {"home_odds": 1.60, "draw_odds": 4.00, "away_odds": 5.00, "result": 1},
    {"home_odds": 3.20, "draw_odds": 3.00, "away_odds": 2.30, "result": 0},
    {"home_odds": 2.50, "draw_odds": 3.20, "away_odds": 2.90, "result": 0},
    {"home_odds": 1.50, "draw_odds": 4.10, "away_odds": 6.00, "result": 1},
    {"home_odds": 2.20, "draw_odds": 3.10, "away_odds": 3.40, "result": 0},
]

df = pd.DataFrame(data)
df["avg_odds"] = (df["home_odds"] + df["draw_odds"] + df["away_odds"]) / 3

X = df[["home_odds", "draw_odds", "away_odds", "avg_odds"]]
y = df["result"]

# Train/test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train model
model = DecisionTreeClassifier()
model.fit(X_train, y_train)

# Evaluate
y_pred = model.predict(X_test)
print("Accuracy:", accuracy_score(y_test, y_pred))

# Export model
joblib.dump(model, "smartslip_model.pkl")
print("Model saved to smartslip_model.pkl")
