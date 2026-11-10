
import os
from datetime import date, datetime

import requests
from dotenv import load_dotenv
from flask import Flask, render_template, request

load_dotenv()

app = Flask(__name__)

API_URL = "https://api.balldontlie.io/v1/games"


def get_games(selected_date):
    """Get NBA games for a selected date."""

    api_key = os.getenv("BALLDONTLIE_API_KEY")

    if not api_key:
        raise ValueError("Missing API key in .env")

    response = requests.get(
        API_URL,
        headers={"Authorization": api_key},
        params={
            "dates[]": selected_date,
            "per_page": 100
        },
        timeout=15
    )

    response.raise_for_status()
    return response.json()["data"]


@app.route("/")
def home():
    selected_date = request.args.get(
        "date", date.today().isoformat()
    )

    games = []
    error = None

    try:
        datetime.strptime(selected_date, "%Y-%m-%d")
        games = get_games(selected_date)

    except ValueError:
        error = "Please enter a valid date or check your API key."

    except requests.exceptions.RequestException:
        error = "Could not load games. Try again later."

    return render_template(
        "index.html",
        games=games,
        selected_date=selected_date,
        error=error
    )


if __name__ == "__main__":
    app.run(debug=True)
