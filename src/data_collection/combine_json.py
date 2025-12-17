import random
import time

import requests
import json

def load_json(filename):
    with open(filename, "r", encoding="utf-8") as f:
        return json.load(f)


def combine_json(game, web_dict, spy_dict):
    app_id = game[0]
    web_game = web_dict.get(app_id)
    spy_game = spy_dict.get(app_id)

    # Check web tags
    if web_game and len(web_game[2]) > 0:
        print(f"✓ {web_game[1]} | {len(web_game[2])} tags (web)")
        return {
            'app_id': web_game[0],
            'name': web_game[1],
            'tags': web_game[2]
        }
    # Check spy tags
    elif spy_game and len(spy_game[2]) > 0:
        print(f"✓ {spy_game[1]} | {len(spy_game[2])} tags (spy)")
        return {
            'app_id': spy_game[0],
            'name': spy_game[1],
            'tags': spy_game[2]
        }
    # No tags
    else:
        print(f"✗ {game[1]} | 0 tags (SKIPPING)")
        return None

def save_json(game_data):
    simpleList = []

    for app in game_data:
        if app is None:
            continue

        app_id = app['app_id']
        app_name = app['name']
        app_tags = app['tags']
        simpleList.append([app_id, app_name, app_tags])

    with open('../../data/steam_app_tags_combined.json', 'w', encoding="utf-8") as f:
        json.dump(simpleList, f, ensure_ascii=False, indent=2)

def list_to_dict(game_list):
    game_dict = {}
    for game in game_list:
        if len(game) >= 3: 
            app_id = game[0]
            game_dict[app_id] = game
    return game_dict

if __name__ == "__main__":
    game_catalogue_combined = []
    game_catalogue_web = load_json("../../data/steam_app_tags_web.json")
    game_catalogue_spy = load_json("../../data/steam_app_tags_spy.json")

    web_dict = list_to_dict(game_catalogue_web)
    spy_dict = list_to_dict(game_catalogue_spy)

    index = 1
    for game in game_catalogue_web:
        combined = combine_json(game, web_dict, spy_dict)
        if combined:
            game_catalogue_combined.append(combined)

    print(len(game_catalogue_web))
    print(len(game_catalogue_spy))
    print(len(game_catalogue_combined))







