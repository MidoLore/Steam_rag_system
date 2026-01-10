import random
import time

import requests
import json

url = "https://steamspy.com/api.php?request=appdetails"

#Loads a json dataset of games (ID, name, and tags) from a December 2024 snapshot
def load_app_ids(filename="../data/steam_app_tags_missing.json"):
    with open(filename, "r", encoding="utf-8") as f:
        return json.load(f)

#Finds tags from steamspy api if it doesn't exist
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
            return {
                'app_id': app_id[0],
                'name': app_id[1],
                'tags': []
            }

def save_app_ids(apps):
    simpleList = []

    for app in apps:
        app_id = app['app_id']
        app_name = app['name']
        app_tags = app['tags']
        simpleList.append([app_id, app_name, app_tags])

    with open('../../data/raw/steam_app_tags_spy.json', 'w', encoding="utf-8") as f:
        json.dump(simpleList, f, ensure_ascii=False, indent=2)

def load_existing_data(filename="../data/steam_app_tags_spy.json"):
    with open(filename, "r", encoding="utf-8") as f:
        data = json.load(f)

    game_data = []
    for game in data:
        game_data.append({
            'app_id': game[0],
            'name': game[1],
            'tags': game[2]
        })

    return game_data

if __name__ == "__main__":
    app_ids = load_app_ids()
    game_data = load_existing_data()
    index = 1
    save_interval = 2000
    START_FROM_ID = 881980

    for app in app_ids:
        if app[0] <= START_FROM_ID:
            index += 1
            continue

        game_data.append(fetch_app_details(app, index, len(app_ids)))
        index += 1

        if index % save_interval == 0:
            save_app_ids(game_data)
            print(f"checkpoint saved at game {index}")

    save_app_ids(game_data)