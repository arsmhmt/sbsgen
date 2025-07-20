# Placeholder for fetch_leagues_by_sport to fix ImportError

def fetch_leagues_by_sport(sport_ids):
    """
    Accepts a single sport or a list of sports, returns merged leagues.
    """
    if isinstance(sport_ids, str):
        sport_ids = [sport_ids]
    all_leagues = []
    for sport in sport_ids:
        url = f"{BASE_URL}/leagues"
        try:
            response = httpx.get(url, headers=HEADERS, params={"sport": sport})
            response.raise_for_status()
            leagues = response.json().get("response", [])
            all_leagues.extend(leagues)
        except Exception as e:
            print(f"[ERROR] fetch_leagues_by_sport for sport {sport}:", e)
    # Optionally deduplicate by league id
    seen = set()
    merged = []
    for league in all_leagues:
        lid = league.get("league", {}).get("id")
        if lid and lid not in seen:
            merged.append(league)
            seen.add(lid)
    return merged
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
    return [{"error": True, "message": f"Failed to fetch sports: {str(e)}"}]


def fetch_leagues() -> List[Dict]:
    url = f"{BASE_URL}/leagues"
    try:
        response = httpx.get(url, headers=HEADERS)
        response.raise_for_status()
        return response.json().get("response", [])
    except Exception as e:
        print("[ERROR] fetch_leagues:", e)
        return []
    return [{"error": True, "message": f"Failed to fetch leagues: {str(e)}"}]


def fetch_fixtures(league_id: int, season: int = 2024) -> List[Dict]:
    url = f"{BASE_URL}/fixtures"
    try:
        response = httpx.get(url, headers=HEADERS, params={"league": league_id, "season": season})
        response.raise_for_status()
        return response.json().get("response", [])
    except Exception as e:
        print(f"[ERROR] fetch_fixtures for league {league_id}:", e)
        return []
    return [{"error": True, "message": f"Failed to fetch fixtures for league {league_id}: {str(e)}"}]
