from flask import Flask, render_template, jsonify, request
import requests

app = Flask(__name__)

STEAM_API_KEY = 'YOUR_STEAM_API_KEY_HERE'
DEFAULT_STEAM_ID = 'YOUR_STEAM_ID_HERE' 
DEFAULT_APP_ID = '12210'

def fetch_steam_data(app_id, steam_id):
    try:
        player_url = (
            f"http://api.steampowered.com/ISteamUserStats/"
            f"GetPlayerAchievements/v0001/"
            f"?appid={app_id}&key={STEAM_API_KEY}&steamid={steam_id}"
        )
        player_res = requests.get(player_url).json()

        if 'playerstats' not in player_res or 'achievements' not in player_res['playerstats']:
            print(f"No stats found for AppID {app_id}")
            return []

        player_achievements = player_res['playerstats']['achievements']
        print(f"SUCCESS: Found {len(player_achievements)} achievements for AppID {app_id}")

        schema_map = {}
        try:
            schema_url = (
                f"http://api.steampowered.com/ISteamUserStats/GetSchemaForGame/v2/"
                f"?key={STEAM_API_KEY}&appid={app_id}&l=english"
            )
            schema_res = requests.get(schema_url).json()

            if 'game' in schema_res and 'availableGameStats' in schema_res['game']:
                stats = schema_res['game']['availableGameStats']['achievements']
                for item in stats:
                    schema_map[item['name']] = {
                        'title': item.get('displayName', item['name']),
                        'desc': item.get('description', 'No description available')
                    }
        except Exception:
            print(f"Schema Error: {e}")
            
        global_map = {}
        try:
            global_url = (
                f"http://api.steampowered.com/ISteamUserStats/"
                f"GetGlobalAchievementPercentagesForApp/v0002/"
                f"?gameid={app_id}"
            )
            global_res = requests.get(global_url).json()
            ach_list = global_res.get('achievementpercentages', {}).get('achievements', [])
            global_map = {x['name']: x['percent'] for x in ach_list}
        except Exception:
            print("Could not fetch global rarity stats.")

        processed_data = []
        for ach in player_achievements:
            api_name = ach['apiname']
            pretty_info = schema_map.get(api_name, {})
            processed_data.append({
                'apiname': api_name,
                'name': pretty_info.get('title', ach.get('name', api_name)),
                'description': pretty_info.get('desc', ach.get('description', 'No description available')),
                'achieved': int(ach['achieved']),  
                'rarity': float(global_map.get(ach['apiname'], 0.0))
            })

        processed_data.sort(key=lambda x: (x['achieved'], -x['rarity']))

        return processed_data

    except Exception as e:
        print(f"Critical Error fetching data: {e}")
        return []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/data')
def get_data():
    app_id = request.args.get('app_id', DEFAULT_APP_ID)
    steam_id = request.args.get('steam_id', DEFAULT_STEAM_ID)
    data = fetch_steam_data(app_id, steam_id)
    return jsonify(data)

@app.route('/api/search')
def search_game():
    query = request.args.get('q', '')
    if len(query) < 3:
        return jsonify([])

    url = f"https://store.steampowered.com/api/storesearch/?term={query}&l=english&cc=US"

    try:
        res = requests.get(url)
        data = res.json()
        items = data.get('items', [])
        results = [{'id': item['id'], 'name': item['name']} for item in items]
        return jsonify(results)
    except Exception as e:
        print(f"Search Error: {e}")
        return jsonify([])

if __name__ == '__main__':
    app.run(debug=True)
