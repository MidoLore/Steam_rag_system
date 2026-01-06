import random
import time
import requests
import json
import re
import html

store_url = "https://store.steampowered.com/api/appdetails"

def load_app_ids(filename="../../data/steam_app_data.json"):
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
        print(f"Error fetching game {app_id}: {e}")


def fetch_game_data(game, current_index, total_games):
    params = {
        'appids': game['app_id'],
        'l': 'english'
    }

    try:
        time.sleep(random.uniform(1, 3))
        response = requests.get(store_url, params=params, timeout=10)
        response.raise_for_status()

        app_data = response.json().get(str(game['app_id']))
        if not app_data or not app_data.get('success'):
            raise ValueError("Steam API returned success=false")

        data = app_data['data']

        if data.get('release_date', {}).get('coming_soon'):
            print(f"[{current_index}/{total_games}] ✗ {game['app_id']} {game['name']} (coming soon)")
            return None

        # ---- PRICE HANDLING ----
        if data.get('is_free'):
            price_details = {
                'price': "0.00 kr",
                'is_free': True,
                'currency': 'NOK'
            }
        else:
            price_overview = data.get('price_overview')
            if not price_overview:
                raise KeyError("price_overview missing for paid game")

            price = (
                price_overview['initial_formatted']
                if price_overview.get('discount_percent', 0) > 0
                else price_overview['final_formatted']
            )

            price_details = {
                'price': price,
                'is_free': False,
                'currency': price_overview['currency']
            }

        game_data = {
            'app_id': game['app_id'],
            'name': game['name'],
            'tags': game['tags'],
            'price_details': price_details,
            'description': re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', ' ', html.unescape(data.get('detailed_description', '')))).strip(),
            'release_date': data['release_date']['date'],
            'developers': data.get('developers', []),
            'publishers': data.get('publishers', [])
        }

        print(f"[{current_index}/{total_games}] ✓ {game['app_id']} {game['name']}")
        return game_data

    except requests.exceptions.RequestException as e:
        print(f"[{current_index}/{total_games}] ✗ {game['app_id']} {game['name']} (network error)")
        return None

    except (KeyError, TypeError, ValueError) as e:
        print(f"[{current_index}/{total_games}] ✗ {game['app_id']} {game['name']} ({e})")
        return None



def save_app_ids(apps):
    cleaned_apps = [app for app in apps if app is not None]

    with open('../../data/steam_app_data_True.json', 'w', encoding="utf-8") as f:
        json.dump(cleaned_apps, f, ensure_ascii=False, indent=2)

    print(f" Saved {len(apps)} games as dicts")

def convert_game_to_dict(game_list):
    data = []
    for game in game_list:
        if len(game) >= 3:
            data.append({
                'app_id': game[0],
                'name': game[1],
                'tags': game[2]
            })
    return data

if __name__ == "__main__":
    game_catalogue = load_app_ids()
    gameList = []
    index = 1
    save_interval = 100

    for game in game_catalogue:
        gameList.append(fetch_game_data(game, index, len(game_catalogue)))
        index += 1

        if index % save_interval == 0:
            save_app_ids(gameList)
            print(f"checkpoint saved at game {index}")

    print(gameList)


    '''
    for game in game_catalogue:
        if game['app_id'] == 2420:
            print(fetch_game_data(game, index, len(game_catalogue)))

    '''














