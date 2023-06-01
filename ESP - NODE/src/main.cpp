#include <WiFi.h>
#include <PubSubClient.h>
#include <Servo.h>
#include <LiquidCrystal.h>
#include <ArduinoJson.h>

const char* ssid = "brisa-2557393";
const char* password =  "q2rl6shg";
const char* mqttServer = "192.168.1.6";
const int mqttPort = 1883;
const char* mqttUser = "ifpb";
const char* mqttPassword = "ifpb";
#define SOUND_SPEED 0.034
#define CM_TO_INCH 0.393701
const int trigPin = 5;
const int echoPin = 18;
bool allow = true;
Servo myservo;
LiquidCrystal lcd(32, 27, 21, 17, 16, 4);
long duration;
float distanceCm;
WiFiClient espClient;
PubSubClient client(espClient);
// RS = 32
// E = 27
// D4 = 21
// D5 = 17
// D6 = 16
// D7 = 4


void openBarrier(const char* name) {
  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print("ACESSO LIBERADO!");
  // lcd.setCursor(0, 1);
  // lcd.print(name);

  digitalWrite(22, LOW);
  digitalWrite(19, HIGH);
  myservo.write(90);
  distanceCm = 0;
  while(distanceCm < 20){
    digitalWrite(trigPin, LOW);
    delayMicroseconds(2);

    digitalWrite(trigPin, HIGH);
    delayMicroseconds(10);
    digitalWrite(trigPin, LOW);
    
    duration = pulseIn(echoPin, HIGH);
    
    distanceCm = duration * SOUND_SPEED/2;
  }
  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print("VOLTE SEMPRE!");
  delay(3000);

  myservo.write(0);
  digitalWrite(19, LOW);
  digitalWrite(22, HIGH);
  allow = false;
  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print("IDENTIFIQUE-SE!");
  return;
}

String lastName = "";
void callback(char* topic, byte* payload, unsigned int length) {
  DynamicJsonDocument doc(length);
  deserializeJson(doc, payload);  
  serializeJsonPretty(doc, Serial);
  Serial.println();
  const char* currName = doc["name"];
  
  if((bool) doc["allow"] && currName != lastName.c_str()){
    Serial.println("Permitido");
    lastName = currName;
    Serial.println(currName);
    openBarrier(currName);
  }else{
    lastName = "";
    Serial.println("Não permitido");
  }
  return;
}

long lastReconnectAttempt = 0;

boolean reconnect() {
  if (client.connect("arduinoClient")) {
    // Once connected, publish an announcement...
    client.publish("outTopic","hello world");
    // ... and resubscribe
    client.subscribe("inTopic");
  }
  return client.connected();
}
 
void setup() {
  Serial.begin(115200);

  pinMode(22, OUTPUT);
  pinMode(19, OUTPUT);
  digitalWrite(22, HIGH);
  digitalWrite(19, LOW);

  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);

  myservo.attach(13);
  myservo.write(0);

  
  lcd.begin(16, 2);
  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print("IDENTIFIQUE-SE!");

  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.println("Connecting to WiFi..");
  }
  Serial.println("Connected to the WiFi network");
  client.setServer(mqttServer, mqttPort);
  client.setCallback(callback);
  while (!client.connected()) {

    Serial.println("Connecting to MQTT...");
 
    if (client.connect("ESP-NODE", mqttUser, mqttPassword)) {
 
      Serial.println("connected");  
 
    } else {
 
      Serial.print("failed with state ");
      Serial.print(client.state());
      delay(2000);
 
    }
    delay(2000);
  }
 
  client.subscribe("status");
 
}

void loop() {
  if (!client.connected()) {
      long now = millis();
      if (now - lastReconnectAttempt > 5000) {
        lastReconnectAttempt = now;
        // Attempt to reconnect
        if (reconnect()) {
          lastReconnectAttempt = 0;
        }
      }
    } else {
      // Client connected
      client.loop();
    }
}

