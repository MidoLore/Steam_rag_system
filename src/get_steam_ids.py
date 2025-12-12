import time
import requests
import json

path = ''
with open("../", "r") as f:
    STEAM_API_KEY = f.read().strip()
    f.close()

"Get all Steam game IDs"
def get_app_list():
    all_apps = []
    last_appid = 0

    while True:
        try:
            url = "https://api.steampowered.com/IStoreService/GetAppList/v1/"
            params = {
                'key': STEAM_API_KEY,
                'include_games': True,
                'include_dlc': False,  # Skip DLC
                'include_software': False,  # Skip software
                'include_videos': False,  # Skip videos
                'max_results': 50000, # Max per request
                'last_appid': last_appid  # For pagination
            }

            response = requests.get(url, params=params, timeout=30)
            steam_data = response.json()
            apps = steam_data.get('response', {}).get('apps', [])

            all_apps.extend(apps)
            last_appid = apps[-1]['appid']

            print(f"Fetched {len(apps)} apps. Total: {len(all_apps)}")
            print(f"Last app ID in this batch: {apps[-1]['name']}")

            if len(apps) < 50000:
                break
            else:
                time.sleep(2)
        except requests.exceptions.RequestException as err:
            print(f"Error fetching data:{err}")

    return all_apps

def save_app_ids(apps):
    simpleList = []

    for app in apps:
        app_id = app['appid']
        app_name = app['name']
        simpleList.append([app_id, app_name])

    with open('steam_app_ids.json', 'w', encoding="utf-8") as f:
        json.dump(simpleList, f, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    all_apps = get_app_list()
    save_app_ids(all_apps)

