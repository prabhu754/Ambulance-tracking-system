#include <Arduino.h>
#include <WiFi.h>
#include <HTTPClient.h>
#include <TinyGPSPlus.h>

// Wi-Fi credentials
const char* WIFI_SSID = "oneplus";
const char* WIFI_PASS = "puni1626";

// Server details
const char* SERVER_IP = "10.48.67.9";
const int SERVER_PORT = 5000;
String serverURL;

// GPS setup
const unsigned long GPS_BAUD = 9600;
const int GPS_RX_PIN = 16; // GPS TX -> ESP32 RX2 (pin 16)
const int GPS_TX_PIN = 17; // optional (ESP32 TX2 -> GPS RX)

TinyGPSPlus gps;

unsigned long lastSend = 0;
const unsigned long SEND_INTERVAL = 2000; // send every 2 seconds

double lastLat = 0.0;
double lastLng = 0.0;

void connectWiFi() {
  Serial.printf("Connecting to WiFi: %s\n", WIFI_SSID);
  WiFi.mode(WIFI_STA);
  WiFi.disconnect(true);  // clear old connections
  delay(1000);
  WiFi.begin(WIFI_SSID, WIFI_PASS);

  unsigned long start = millis();
  while (WiFi.status() != WL_CONNECTED && millis() - start < 30000) { // wait 30s
    Serial.print(".");
    delay(500);
  }

  if (WiFi.status() == WL_CONNECTED) {
    Serial.println("\n✅ WiFi connected!");
    Serial.print("IP Address: ");
    Serial.println(WiFi.localIP());
  } else {
    Serial.println("\n❌ WiFi connection failed!");
  }
}

void setup() {
  Serial.begin(115200);
  delay(500);
  Serial2.begin(GPS_BAUD, SERIAL_8N1, GPS_RX_PIN, GPS_TX_PIN);

  connectWiFi();

  serverURL = "http://" + String(SERVER_IP) + ":" + String(SERVER_PORT) + "/update";
  Serial.println("Server URL: " + serverURL);
}

void loop() {
  // Feed GPS parser
  while (Serial2.available()) {
    gps.encode(Serial2.read());
  }

  // Send GPS data when updated
  if (gps.location.isUpdated()) {
    double lat = gps.location.lat();
    double lng = gps.location.lng();
    bool valid = gps.location.isValid();
    Serial.printf("GPS: lat=%.6f, lng=%.6f, valid=%d\n", lat, lng, valid ? 1 : 0);

    if (valid && millis() - lastSend >= SEND_INTERVAL && WiFi.status() == WL_CONNECTED) {
      lastSend = millis();

      HTTPClient http;
      String payload = "lat=" + String(lat, 6) + "&lng=" + String(lng, 6);
      Serial.println("Sending to server: " + payload);

      http.begin(serverURL);
      http.addHeader("Content-Type", "application/x-www-form-urlencoded");
      int httpCode = http.POST(payload);

      if (httpCode > 0) {
        Serial.printf("Server response (%d): %s\n", httpCode, http.getString().c_str());
      } else {
        Serial.printf("HTTP POST failed! Error: %s\n", http.errorToString(httpCode).c_str());
      }
      http.end();
    }
  }

  delay(10);
}
