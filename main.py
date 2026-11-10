from datetime import date
import os
import requests
from dotenv import load_dotenv

# Read the API key from .env
load_dotenv()
api_key = os.getenv("BALLDONTLIE_API_KEY")

# NBA API address
url = "https://api.balldontlie.io/v1/games"

# Authentication
headers = {
    "Authorization": api_key
}

# Choose which day's games to retrieve
user_date = input("Enter a date (YYYY-MM-DD), or press Enter for today: ")

if user_date == "":
    selected_date = date.today().isoformat()
else:
    selected_date = user_date

params = {
    "dates[]": selected_date
}

# Ask the API for game data
if not api_key:
    raise ValueError("API key is missing from .env")

response = requests.get(
    url,
    headers=headers,
    params=params,
    timeout=30
)

response.raise_for_status()

# Convert the response into a Python dictionary
data = response.json()

# Get the list of games
games = data["data"]

if len(games) == 0:
    print("No NBA games found on this date.")

print("🏀 Welcome to PulseScore!")
print("---------------------------")

for game in games:
    home_team = game["home_team"]["full_name"]
    away_team = game["visitor_team"]["full_name"]

    home_score = game["home_team_score"]
    away_score = game["visitor_team_score"]

    print(f"{away_team} vs {home_team}")
    print(f"Score: {away_score} - {home_score}")
    print(f"Status: {game['status']}")
    print("---------------------------")

