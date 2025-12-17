import random
import time
import requests
import json

store_url = "https://store.steampowered.com/api/appdetails"

def load_app_ids(filename="../../data/steam_app_tags_combined.json"):
    with open(filename, "r", encoding="utf-8") as f:
        return json.load(f)

def fetch_game(app_id):
    params = {
        'appids': app_id,
        'l' : 'english'
    }

    try:
        time.sleep(random.uniform(1, 3))
        response = requests.get(store_url, params=params)
        data = response.json()

        game_data = data.get(str(app_id))

        return game_data['data']

    except requests.exceptions.RequestException as e:
        print(f"Error fetching game {app_ids}: {e}")

def save_app_ids(apps):
    simpleList = []

    for app in apps:
        app_id = app['app_id']
        app_name = app['name']
        app_tags = app['tags']
        simpleList.append([app_id, app_name, app_tags])

    with open('../../data/steam_app_tags_web.json', 'w', encoding="utf-8") as f:
        json.dump(simpleList, f, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    app_ids = load_app_ids()
    app = fetch_game(app_ids[43][0])
    print(app)