from flask import Flask, render_template, jsonify, request
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

STEAM_API_KEY = 'YOUR_STEAM_API_KEY_HERE'
DEFAULT_STEAM_ID = 'YOUR_STEAM_ID_HERE' 
DEFAULT_APP_ID = '12210'

def fetch_global_from_api(app_id):
    try:
        url = (
            f"https://api.steampowered.com/ISteamUserStats/"
            f"GetGlobalAchievementPercentagesForApp/v0002/"
            f"?gameid={app_id}"
        )
        data = requests.get(url).json()
        achievements = data.get('achievementpercentages', {}).get('achievements', [])

        global_map = {a['name']: float(a['percent']) for a in achievements}
        print(f"[API] Global stats loaded: {len(global_map)}")

        return global_map
    except Exception as e:
        print("[API] Global stats error:", e)
        return {}


def fetch_global_from_scrape(app_id):
    try:
        url = f"https://steamcommunity.com/stats/{app_id}/achievements"
        html = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}).text
        soup = BeautifulSoup(html, "html.parser")

        global_map = {}

        blocks = soup.select(".achieveRow")

        for block in blocks:
            title = block.select_one(".achieveTxt h3")
            percent = block.select_one(".achievePercent")

            if title and percent:
                name = title.text.strip()
                pct = percent.text.strip().replace('%', '')

                try:
                    global_map[name] = float(pct)
                except:
                    pass

        print(f"[SCRAPER] Global stats loaded: {len(global_map)}")

        return global_map
    except Exception as e:
        print("[SCRAPER] Error:", e)
        return {}


def fetch_steam_data(app_id, steam_id):
    try:
        player_url = (
            f"https://api.steampowered.com/ISteamUserStats/"
            f"GetPlayerAchievements/v0001/"
            f"?appid={app_id}&key={STEAM_API_KEY}&steamid={steam_id}"
        )
        player_res = requests.get(player_url).json()

        if 'playerstats' not in player_res:
            print("No player stats")
            return []

        player_achievements = player_res['playerstats']['achievements']
        print(f"SUCCESS: Found {len(player_achievements)} achievements")

        schema_map = {}
        try:
            schema_url = (
                f"https://api.steampowered.com/ISteamUserStats/GetSchemaForGame/v2/"
                f"?key={STEAM_API_KEY}&appid={app_id}&l=english"
            )
            schema = requests.get(schema_url).json()

            if 'game' in schema and 'availableGameStats' in schema['game']:
                for item in schema['game']['availableGameStats']['achievements']:
                    schema_map[item['name']] = {
                        'title': item.get('displayName', item['name']),
                        'desc': item.get('description', '')
                    }

            print(f"Schema loaded: {len(schema_map)}")

        except Exception as e:
            print("Schema error:", e)

        global_map = fetch_global_from_api(app_id)

        # If API empty → scrape page
        if len(global_map) == 0:
            print("API empty, switching to scraper...")
            global_map = fetch_global_from_scrape(app_id)

        processed = []

        for ach in player_achievements:
            api_name = ach['apiname']
            schema = schema_map.get(api_name, {})

            title = schema.get('title', api_name)

            rarity = (
                global_map.get(api_name)
                or global_map.get(title)
                or 0.0
            )

            processed.append({
                "apiname": api_name,
                "name": title,
                "description": schema.get('desc', ''),
                "achieved": int(ach['achieved']),
                "rarity": float(rarity)
            })

        processed.sort(key=lambda x: (x['achieved'], -x['rarity']))

        return processed

    except Exception as e:
        print("Critical error:", e)
        return []

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/data')
def get_data():
    app_id = request.args.get('app_id', DEFAULT_APP_ID)
    steam_id = request.args.get('steam_id', DEFAULT_STEAM_ID)
    return jsonify(fetch_steam_data(app_id, steam_id))

@app.route('/api/search')
def search_game():
    query = request.args.get('q', '')
    if len(query) < 3:
        return jsonify([])

    url = f"https://store.steampowered.com/api/storesearch/?term={query}&l=english&cc=US"
    try:
        res = requests.get(url).json()
        items = res.get('items', [])
        return jsonify([{'id': i['id'], 'name': i['name']} for i in items])
    except:
        return jsonify([])

if __name__ == "__main__":
    app.run(debug=True)