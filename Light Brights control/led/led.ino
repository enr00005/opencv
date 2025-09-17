int ledPin = 9;  // PWM pin
int brightness = 0;

void setup() {
  Serial.begin(9600);
  pinMode(ledPin, OUTPUT);
}

void loop() {
  if (Serial.available()) {
    brightness = Serial.parseInt();  // read brightness from Python
    brightness = constrain(brightness, 0, 255);

    if (brightness > 0) {
      analogWrite(ledPin, brightness);  // LED ON with brightness
    } else {
      analogWrite(ledPin, 0);  // LED OFF
    }
  }
}
