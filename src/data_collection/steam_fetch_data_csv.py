import csv
import json
from collections import defaultdict

#Loads up json file containing every gameID and name
def load_app_ids(filename="../data/steam_app_ids.json"):
    with open(filename, "r", encoding="utf-8") as f:
        return json.load(f)

#LoadLoads a dataset of games (ID, name, and tags) from a December 2024 CSV
def load_tags_from_csv(filename="../data/tags.csv"):
    tags_dict = defaultdict(list)
    with open(filename, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)

        for row in reader:
            app_id = row["app_id"].strip('""')
            tags = row["tag"].strip('""')
            tags_dict[app_id].append(tags)
    return tags_dict

#Converts the csv to json
def csv_to_json(tags,app_info):
    game_data = {
        'app_id': app_info[0],
        'name': app_info[1],
        'tags': tags.get(str(app_info[0]), []),  # Get tags if exists, else empty list
    }
    return game_data

#Saves the csv converted json file as steam_app_tags_missing
def save_app_ids(apps):
    simpleList = []

    for app in apps:
        app_id = app['app_id']
        app_name = app['name']
        app_tags = app['tags']
        simpleList.append([app_id, app_name, app_tags])

    with open('../../data/raw/steam_app_tags_missing.json', 'w', encoding="utf-8") as f:
        json.dump(simpleList, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    all_apps = load_app_ids()
    all_tags = load_tags_from_csv()

    gamedata = []

    for i, app in enumerate(all_apps):
        game = csv_to_json(all_tags, app)
        gamedata.append(game)

    save_app_ids(gamedata)