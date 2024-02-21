import machine
import utime
import random
import micropython
from umqtt.simple import MQTTClient 
import network



MQTT_BROKER_ADDR = "homeassistant.local" # your MQTT borker IP
MQTT_PORT = 1883

# Replace with your desired client ID
MQTT_CLIENT_ID = "pico_w_subscriber" 

# Replace with the topic you want to subscribe to
MQTT_SUBSCRIBE_TOPIC = "/everything/smart/home" # your home assistant mqtt topic to subscribe

MQTT_TOPIC_PUBLISH = "home_automation/led_status" # your mqtt topic


# Replace with your username and password if required
MQTT_USERNAME = ""  # "username" if needed
MQTT_PASSWORD =  "" # "password" if needed

SSID = "<your-network-ssid>"
PASSWORD = "<your-network-password>"

led = machine.Pin('LED',machine.Pin.OUT)

def wifi_connect():
    wifi = network.WLAN(network.STA_IF)
    wifi.active(True)
    wifi.connect(SSID,PASSWORD)
    while not wifi.isconnected():
        pass

def decode_status(status):
    if status == 1:
        return "ON"
    else:
        return "OFF"

def publish(status:int):
    global client1
    try:
        
        print("Connected to the MQTT broker")
        client.publish("/led/status",decode_status(status),True)
        print(f"Published status: {status}")
        print("Disconnected form the MQTT Client")
    except Exception as e:
        print(f"Error publishing status: {e}")

def mqtt_connect():
    """Connects to the MQTT broker and subscribes to the topic."""
    global client
    try:
        client = MQTTClient(MQTT_CLIENT_ID, MQTT_BROKER_ADDR,port=1883,user=MQTT_USERNAME,password=MQTT_PASSWORD)
        client.connect()
        print("Connected to MQTT broker.")
        client.set_callback(mqtt_callback)
        client.subscribe(MQTT_SUBSCRIBE_TOPIC, 0)  # QoS level 1
        print("Subscribed to topic:", MQTT_SUBSCRIBE_TOPIC)
    except Exception as e:
        print("MQTT connection failed:", e)

def mqtt_callback(topic,msg):
    payload_bytes = bytearray(msg)
    mqtt_topic_bytes = bytearray(topic)
    payload = payload_bytes.decode("utf-8")
    mqtt_topic = mqtt_topic_bytes.decode("utf-8")
    if mqtt_topic == MQTT_SUBSCRIBE_TOPIC and payload == "ON":
        led.value(1)
        publish(led.value())
        print("Received message on topic onnn {}: {}".format(topic, msg))
    elif mqtt_topic == MQTT_SUBSCRIBE_TOPIC and payload == "OFF":
        led.value(0)
        publish(led.value())
    else:
        pass

def main():
    """Main program loop."""
    wifi_connect()
    mqtt_connect()
    
    while True:
        try:
            client.wait_msg()
            utime.sleep(1)  # Check for messages periodically
        except Exception as e:
            print("MQTT error:", e)
            utime.sleep(0.5)  # Wait for reconnection

if __name__ == "__main__":
    main()

