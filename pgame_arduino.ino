void setup() {
  Serial.begin(9600);
}
void loop() {
  Serial.print("#");
  Serial.print(analogRead(A0));
  Serial.print(" ");
  Serial.print(analogRead(A1));
  Serial.println("%");
  delay(50);
}
