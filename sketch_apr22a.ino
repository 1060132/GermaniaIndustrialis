#include <HardwareSerial.h>

const int numRows = 14;
const int numCols = 8;
const int potPin = 34;
const int rowPin = 13; // Pin für die Reihe
const int colPin = 12; // Pin für die Spalte
unsigned long previousMillis = 0;
unsigned long interval = 9;
int type;

enum State
{
  WAIT_CLOCK_HIGH,
  READ_POT_VALUE
};

State currentState = WAIT_CLOCK_HIGH;
HardwareSerial SerialESP(1);

void setup()
{
  SerialESP.begin(115200);
  pinMode(rowPin, OUTPUT);
  pinMode(colPin, OUTPUT);
  digitalWrite(rowPin, LOW);
  digitalWrite(colPin, LOW);
  while (!SerialESP)
  {
    delay(10);
  }
}

void loop()
{
  unsigned long currentMillis = millis();
  for (int y = 0; y < numRows; y++)
  {
    for (int x = 0; x < numCols; x++)
    {
      digitalWrite(rowPin, LOW);
      digitalWrite(colPin, LOW);
      switch (currentState)
      {
      case WAIT_CLOCK_HIGH:
        if (currentMillis - previousMillis >= interval)
        {
          currentState = READ_POT_VALUE;
          previousMillis = currentMillis;
        }
        break;

      case READ_POT_VALUE:
        int potValue = analogRead(potPin);
        Serial.print(potValue);
        if (potValue > 1861 && potValue < 2295)
          type = 1;
        else if (potValue > 2295 && potValue < 2729)
          type = 2;
        else if (potValue > 2729 && potValue < 3163)
          type = 3;
        else if (potValue > 3163 && potValue < 3597)
          type = 4;
        Serial.print(type);
        SerialESP.print(x); // x-Koordinate senden
        SerialESP.print(",");
        SerialESP.print(y); // y-Koordinate senden
        SerialESP.print(",");
        SerialESP.print("t");
        SerialESP.println(type);
        SerialESP.println(".");
        currentState = WAIT_CLOCK_HIGH;
        break;
      }
      digitalWrite(colPin, HIGH);
      delay(100); // Kurze Pause zwischen den Schaltungen
    }
    digitalWrite(rowPin, HIGH);
  }
}
