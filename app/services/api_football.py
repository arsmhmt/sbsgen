import os
import httpx
from typing import List, Dict, Optional
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_FOOTBALL_KEY")
BASE_URL = "https://v3.football.api-sports.io"
HEADERS = {"x-apisports-key": API_KEY}


def fetch_available_sports() -> List[Dict]:
    url = f"{BASE_URL}/sports"
    try:
        response = httpx.get(url, headers=HEADERS)
        response.raise_for_status()
        return response.json().get("response", [])
    except Exception as e:
        print("[ERROR] fetch_available_sports:", e)
        return []


def fetch_leagues() -> List[Dict]:
    url = f"{BASE_URL}/leagues"
    try:
        response = httpx.get(url, headers=HEADERS)
        response.raise_for_status()
        return response.json().get("response", [])
    except Exception as e:
        print("[ERROR] fetch_leagues:", e)
        return []


def fetch_fixtures(league_id: int, season: int = 2024) -> List[Dict]:
    url = f"{BASE_URL}/fixtures"
    try:
        response = httpx.get(url, headers=HEADERS, params={"league": league_id, "season": season})
        response.raise_for_status()
        return response.json().get("response", [])
    except Exception as e:
        print(f"[ERROR] fetch_fixtures for league {league_id}:", e)
        return []
