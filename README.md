# 🧭 Indoor Bluetooth Navigation System
Indoor navigation system using Bluetooth RSSI fingerprinting, KNN location estimation, and A* pathfinding, with a real-time web interface built using Streamlit. The system consists of:
* ESP32-based beacon and RSSI collector nodes (Arduino)
* MQTT communication
* Python backend for location estimation and pathfinding
* Live indoor map visualization


## 📦 Project Structure
<pre>
project/
├── BLE_Beacon/                  # Arduino code for ESP32 beacon
│   └── BLE_Beacon.ino
├── RSSI_Collector/              # Arduino code for ESP32 RSSI scanner
│   └── RSSI_Collector.ino
└── navigation/                  # Python application directory
    ├── main.py                  # Streamlit main app
    ├── config.py                # Configurations and static data
    ├── mqtt_handler.py          # MQTT client to receive RSSI
    ├── location_finder.py       # KNN location estimation
    ├── navigation.py            # A* algorithm implementation
    ├── find_coordinate.py       # Helper for drawing path on map
    ├── Database.csv             # RSSI fingerprint dataset
    ├── Map.png                  # Map image
    ├── Map_allpoint.png         # Map with all coordinates labeled
    ├── icon_beacon.png          # Marker icon for current location
    ├── icon_goal.png            # Marker icon for goal
    └── pages/
        └── navigate.py          # Sub-page to handle navigation UI
</pre>


## 💻 Development Tools
### 🛠 Arduino Environment
* Arduino IDE Version: 2.3.4
* ESP32 Board Package:
    * ESP32 by Espressif Systems: version 3.1.1
* Required Libraries:
    * ESP32 BLE Arduino by Neil Kolban / nkolban: version 1.0.1
    * NimBLE-Arduino: version 2.2.1
    * ArduinoJson: version 7.3.0
    * PubSubClient: version 2.8
### 🧠 Python Environment
* Python Version: 3.9+ (Tested on: Python 3.13)
* Recommended IDE: PyCharm Community/Professional Edition
(Tested on: PyCharm 2024.3.2)


## 🧠 Key Features
* 📡 Live RSSI input via MQTT
* 📍 K-Nearest Neighbors (KNN) to classify current location from RSSI values
* 🧠 A* Search for optimal indoor path calculation
* 🗺️ Map visualization with real-time location updates
* 🌐 Web interface (Streamlit) for selecting and navigating between rooms


## 🚀 How to Run (Python)
1. Install requirements:
<pre> pip install streamlit pandas numpy scikit-learn paho-mqtt </pre>
2. Run the app:
<pre> streamlit run main.py </pre>
3. Navigate to http://localhost:8501 in your browser.


## 🔄 How It Works
1. ESP32 beacon advertises a Bluetooth signal.
2. ESP32 RSSI Collector scans RSSI values and sends them via MQTT.
3. Python backend:
      * Receives data in real time (mqtt_handler.py)
      * Estimates current location (location_finder.py)
      * Calculates path using A* (navigation.py)
      * Updates map and path live in the browser (main.py + Streamlit)
