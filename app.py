from flask import Flask, render_template_string
import requests
from flask_socketio import SocketIO
import time
import json
import threading

"""
NOTES:
-socket.io:n implementointi !!
"""

app = Flask(__name__)
socketio = SocketIO(app)  # Initialize SocketIO with your Flask app

API_KEY = "AsRl61pG1VplyZgHfax7h7x7BKmYZjMx1bQBBDP5"
BRIDGE_IP = "192.168.10.85"
url_get_lights = f"http://{BRIDGE_IP}/api/{API_KEY}/lights"

"""
@app.route('/')
def home():
    html_content = '<h1>Lights Status</h1>'
    if False:
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
"""


def fetch_and_emit_light_status():
    # Assuming you want to periodically fetch light status and broadcast it
    response = requests.get(url_get_lights)
    lights = response.json()
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

    # Emit the light status to all connected clients
    socketio.emit('update_light_status', {'html_content': html_content})

    # Send data to external website
    # Adjust the endpoint as necessary
    url = 'https://liiketunnistin.azurewebsites.net'
    headers = {'Content-Type': 'application/json'}
    # Convert the Python dictionary to a JSON string
    data = json.dumps(all_lights)

    try:
        response = requests.post(url, headers=headers, data=data)
        if response.status_code == 200:
            print("Data sent successfully")
        else:
            print(f"Failed to send data: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")


if __name__ == '__main__':
    app.run(debug=True)
