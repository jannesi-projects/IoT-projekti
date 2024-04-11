import requests
import os
import json
from gpiozero import MotionSensor
import gpiozero
import time


def initialization():

    current_dir = os.getcwd()
    info_json_path = os.path.join(current_dir, "info.json")

    # Lukee tiedot json-tiedostosta
    # with open(info_json_path, "r") as file:
    #    info = json.load(file)

    # Bridge IP ja API-avain
    API_KEY = "AsRl61pG1VplyZgHfax7h7x7BKmYZjMx1bQBBDP5"  # info.get("api_key")
    BRIDGE_IP = "192.168.10.85"  # info.get("bridge_ip")

    # Endpoint kaikkien lamppujen hakemiseen
    url_get_lights = f"http://{BRIDGE_IP}/api/{API_KEY}/lights"

    return API_KEY, BRIDGE_IP, url_get_lights


def check_lights_and_names(API_KEY, BRIDGE_IP, url_get_lights):
    # Request to fetch all connected lights
    response = requests.get(url_get_lights)
    lights = response.json()

    all_lights = []
    light_states = {
        "1": "",
        "2": "",
        "3": "",
        "4": "",
        "5": "",
        "6": "",
        "8": "",
        "9": "",
        "10": "",
        "12": "",
        "13": "",
        "14": "",
        "20": "",
        "21": ""
    }

    # Iterate through each light and print its name and if it's on or off
    for light_id, light_data in lights.items():
        light_name = light_data['name']  # This line gets the light's name
        # This gets whether the light is on or off
        light_state = light_data['state']['on']
        state_str = "on" if light_state else "off"

        print(f"Light {light_id} ({light_name}) is {state_str}.")

        data = {
            f"{light_id}": {
                "id": light_id,
                "name": light_name,
                "state": light_state
            }
        }

        light_states.update(data)

        all_lights.append(data)

    x = light_states.keys()
    print(x)

    for key in x:
        print(light_states[f"{key}"]["name"])
        print(light_states[f"{key}"]["state"])
        print("\n")


def main():
    try:
        API_KEY, BRIDGE_IP, url_get_lights = initialization()

        check_lights_and_names(API_KEY, BRIDGE_IP, url_get_lights)

    except Exception as e:
        print(f'ERROR: {e}')
        input('Press enter to exit...')


if __name__ == '__main__':
    main()
