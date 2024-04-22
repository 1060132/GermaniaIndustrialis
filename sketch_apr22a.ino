#include <HardwareSerial.h>

const int numRows = 14;
const int numCols = 8;
const int potPin = 34;
const int rowPin = 13; // Pin für die Reihe
const int colPin = 12; // Pin für die Spalte
unsigned long previousMillis = 0;
unsigned long interval = 9;

enum State {
  WAIT_CLOCK_HIGH,
  READ_POT_VALUE
};

State currentState = WAIT_CLOCK_HIGH;
HardwareSerial SerialESP(1);

void setup() {
  SerialESP.begin(115200);
  pinMode(rowPin, OUTPUT);
  pinMode(colPin, OUTPUT);
  digitalWrite(rowPin, LOW);
  digitalWrite(colPin, LOW);
  while (!SerialESP) {
    delay(10);
  }
}

void loop() {
  unsigned long currentMillis = millis();

  for (int y = 0; y < numRows; y++) {
    for (int x = 0; x < numCols; x++) {
      // Schalten auf das nächste Element der Matrix
      switchMatrixElement(x, y);

      // Zustandsmaschine aktualisieren
      switch (currentState) {
        case WAIT_CLOCK_HIGH:
          if (currentMillis - previousMillis >= interval) {
            currentState = READ_POT_VALUE;
            previousMillis = currentMillis;
          }
          break;

        case READ_POT_VALUE:
          int potValue = analogRead(potPin);
          SerialESP.print(x); // x-Koordinate senden
          SerialESP.print(",");
          SerialESP.print(y); // y-Koordinate senden
          SerialESP.print(",");
          SerialESP.println(potValue); // Widerstandswert senden
          
          // Hier könntest du weitere Aktionen basierend auf dem Widerstandswert ausführen
          
          currentState = WAIT_CLOCK_HIGH;
          digitalWrite(rowPin, LOW); // Reihe deaktivieren
          delay(1); // Kurze Pause zwischen den Spalten
          digitalWrite(colPin, LOW); // Spalte deaktivieren
          delay(1); // Kurze Pause zwischen den Reihen
          break;
      }
      delay(100); // Kurze Pause zwischen den Schaltungen
    }
  }
}

void switchMatrixElement(int x, int y) {
  // Schalten der entsprechenden Reihe und Spalte basierend auf x und y
  // Hier wird davon ausgegangen, dass x die Spalte und y die Reihe ist
  // Du kannst diese Logik anpassen, falls deine Matrix anders organisiert ist oder wenn du unterschiedliche Pins verwenden möchtest.
  
  // Reihe aktivieren (HIGH setzen)
  digitalWrite(rowPin, HIGH);
  delay(1); // Kurze Pause für Stabilität
  // Spalte aktivieren (HIGH setzen)
  digitalWrite(colPin, HIGH);
  delay(1); // Kurze Pause für Stabilität
}
