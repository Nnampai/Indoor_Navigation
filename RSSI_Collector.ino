#include <WiFi.h>
#include <PubSubClient.h>
#include <NimBLEDevice.h>
//#include <NimBLEAdvertisedDevice.h>
//#include "NimBLEBeacon.h"

// WiFi setting
const char* ssid = "Suda";
const char* password = "027222307";

WiFiClient espClient;

// NETPIE setting
const char* mqtt_client = "02868f7c-d4eb-4fd0-9b9c-b48c27137659";
const char* mqtt_username = "KmZjJWyAoACCJsAk6dJKzhu959VrTQzx";
const char* mqtt_password = "G5XBx7cSvBgxf6KQ9KHWhAfTsooqNS7e";

const char* mqtt_server = "broker.netpie.io";
const int mqtt_port = 1883;

PubSubClient client(espClient);

// BLE setting
int scanTime = 5 * 1000; // In milliseconds
NimBLEScan* pBLEScan;

int RSSI1 = -100, RSSI2 = -100, RSSI3 = -100;
char msg[150];

class ScanCallbacks : public NimBLEScanCallbacks {
  void onResult(const NimBLEAdvertisedDevice* advertisedDevice) override {
    String deviceName = advertisedDevice->getName().c_str(); // Read all names of scanned devices
    if (deviceName == "Beacon1") {
      RSSI1 = advertisedDevice->getRSSI();
    } else if (deviceName == "Beacon2") {
      RSSI2 = advertisedDevice->getRSSI();
    } else if (deviceName == "Beacon3") {
      RSSI3 = advertisedDevice->getRSSI();
    }
  }
} scanCallbacks;

void setup() {
  // BLE
  NimBLEDevice::init("Beacon-scanner");
  pBLEScan = BLEDevice::getScan();
  pBLEScan->setScanCallbacks(&scanCallbacks);
  pBLEScan->setActiveScan(true);
  pBLEScan->setInterval(100);
  pBLEScan->setWindow(100);

  // Wi-Fi
  WiFi.begin(ssid, password);

  // MQTT
  client.setServer(mqtt_server, mqtt_port);
  client.connect(mqtt_client, mqtt_username, mqtt_password);
}

void loop() {
  // BLE scan
  pBLEScan->getResults(scanTime, false);
  pBLEScan->clearResults(); // delete results scan buffer to release memory

  // Publish to MQTT
  if(client.connected()) { // Check MQTT
    client.loop();
  
    String payload = "{\"data\": {";
    payload.concat("\"RSSI1\":" + String(RSSI1));
    payload.concat(", "); // separator between data
    payload.concat("\"RSSI2\":" + String(RSSI2));
    payload.concat(", ");
    payload.concat("\"RSSI3\":" + String(RSSI3));
    payload.concat("}}");

    payload.toCharArray(msg, (payload.length()+1)); 
    client.publish("@shadow/data/update", msg); // Update data in NETPIE feed
    client.publish("@msg/data", msg); // Send data to topic

  } else {
    if(WiFi.status() == WL_CONNECTED) { // Check Wi-Fi
      client.disconnect();
      client.connect(mqtt_client, mqtt_username, mqtt_password);
    } else {
      WiFi.disconnect();
      WiFi.begin(ssid, password);
    }
  }
  delay(1000);
}
