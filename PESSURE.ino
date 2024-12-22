//LIBS
#include <LiquidCrystal_I2C.h>
#include <RTClib.h>
#include <Wire.h>
#include <WiFi.h>
#include <SD.h>
#include <SPI.h>

#define CS_PIN 5  // Replace 5 with the correct pin if needed

const char* ssid = "SIH_2024_07";
const char* password = "1234567@";
const char* serverIP = "192.168.0.230";
const int serverPort = 11112;

//Input pins
const int pressurePin = A0;
const int flowSensorPin = 2;

//decleration
LiquidCrystal_I2C lcd(0x27, 16, 2);
WiFiClient client;
RTC_DS3231 rtc;

float offset = 0.00;
float pressureMPa = 0.00;
float pressurebar = 0.00;
float height = 0.00;
float flowRate = 0.00;  // L/min
float waterSaved = 0.00;

volatile int pulseCount = 0;
unsigned long oldTime = 0;

String T_F = "False";
String security = "False";
String Internet = "False";

void setup() {
  Serial.begin(9600);
  pinMode(flowSensorPin, INPUT_PULLUP);
  attachInterrupt(digitalPinToInterrupt(flowSensorPin), countPulse, FALLING);
  // Initialize SD card
  if (!SD.begin(CS_PIN)) {
    Serial.println("SD card initialization failed!");
    while (1)
      ;  // Halt execution
  }
  Serial.println("SD card initialized.");
  Wire.begin();
  lcd.init();
  lcd.backlight();
  lcd.setCursor(0, 0);
  lcd.print("Welcome!");
  delay(1000);
  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print("Connecting...");

  // Initialize RTC
  if (!rtc.begin()) {
    Serial.println("Couldn't find RTC");
    while (1)
      ;
  }

  if (rtc.lostPower()) {
    Serial.println("RTC lost power, setting the time!");
    rtc.adjust(DateTime(F(__DATE__), F(__TIME__)));
  }

  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(250);
    Serial.print(".");
  }
  Serial.println("\nConnected to Wi-Fi!");

  calibrationOffset();
}

void loop() {
  calculatePressure();
  calculateWaterHeight();
  calculateFlowRate();
  waterSave();
  flowTF();
  displayData();

  lcd.setCursor(0, 0);
  lcd.print("P: ");
  lcd.print(pressureMPa * 10, 4);
  lcd.print(" bar");

  lcd.setCursor(0, 1);
  lcd.print("H: ");
  lcd.print(height, 4);
  lcd.print(" m");
  delay(500);

  DateTime now = rtc.now();
  char datetimeStr[100];
  snprintf(datetimeStr, sizeof(datetimeStr), "%04d-%02d-%02d %02d:%02d:%02d,", now.year(), now.month(), now.day(), now.hour(), now.minute(), now.second());
  // char timeStr[17];
  // snprintf(timeStr, sizeof(timeStr), "%02d:%02d:%02d", now.hour(), now.minute(), now.second());
  char message1[100];
  snprintf(message1, sizeof(message1), "%.4f, %.4f, %.4f, %.4f, %.1f,", pressureMPa*10, height, flowRate, waterSaved, 98.2);
  char message2[50];
  snprintf(message2, sizeof(message2), "%s, %s, %s", T_F, security, "False");  //  pressure,     , height, flowRate ,Watersaved","Battery Percentage"
  //                                               , "Tap Opened", "Safety", "Battery Strength"
  char mainstr[200];
  snprintf(mainstr, sizeof(mainstr), "%s %s %s", message1, datetimeStr, message2);

  File file = SD.open("/Readings.txt", FILE_APPEND);
  if (file) {
    file.println(mainstr);
    file.close();
    Serial.print("Data appended: ");
    Serial.println(mainstr);
  } else {
    Serial.println("Failed to open file for appending.");
  }

  if (WiFi.status() == WL_CONNECTED || Internet == "True") {
    if (!client.connected()) {
      Serial.println("Connecting to server...");
      if (client.connect(serverIP, serverPort)) {
        Serial.println("Connected to server!");
      } else {
        Serial.println("Connection failed, retrying...");
        delay(5000);
        return;
      }
    }
    client.println(mainstr);

    Serial.println("Data sent: " + String(mainstr));
    if (client.available()) {
      String receivedData = client.readStringUntil('\n');
      Serial.println("Received from server: " + receivedData);
    }
  } else {
    Serial.println("Can't connect, logging without sending");
  }
  delay(7000);
  lcd.clear();
  Security(26);
}

//All the functions
void calibrationOffset() {
  for (int i = 0; i < 50; i++) {
    int pressureValue = analogRead(pressurePin);
    float voltage = pressureValue * (3.3 / 4096.0) + 0.1621;
    offset += 2 * (voltage - 0.5) / 5;
  }
  offset /= 50;
  Serial.print("Offset: ");
  Serial.println(offset, 4);
}  //D

void calculatePressure() {
  int pressureValue = analogRead(pressurePin);
  float voltage = pressureValue * (3.3 / 4096.0) + 0.1621;
  float currentPressureMPa = 2 * (voltage - 0.5) / 5 - offset;
  pressureMPa = abs(currentPressureMPa);

}  //D

void calculateWaterHeight() {
  float pressurePa = pressureMPa * 1000000.0;
  height = pressurePa / (1000.0 * 9.81);

}  //D

void displayData() {
  Serial.print("Water Pressure: ");
  Serial.print(pressureMPa * 10, 4);
  Serial.println(" bar");

  Serial.print("Height: ");
  Serial.print(height, 4);
  Serial.println(" m");

  Serial.print("flow rate: ");
  Serial.print(flowRate, 4);
  Serial.println(" L/min");

  Serial.print("water saved: ");
  Serial.print(waterSaved, 4);
  Serial.println(" L");

  Serial.print("Water Flowing: ");
  Serial.print(T_F);
  Serial.println(" ");
  Serial.println("----------------");
}  //D

void calculateFlowRate() {
  flowRate = (pulseCount / 450.0) * 60.0;
  pulseCount = 0;
}  //D

void countPulse() {
  pulseCount++;
}  //D

void waterSave() {
  unsigned long currentTime = millis();
  unsigned long timeInterval = currentTime - oldTime;
  float volumeInInterval = (flowRate / 60.0);  // L/min to L/s
  waterSaved += volumeInInterval;
  oldTime = currentTime;
}  //D

void flowTF() {
  if (flowRate != 0) {
    T_F = "True";
  } else {
    T_F = "False";  // Add an explicit action for clarity
  }
}  //D

void Security(int pin) {
  int state = digitalRead(pin);  // Read the pin state
  if (state == LOW) {
    security = "False";
  } else {
    security = "True";  // Set it explicitly
  }

}  //D
