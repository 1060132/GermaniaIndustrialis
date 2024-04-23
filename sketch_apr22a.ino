#include <HardwareSerial.h>

const int numRows = 14;
const int numCols = 8;
const int potPin = 34;
const int rowPin = 13;
const int colPin = 12;
unsigned long previousMillis = 0;
unsigned long interval = 9;
int type = 0;
int potPins[] = {
  36,39,34,35,32,33,25,26,27,14,12,13,15,2
};

HardwareSerial SerialESP(1);

void setup() {
  Serial.begin(115200);
  SerialESP.begin(115200);
  pinMode(rowPin, OUTPUT);
  pinMode(colPin, OUTPUT);
  digitalWrite(rowPin, LOW);
  digitalWrite(colPin, LOW);

  while(!SerialESP){
    delay(10);
  }

}

void loop() {

  for(int x = 0; x < 14; x++){
    digitalWrite(rowPin, HIGH);
    for(int y = 0; y < 8; y++){
      digitalWrite(colPin, HIGH);
      int potValue = analogRead(potPins[x]);
      Serial.print(potValue);
      Serial.print(potPins[x]);
        if (potValue > 1861 && potValue < 2295)
            type = 1;
        else if (potValue > 2295 && potValue < 2729)
            type = 2;
        else if (potValue > 2729 && potValue < 3163)
            type = 3;
        else if (potValue > 3163 && potValue < 3597)
            type = 4;
      Serial.print(type);
      digitalWrite(colPin,LOW);
    }
    digitalWrite(rowPin, LOW);
  }


}
