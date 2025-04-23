import paho.mqtt.client as mqtt
import json
import threading
import config

# Global variables
mqtt_data = {"RSSI1": None, "RSSI2": None, "RSSI3": None}
mqtt_client = None
mqtt_thread = None

# MQTT Callback
def on_connect(client, userdata, flags, rc, properties=None):
    print(f"Connected with result code {rc}")
    client.subscribe(config.MQTT_TOPIC)

def on_disconnect(client, userdata, rc):
    if rc != 0:
        print(f"Disconnected unexpectedly with result code {rc}, reconnecting...")
    else:
        print("Disconnected cleanly.")

def on_message(client, userdata, msg):
    global mqtt_data
    try:
        payload = msg.payload.decode("utf-8") # Decode the message
        data = json.loads(payload) # Parse JSON data
        mqtt_data["RSSI1"] = data["data"]["RSSI1"]
        mqtt_data["RSSI2"] = data["data"]["RSSI2"]
        mqtt_data["RSSI3"] = data["data"]["RSSI3"]

        # Print the received RSSI values
        print(f"Updated MQTT Data: {mqtt_data}")

    except Exception as e:
        print(f"Error processing message: {e}")

def start_mqtt():
    global mqtt_client, mqtt_thread
    if mqtt_client is None:
        mqtt_client = mqtt.Client(client_id=config.MQTT_CLIENT)
        mqtt_client.username_pw_set(config.MQTT_USERNAME, config.MQTT_PASSWORD)
        mqtt_client.on_connect = on_connect
        mqtt_client.on_disconnect = on_disconnect
        mqtt_client.on_message = on_message

        try:
            mqtt_client.connect(config.MQTT_SERVER, config.MQTT_PORT, 60)
        except Exception as e:
            print(f"Unable to connect to MQTT broker: {e}")
            return

        # Run the MQTT client loop in a separate thread so it doesn't block the main program.
        mqtt_thread = threading.Thread(target=mqtt_client.loop_forever)
        mqtt_thread.daemon = True
        mqtt_thread.start()
        print("MQTT client started and listening...")

def stop_mqtt():
    global mqtt_client, mqtt_thread
    if mqtt_client is not None:
        print("Stopping MQTT client...")
        mqtt_client.disconnect()
        mqtt_client = None
        mqtt_thread = None

'''
import paho.mqtt.client as mqtt
import json
import threading
import config

# Global variable
mqtt_data = {"RSSI1": None, "RSSI2": None, "RSSI3": None}

# MQTT Callback
def on_connect(client, userdata, flags, rc, properties=None):
    print(f"Connected with result code {rc}")
    client.subscribe(config.MQTT_TOPIC)

def on_disconnect(client, userdata, rc):
    if rc != 0:
        print(f"Disconnected unexpectedly with result code {rc}, reconnecting...")
    else:
        print("Disconnected cleanly.")

def on_message(client, userdata, msg):
    global mqtt_data
    try:
        payload = msg.payload.decode("utf-8") # Decode the message
        data = json.loads(payload) # Parse JSON data
        mqtt_data["RSSI1"] = data["data"]["RSSI1"]
        mqtt_data["RSSI2"] = data["data"]["RSSI2"]
        mqtt_data["RSSI3"] = data["data"]["RSSI3"]

        # Print the received RSSI values
        print(f"Updated MQTT Data: {mqtt_data}")

    except Exception as e:
        print(f"Error processing message: {e}")

def start_mqtt():
    # Create client MQTT
    client = mqtt.Client(client_id=config.MQTT_CLIENT)
    client.username_pw_set(config.MQTT_USERNAME, config.MQTT_PASSWORD)
    client.on_connect = on_connect
    client.on_disconnect = on_disconnect
    client.on_message = on_message

    try:
        client.connect(config.MQTT_SERVER, config.MQTT_PORT, 60)
    except Exception as e:
        print(f"Unable to connect to MQTT broker: {e}")
        return

    # Run the MQTT client loop in a separate thread so it doesn't block the main program.
    mqtt_thread = threading.Thread(target=client.loop_forever)
    mqtt_thread.daemon = True
    mqtt_thread.start()
    print("MQTT client started and listening...")
'''