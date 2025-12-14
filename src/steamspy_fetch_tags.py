import random
import time

import requests
import json

url = "https://steamspy.com/api.php?request=appdetails"

def load_app_ids(filename="../data/steam_app_tags_missing.json"):
    with open(filename, "r", encoding="utf-8") as f:
        return json.load(f)

def fetch_app_details(app_id, current_index, total_games):


    if len(app_id[2]) > 0:
        return {
        'app_id': app_id[0],
        'name': app_id[1],
        'tags': app_id[2]
    }
    else:
        try:
            time.sleep(random.uniform(1, 3))
            params = {
                "appid": app_id[0],
            }

            game_data = {
                'app_id': app_id[0],
                'name': app_id[1],
                'tags': []
            }
            response = requests.get(url, params=params)

            for tag in response.json()['tags']:
               game_data['tags'].append(tag)

            tag_count = len(game_data['tags'])
            status_symbol = "✓" if tag_count > 0 else "✗"

            # Print progress with index, symbol, game name, and tag count
            print(f"[{current_index}/{total_games}] {status_symbol} {app_id[1]} | Tags: {tag_count:2d}")

            return game_data


        except requests.exceptions.RequestException as e:
            print(e)

def save_app_ids(apps):
    simpleList = []

    for app in apps:
        app_id = app['appid']
        app_name = app['name']
        app_tags = app['tags']
        simpleList.append([app_id, app_name, app_tags])

    with open('steam_app_tags_spy.json', 'w', encoding="utf-8") as f:
        json.dump(simpleList, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    app_details = load_app_ids()
    gamedata = []
    index = 1

    for app in app_details:
        gamedata.append(fetch_app_details(app, index, len(app_details)))
        index = index + 1
    save_app_ids(gamedata)