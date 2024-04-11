from flask import Flask, render_template_string
import requests
import time
import json
import threading

print("hei")

app = Flask(__name__)

API_KEY = "AsRl61pG1VplyZgHfax7h7x7BKmYZjMx1bQBBDP5"
BRIDGE_IP = "192.168.10.85"
url_get_lights = f"http://{BRIDGE_IP}/api/{API_KEY}/lights"


@app.route('/')
def home():
    response = requests.get(url_get_lights)
    lights = response.json()
    print(lights)
    all_lights = []
    for light_id, light_data in lights.items():
        light_name = light_data['name']
        light_state = light_data['state']['on']
        all_lights.append({
            "id": light_id,
            "name": light_name,
            "state": "on" if light_state else "off"
        })

    # Generate HTML content dynamically based on the lights' states
    html_content = '<h1>Lights Status</h1>'
    for light in all_lights:
        html_content += f'<p>{light["name"]} (ID: {light["id"]}) is {light["state"]}.</p>'
    
    return render_template_string(html_content)


if __name__ == '__main__':
    app.run(debug=True)
