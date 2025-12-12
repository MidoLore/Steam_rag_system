import json
import time

import requests
from bs4 import BeautifulSoup

def load_app_ids(filename="../data/steam_app_ids.json"):
    with open(filename, "r", encoding="utf-8") as f:
        return json.load(f)

def scrape_steam_tags(app_id, delay=4):
    url = f"https://store.steampowered.com/app/{app_id[0]}/{app_id[1]}/"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }

    time.sleep(delay)

    try:
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')

        game_data = {
            'app_id': app_id[0],
            'name' : app_id[1],
            'tags' : []
        }

        for tag in soup.find_all('a', attrs={'class': 'app_tag'}):
            text = tag.text.strip()
            game_data['tags'].append(text)

        return game_data
    except Exception as e:
        print("Timeout")


if __name__ == "__main__":

    app_ids = load_app_ids()
    app_id = app_ids[0]

    for i in range(10):
        game_data = scrape_steam_tags(app_ids[i])
        print(game_data)