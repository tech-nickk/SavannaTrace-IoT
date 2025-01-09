import paho.mqtt.client as mqtt
import socket
import time

BROKER = "broker.emqx.io"
PORT = 1883
TOPIC = "savannaTrace/ip_address"
RETRY_INTERVAL = 5

def get_ip_address():
    """Retrieve the current WiFi IP address of the device."""
    try:
        hostname = socket.gethostname()
        ip_address = socket.gethostbyname(hostname)
        return ip_address
    except Exception as e:
        print(f"Error retrieving IP address: {e}")
        return "Unavailable"

def on_connect(client, userdata, flags, rc):
    """Callback when connected to the MQTT broker."""
    if rc == 0:
        print("Connected to MQTT Broker!")
        ip_address = get_ip_address()
        client.publish(TOPIC, ip_address)
        print(f"Published IP address: {ip_address}")
    else:
        print(f"Failed to connect, return code {rc}")

def main():
    client = mqtt.Client()
    client.on_connect = on_connect

    while True:
        try:
            client.connect(BROKER, PORT)
            client.loop_start()
            break  # Exit the retry loop once connected
        except Exception as e:
            print(f"Connection failed: {e}. Retrying in {RETRY_INTERVAL} seconds...")
            time.sleep(RETRY_INTERVAL)

    client.loop_forever()

if __name__ == "__main__":
    main()
