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
    #with open(info_json_path, "r") as file:
    #    info = json.load(file)

    # Bridge IP ja API-avain
    API_KEY = "AsRl61pG1VplyZgHfax7h7x7BKmYZjMx1bQBBDP5" #info.get("api_key")
    BRIDGE_IP = "192.168.10.85" #info.get("bridge_ip")

    # Välittimen määritys
    pir = MotionSensor(5)
    RELAY_PIN = 16

    relay = gpiozero.OutputDevice(
        RELAY_PIN, active_high=True, initial_value=False)

    relay_state = False  # Track the state of the relay

    i = 1

    # Endpoint kaikkien lamppujen hakemiseen
    url_get_lights = f"http://{BRIDGE_IP}/api/{API_KEY}/lights"

    return API_KEY, BRIDGE_IP, url_get_lights, pir, relay, relay_state, i


def lights_on(API_KEY, BRIDGE_IP, url_get_lights):

    # Pyyntö joka hakee kaikki yhdistetyt lamput
    response = requests.get(url_get_lights)
    lights = response.json()

    # Käy läpi jokaisen lampun ja laittaa ne päälle/pois
    for light_id in lights:
        url_set_state = f"http://{BRIDGE_IP}/api/{
            API_KEY}/lights/{light_id}/state"
        data = {"on": True}
        response = requests.put(url_set_state, json=data)
        print(f"Light {light_id} response: {response.json()}")


def lights_off(API_KEY, BRIDGE_IP, url_get_lights):

    # Pyyntö joka hakee kaikki yhdistetyt lamput
    response = requests.get(url_get_lights)
    lights = response.json()

    # Käy läpi jokaisen lampun ja laittaa ne päälle/pois
    for light_id in lights:
        url_set_state = f"http://{BRIDGE_IP}/api/{
            API_KEY}/lights/{light_id}/state"
        data = {"on": False}
        response = requests.put(url_set_state, json=data)
        print(f"Light {light_id} response: {response.json()}")


def main():
    try:
        API_KEY, BRIDGE_IP, url_get_lights, pir, relay, relay_state, i = initialization()

        while True:
            if pir.motion_detected:
                print("Motion detected.")
                if relay_state:
                    relay.off()  # Turn off if previously on
                    relay_state = False
                    print("Relay turned off.")
                    lights_off(API_KEY, BRIDGE_IP, url_get_lights)
                else:
                    relay.on()  # Turn on if previously off
                    relay_state = True
                    print("Relay turned on.")
                    lights_on(API_KEY, BRIDGE_IP, url_get_lights)
                # Debounce delay to avoid immediate re-triggering
                time.sleep(10)
            else:
                print("No motion detected.")
                time.sleep(1)
    except Exception as e:
        print(f'ERROR: {e}')
        input('Press enter to exit...')


if __name__ == '__main__':
    main()
