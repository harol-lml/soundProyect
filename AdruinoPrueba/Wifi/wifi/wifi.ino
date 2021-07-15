
































#include <WiFi.h>
#include <WiFiClient.h>
#include <WebServer.h>
#include <ESPmDNS.h>

const char* ssid = "PRUEBACLARO";/*"HOME-5B22";*/
const char* password = "12345678#";/*"5742634166";*/
const int analogInPin = 34;

int sensorValue = 0;
int outputValue = 0; 

WebServer server(80);

void handleRoot() {
  //digitalWrite(led, 1);
  sensorValue = analogRead(analogInPin);
  double lect=(sensorValue+83.2073)/11.003;
  String msn = String(lect);
  Serial.println(msn);
  server.send(200, "text/plain", msn);
  //digitalWrite(led, 0);
}

void handleNotFound() {
  //digitalWrite(led, 1);
  String message = "File Not Found\n\n";
  message += "URI: ";
  message += server.uri();
  message += "\nMethod: ";
  message += (server.method() == HTTP_GET) ? "GET" : "POST";
  message += "\nArguments: ";
  message += server.args();
  message += "\n";
  for (uint8_t i = 0; i < server.args(); i++) {
    message += " " + server.argName(i) + ": " + server.arg(i) + "\n";
  }
  server.send(404, "text/plain", message);
  //digitalWrite(led, 0);
}

void setup() {

  Serial.begin(115200);
  pinMode(analogInPin,INPUT);
  adcAttachPin(analogInPin);
  analogReadResolution(11);
  analogSetAttenuation(ADC_6db);
  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, password);
  Serial.println("");

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("");
  Serial.print("Connected to ");
  Serial.println(ssid);
  Serial.print("IP address: ");
  Serial.println(WiFi.localIP());

  if (MDNS.begin("esp32")) {
    Serial.println("MDNS responder started");
  }

  server.on("/", handleRoot);

  server.on("/inline", []() {
    server.send(200, "text/plain", "this works as well");
  });

  server.onNotFound(handleNotFound);

  server.begin();
  Serial.println("HTTP server started");

}

void loop(){
  server.handleClient();
  sensorValue = analogRead(analogInPin);
  
  // change the analog out value:
  Serial.print("sensor = ");
  Serial.print(sensorValue);
  Serial.print("\t out.db= ");
  Serial.println((sensorValue+83.2073)/11.003);
  delay(100);

}
