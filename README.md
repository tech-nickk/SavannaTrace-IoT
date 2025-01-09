# SavannaTrace IoT Project

This project demonstrates an IoT application where a Raspberry Pi publishes its IP address to an MQTT broker, and a VueJS-based UI displays it.

## Features
- Publish the Raspberry Pi's IP address to an MQTT topic.
- Retry mechanism for MQTT connection failures.
- VueJS-based UI for displaying the IP address.

## Requirements
- Python 3.x
- Node.js and npm
- Raspberry Pi with WiFi connection

## Usage
### Python Script
1. Navigate to the `python_script/` folder.
2. Install the required libraries:
   ```bash
   pip install paho-mqtt
