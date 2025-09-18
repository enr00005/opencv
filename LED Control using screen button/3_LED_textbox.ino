int led1 = 2;
int led2 = 3;
int led3 = 4;

void setup() {
  pinMode(led1, OUTPUT);
  pinMode(led2, OUTPUT);
  pinMode(led3, OUTPUT);
  Serial.begin(9600);
}

void loop() {
  if (Serial.available()) {
    char cmd = Serial.read();
    digitalWrite(led1, LOW);
    digitalWrite(led2, LOW);
    digitalWrite(led3, LOW);

    if (cmd == '1') digitalWrite(led1, HIGH);
    else if (cmd == '2') digitalWrite(led2, HIGH);
    else if (cmd == '3') digitalWrite(led3, HIGH);
  }
}
