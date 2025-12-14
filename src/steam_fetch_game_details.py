import time
import requests
import json

store_url = "https://store.steampowered.com/api/appdetails"

def load_app_ids(filename="../data/steam_app_ids.json"):
    with open(filename, "r", encoding="utf-8") as f:
        return json.load(f)

def fetch_game(app_id):
    params = {
        'appids': app_id,
        'l' : 'english'
    }

    try:
        response = requests.get(store_url, params=params)
        data = response.json()

        game_data = data.get(str(app_id))

        return game_data['data']

    except requests.exceptions.RequestException as e:
        print(f"Error fetching game {app_ids}: {e}")

if __name__ == "__main__":
    app_ids = load_app_ids()
    app = fetch_game(app_ids[43][0])
    print(app)