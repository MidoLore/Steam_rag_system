import json
import random
import time

import requests
from bs4 import BeautifulSoup

def load_app_ids(filename="../data/steam_app_tags_missing.json"):
    with open(filename, "r", encoding="utf-8") as f:
        return json.load(f)

def scrape_steam_tags(app_id, current_index, total_games):

    if len(app_id[2]) > 0:
        return {
        'app_id': app_id[0],
        'name': app_id[1],
        'tags': app_id[2]
    }
    else:
        url = f"https://store.steampowered.com/app/{app_id[0]}/{app_id[1]}/"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }

        time.sleep(random.uniform(1, 3))

        try:
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')

            game_data = {
                'app_id': app_id[0],
                'name': app_id[1],
                'tags': []
            }

            for tag in soup.find_all('a', attrs={'class': 'app_tag'}):
                text = tag.text.strip()
                game_data['tags'].append(text)

            tag_count = len(game_data['tags'])
            status_symbol = "✓" if tag_count > 0 else "✗"

            # Print progress with index, symbol, game name, and tag count
            print(f"[{current_index}/{total_games}] {status_symbol} {app_id[1]} | Tags: {tag_count:2d}")

            return game_data
        except Exception as e:
            print("Timeout")

def save_app_ids(apps):
    simpleList = []

    for app in apps:
        app_id = app['appid']
        app_name = app['name']
        app_tags = app['tags']
        simpleList.append([app_id, app_name, app_tags])

    with open('steam_app_tags_web.json', 'w', encoding="utf-8") as f:
        json.dump(simpleList, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    app_ids = load_app_ids()
    game_data = []
    index = 1

    for app in app_ids:
        game_data.append(scrape_steam_tags(app, index, len(app_ids)))
        index += 1

    save_app_ids(game_data)