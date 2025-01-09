import paho.mqtt.client as mqtt
import socket
import time
import subprocess

BROKER = "broker.emqx.io"
PORT = 1883
TOPIC = "savannaTrace/ip_address"
RETRY_INTERVAL = 5
UPDATE_INTERVAL = 300  # Check IP every 5 minutes

def get_ip_address():
    """Retrieve the current WiFi IP address of the device."""
    try:
        # For Linux/Raspberry Pi
        try:
            # Try using ip route command to get WiFi IP
            cmd = "ip route get 8.8.8.8 | awk '{print $7}' | head -1"
            ip = subprocess.check_output(cmd, shell=True).decode().strip()
            if ip:
                return ip
        except:
            pass

        # Fallback method
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # Doesn't need to be reachable
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception as e:
        print(f"Error retrieving IP address: {e}")
        return "Unavailable"

def on_connect(client, userdata, flags, rc):
    """Callback when connected to the MQTT broker."""
    if rc == 0:
        print("Connected to MQTT Broker!")
        publish_ip(client)
    else:
        print(f"Failed to connect, return code {rc}")

def on_disconnect(client, userdata, rc):
    """Callback when disconnected from the MQTT broker."""
    print("Disconnected from MQTT broker")
    if rc != 0:
        print("Unexpected disconnection. Will auto-reconnect")

def publish_ip(client):
    """Publish the current IP address."""
    ip_address = get_ip_address()
    client.publish(TOPIC, ip_address, qos=1, retain=True)
    print(f"Published IP address: {ip_address}")

def main():
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_disconnect = on_disconnect

    last_update = 0

    while True:
        try:
            if not client.is_connected():
                print(f"Connecting to broker {BROKER}...")
                client.connect(BROKER, PORT)
                client.loop_start()
            
            # Periodic IP update
            current_time = time.time()
            if current_time - last_update >= UPDATE_INTERVAL:
                if client.is_connected():
                    publish_ip(client)
                    last_update = current_time
            
            time.sleep(1)

        except Exception as e:
            print(f"Error: {e}. Retrying in {RETRY_INTERVAL} seconds...")
            time.sleep(RETRY_INTERVAL)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nProgram terminated by user")
