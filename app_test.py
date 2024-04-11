from flask import Flask, jsonify
import requests

app = Flask(__name__)

API_KEY = "AsRl61pG1VplyZgHfax7h7x7BKmYZjMx1bQBBDP5"
BRIDGE_IP = "192.168.10.85"
url_get_lights = f"http://{BRIDGE_IP}/api/{API_KEY}/lights"

@app.route('/lights_status')
def lights_status():
    response = requests.get(url_get_lights)
    lights = response.json()
    
    all_lights = []
    for light_id, light_data in lights.items():
        all_lights.append({
            "id": light_id,
            "name": light_data['name'],
            "state": "on" if light_data['state']['on'] else "off"
        })
    return jsonify(all_lights)

if __name__ == '__main__':
    app.run(debug=True)
