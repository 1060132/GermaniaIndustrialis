#include <ArduinoBLE.h>

const int potPin = 34;
const int clockPin = 13;
int potValue = 0;
unsigned long previousMillis = 0;
unsigned long interval = 9;

enum State {
  WAIT_CLOCK_HIGH,
  READ_POT_VALUE
};

State currentState = WAIT_CLOCK_HIGH;

BLEService bleService("19B10000-E8F2-537E-4F6C-D104768A1214"); // Beispiel-Service UUID
BLECharacteristic potCharacteristic("19B10001-E8F2-537E-4F6C-D104768A1214", BLERead | BLENotify, 2); // Beispiel-Charakteristik UUID

void setup() {
  Serial.begin(115200);
  pinMode(clockPin, OUTPUT);
  digitalWrite(clockPin, LOW); 

  if (!BLE.begin()) {
    Serial.println("Starting BLE failed!");
    while (1);
  }

  BLE.setLocalName("ESP32"); // Name des Geräts für Bluetooth
  BLE.setAdvertisedService(bleService); // Service bekannt machen
  bleService.addCharacteristic(potCharacteristic); // Charakteristik zum Service hinzufügen
  BLE.addService(bleService); // Service starten

  BLE.advertise(); // Beginne mit dem Ausstrahlen der BLE-Anzeige
  Serial.println("BLE server started");
}

void loop() {
  BLEDevice central = BLE.central();

  if (central) {
    Serial.print("Connected to central: ");
    Serial.println(central.address());

    while (central.connected()) {
      unsigned long currentMillis = millis();

      switch (currentState) {
        case WAIT_CLOCK_HIGH:
          if (currentMillis - previousMillis >= interval) {
            digitalWrite(clockPin, HIGH);
            previousMillis = currentMillis;
            currentState = READ_POT_VALUE;
          }
          break;

        case READ_POT_VALUE:
          potValue = analogRead(potPin);
          potCharacteristic.writeValue((uint8_t*)&potValue, sizeof(potValue)); // Daten an die Charakteristik senden
          currentState = WAIT_CLOCK_HIGH;
          digitalWrite(clockPin, LOW);
          break;
      }
    }
    Serial.print("Disconnected from central: ");
    Serial.println(central.address());
  }
}