# SavannaTrace IoT

A system for monitoring and displaying a LoRa gateway's IP address using MQTT. This project consists of two main components:
1. A Python script that runs on the Raspberry Pi to publish its IP address
2. A Vue.js web interface to display the IP address

## Overview

The Gateway Monitor solves the problem of tracking a LoRa gateway's IP address when it changes due to network updates. The system:
- Automatically detects and publishes the gateway's IP address
- Provides a user-friendly web interface to view the IP
- Uses MQTT for real-time communication
- Handles network issues gracefully

## System Requirements

### For the Python Script (Raspberry Pi)
- Python 3.6+
- paho-mqtt library

### For the Vue.js UI
- Node.js 14+
- npm or yarn

## Installation

1. Clone the repository:
```bash
git clone https://github.com/tech-nickk/SavannaTrace-IoT.git
cd SavannaTrace-IoT
```

2. Install Python dependencies:
```bash
pip install paho-mqtt
```

3. Install Vue.js dependencies:
```bash
cd vue_ui/SavannaTrace-Iot
npm install

```

## Configuration

### Python Script
The script (`mqtt_publish.py`) uses these default settings:
- MQTT Broker: broker.emqx.io
- Port: 1883
- Topic: savannaTrace/ip_address
- Update Interval: 300 seconds (5 minutes)

To modify these settings, edit the constants at the top of `gateway_monitor.py`:
```python
BROKER = "broker.emqx.io"
PORT = 1883
TOPIC = "savannaTrace/ip_address"
UPDATE_INTERVAL = 300
```

### Vue.js UI
The UI connects to the same MQTT broker and topic by default. If you need to modify these settings, edit them in the Vue component.

## Usage

### Running the Python Script on Raspberry Pi
1. Navigate to the script directory:
```bash
cd python_script
```

2. Run the script:
```bash
python mqtt_publish.py
```

3. To run the script automatically on Raspberry Pi startup, add it to crontab:
```bash
crontab -e
```
Add this line:
```
@reboot python /path/to/mqtt_publish.py
```

### Running the Vue.js UI
1. Navigate to the frontend directory:
```bash
cd vue_ui/SavannaTrace-Iot
```

2. Start the development server:
```bash
npm run dev

```

3. Build for production:
```bash
npm run build

```

## Features

### Python Script
- Automatically detects the gateway's IP address
- Publishes IP address to MQTT broker
- Retries connection if broker is unavailable
- Updates IP address every 5 minutes
- Handles network disconnections gracefully

### Vue.js UI
- Real-time IP address display
- Copy to clipboard functionality
- Connection status indicators
- Responsive design
- User-friendly interface

## Troubleshooting

### Python Script
If the script fails to run:
1. Check your internet connection
2. Verify MQTT broker accessibility
3. Check console output for error messages
4. Ensure Python and required packages are installed

### Vue.js UI
If the UI fails to display:
1. Check browser console for errors
2. Verify MQTT broker connection
3. Ensure all npm dependencies are installed
4. Check if the Python script is running and publishing

