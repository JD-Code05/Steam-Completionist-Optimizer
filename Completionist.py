from flask import Flask, render_template, jsonify, request
import requests

app = Flask(__name__)

# CONFIGURATION
STEAM_API_KEY = '5DAA9B7B2270CB94698C0C00349C6BE8'
DEFAULT_STEAM_ID = '76561198979373921'

def fetch_steam_data(app_id, steam_id):
    try:
        player_url = f"http://api.steampowered.com/ISteamUserStats/GetPlayerAchievements/v0001/?appid={app_id}&key={STEAM_API_KEY}&steamid={steam_id}"
        player_res = requests.get(player_url).json()

        if 'playerstats' not in player_res or 'achievements' not in player_res['playerstats']:
            print(f"❌ No stats found for AppID {app_id}")
            return []

        player_achievements = player_res['playerstats']['achievements']
        print(f"✅ SUCCESS: Found {len(player_achievements)} achievements for AppID {app_id}")

        global_map = {}
        try:
            global_url = f"http://api.steampowered.com/ISteamUserStats/GetGlobalAchievementPercentagesForApp/v0002/?gameid={app_id}"
            global_res = requests.get(global_url).json()
            ach_list = global_res.get('achievementpercentages', {}).get('achievements', [])
            global_map = {x['name']: x['percent'] for x in ach_list}
        except Exception:
            print("⚠️ Warning: Could not fetch global rarity stats. Using defaults.")

        processed_data = []
        for ach in player_achievements:
            processed_data.append({
                'apiname': ach['apiname'],
                # Fallback: If 'name' is missing, use the ID (e.g. THETOUR)
                'name' : ach.get('name', ach['apiname']),
                'description': ach.get('description', ''),
                'achieved': ach['achieved'],
                'rarity': global_map.get(ach['apiname'], 0)
            })
        
        # Sort: Easiest (High Rarity %) first, then Unlocked first
        processed_data.sort(key=lambda x: x['rarity'], reverse=True)
        processed_data.sort(key=lambda x: x['achieved'])
        
        return processed_data

    except Exception as e:
        print(f"🔥 Critical Error fetching data: {e}")
        return []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/data')
def get_data():
    app_id = request.args.get('app_id', '1245620') 
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