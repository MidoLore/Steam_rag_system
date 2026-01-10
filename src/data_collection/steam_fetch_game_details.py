import random
import sys
import time
import requests
import json
import re
import html

store_url = "https://store.steampowered.com/api/appdetails"


def fetch_game_data(game, current_index, total_games):
    params = {
        'appids': game['app_id'],
        'l': 'english'
    }

    try:
        time.sleep(random.uniform(1, 2))
        response = requests.get(store_url, params=params, timeout=10)
        response.raise_for_status()

        app_data = response.json().get(str(game['app_id']))
        if not app_data or not app_data.get('success'):
            raise ValueError("Steam API returned success=false")

        data = app_data['data']

        if data.get('release_date', {}).get('coming_soon'):
            print(f"[{current_index}/{total_games}] ✗ {game['app_id']} {game['name']} (coming soon)")
            return None

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

def retrieve_reviews(game, current_index, total_games):
    app_id = game['app_id']
    url = f"https://store.steampowered.com/appreviews/{app_id}"

    params = {
        'json': 1
    }

    try:

        response = requests.get(url, params=params)
        if response.status_code == 429:
            print(f"[{current_index}/{total_games}] ✗ {app_id} {game['name']} - TOO MANY REQUESTS (IP may be banned). Stopping script.")
            sys.exit(1)
        elif response.status_code == 403:
            print(f"[{current_index}/{total_games}] ✗ {app_id} {game['name']} - ACCESS FORBIDDEN (possible ban). Stopping script.")
            sys.exit(1)
        elif response.status_code != 200:
            print(f"[{current_index}/{total_games}] ✗ {app_id} {game['name']} - HTTP {response.status_code}")
            return None

        data = response.json()

        reviewScore = {
            'review_score_desc': data['query_summary']['review_score_desc'],
            'total_positive': data['query_summary']['total_positive'],
            'total_negative': data['query_summary']['total_negative'],
            'total_reviews': data['query_summary']['total_reviews'],
        }

        game_data = {
            'app_id': game['app_id'],
            'name': game['name'],
            'tags': game['tags'],
            'price_details': game['price_details'],
            'description': game['description'],
            'release_date': game['release_date'],
            'developers': game['developers'],
            'publishers': game['publishers'],
            'reviews': reviewScore,
        }

        print(f"[{current_index}/{total_games}] ✓ {app_id} {game['name']}")
        return game_data

    except requests.exceptions.RequestException as e:
        print(f"[{current_index}/{total_games}] ✗ {app_id} {game['name']} (network error: {e})")
        return None

    except (KeyError, TypeError, ValueError) as e:
        print(f"[{current_index}/{total_games}] ✗ {app_id} {game['name']} (data error: {e})")
        return None

def load_app_ids(filename="../../data/steam_app_data_test.json"):
    with open(filename, "r", encoding="utf-8") as f:
        return json.load(f)

def save_app_ids(apps):
    cleaned_apps = [app for app in apps if app is not None]

    with open('../../data/steam_app_data.json', 'w', encoding="utf-8") as f:
        json.dump(cleaned_apps, f, ensure_ascii=False, indent=2)

    print(f" Saved {len(apps)} games as dicts")

def load_existing_data(filename='../../data/steam_app_data.json'):
    with open(filename, "r", encoding="utf-8") as f:
        return json.load(f)

def normalize_price(game):
    price_details = game.get("price_details", {})
    price_str = price_details.get("price")

    # Handle missing price
    if not price_str:
        price_details["price"] = None
        return game

    # Handle free games
    if isinstance(price_str, str) and "free" in price_str.lower():
        price_details["price"] = 0.0
        return game

    match = re.search(r"[\d.,]+", price_str)

    if not match:
        price_details["price"] = None
        return game

    number = match.group().replace(",", ".")

    try:
        price_details["price"] = float(number)
    except ValueError:
        price_details["price"] = None

    # Save back into price_details (not game["price"])
    game["price_details"] = price_details

    return game



if __name__ == "__main__":
    game_catalogue = load_app_ids()
    gameList = load_existing_data()
    index = 0
    save_interval = 50
    START_FROM_ID = 3560

    for game in game_catalogue:
        if game['app_id'] <= START_FROM_ID:
            index += 1
            continue

        gameList.append(retrieve_reviews(game, index, len(game_catalogue)))
        index += 1

        if index % save_interval == 0:
            save_app_ids(gameList)
            print(f"checkpoint saved at game {index}")

    print(len(game_catalogue))
    print(len(gameList))

    ''' 
    
    for game in game_catalogue:
        if game['app_id'] == 2420:
            print(fetch_game_data(game, index, len(game_catalogue)))
            
    for game in game_catalogue:
        if game['app_id'] <= START_FROM_ID:
            index += 1
            continue

        gameList.append(fetch_game_data(game, index, len(game_catalogue)))
        index += 1

        if index % save_interval == 0:
            save_app_ids(gameList)
            print(f"checkpoint saved at game {index}")

    print(gameList)


    '''














