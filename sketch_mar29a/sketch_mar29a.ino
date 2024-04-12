const int clockPin = 13;
int potValue = 0;
unsigned long previousMillis = 0;
unsigned long interval = 9;
const int potPin = 34;

enum State {
  WAIT_CLOCK_HIGH,
  READ_POT_VALUE
};

State currentState = WAIT_CLOCK_HIGH;

void setup() {
  Serial.begin(115200);
  pinMode(clockPin, OUTPUT);
  digitalWrite(clockPin, LOW); 
}

void loop() {
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
      Serial.println(potValue);
      if (potValue < (680 * 1.10) && potValue > (680 * 0.90)) {
        Serial.println("3.3k");
      } else if (potValue < (2190 * 1.10) && potValue > (2190 * 0.90)) {
        Serial.println("470");
      } else if (potValue < (1580 * 1.10) && potValue > (1580 * 0.90)) {
        Serial.println("1k");
      }
      currentState = WAIT_CLOCK_HIGH;
      digitalWrite(clockPin, LOW);
      break;
  }
}