int btn_pin = 8;
int enc_btn_pin = 5;
void setup() {
  pinMode(btn_pin, INPUT_PULLUP);
  pinMode(enc_btn_pin, INPUT_PULLUP);
  Serial.begin(9600);
  randomSeed(analogRead(0));
}
void loop() {
  bool btn = !digitalRead(btn_pin);
  bool pot = !digitalRead(enc_btn_pin);
//  Serial.println(btn);
  if (btn) {
    int randInt = random(50, 1023);
    if (!(randInt > 200 && randInt < 800)) {
      Serial.print("#");
      Serial.print(randInt);
      Serial.print(" ");
      Serial.print(random(300, 700));
      Serial.println("%");
    }
  } else if (pot) {
    int randInt1 = random(80, 1000);
    if (!(randInt1 > 250 && randInt1 < 850)) {
      Serial.print("#");
      Serial.print(random(400, 600));
      Serial.print(" ");
      Serial.print(randInt1);
      Serial.println("%");
    }
  } else if (pot && btn) {
    int randInt = random(50, 1023);
    int randInt1 = random(80, 1000);
    if (!(randInt > 200 && randInt < 800) && !(randInt1 > 250 && randInt1 < 850)) {
      Serial.print("#");
      Serial.print(randInt);
      Serial.print(" ");
      Serial.print(randInt1);
      Serial.println("%");
    }
  } else {
    Serial.print("#");
    Serial.print(random(400, 600));
    Serial.print(" ");
    Serial.print(random(300, 700));
    Serial.println("%");
  }
  delay(20);
}
