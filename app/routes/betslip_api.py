
from flask import Blueprint, request, jsonify
from flask_login import login_required
import requests
import os
from app.services.api_football import fetch_fixtures  # your service stub
import random  # remove once you have real odds

betslip_api = Blueprint("betslip_api", __name__)

API_URL = "https://v3.football.api-sports.io"
API_KEY = os.getenv("API_FOOTBALL_KEY")
HEADERS = {"x-apisports-key": API_KEY}


@betslip_api.route("/api/sports")
def get_sports():
    res = requests.get(f"{API_URL}/sports", headers=HEADERS)
    return jsonify(res.json().get("response", []))

@betslip_api.route("/api/leagues")
def get_leagues():
    res = requests.get(f"{API_URL}/leagues", headers=HEADERS)
    return jsonify(res.json().get("response", []))

@betslip_api.route("/api/markets")
def get_markets():
    # Static for now or from odds endpoint later
    return jsonify(["1X2", "Over/Under", "BTTS", "Double Chance"])

@betslip_api.route("/api/betslip", methods=["POST"])
@login_required
def generate_betslip():
    body = request.get_json() or {}
    league_ids   = body.get("league_ids", [])
    min_odd      = float(body.get("min_odd", 1.01))
    max_odd      = float(body.get("max_odd", 100.0))
    match_count  = int(body.get("num_matches", 5))

    # 1) Fetch fixtures for each league
    fixtures = []
    for lid in league_ids:
        fixtures.extend(fetch_fixtures(int(lid)))

    # 2) Pick top fixtures by simulated “best odd” in range
    slip = []
    total = 1.0
    for fx in fixtures:
        if len(slip) >= match_count:
            break
        # STUB: generate a random odd in range
        odd = round(random.uniform(min_odd, max_odd), 2)
        slip.append({
            "home_team": fx["teams"]["home"]["name"],
            "away_team": fx["teams"]["away"]["name"],
            "best_odd": {"market": "h2h", "value": odd}
        })
        total *= odd

    # 3) Call FastAPI AI microservice
    ai_payload = {
        "matches": [
            {"home_odds": m["best_odd"]["value"],
             "draw_odds": m["best_odd"]["value"] * 0.5,
             "away_odds": m["best_odd"]["value"] * 1.5}
            for m in slip
        ]
    }
    try:
        ai_resp = requests.post(
            "http://127.0.0.1:5001/predict",
            json=ai_payload,
            timeout=5
        )
        ai_resp.raise_for_status()
        win_pct = ai_resp.json().get("win_probability")
    except Exception:
        win_pct = None

    return jsonify({
        "slip": slip,
        "total_odds": round(total, 2),
        "win_probability": win_pct
    })
