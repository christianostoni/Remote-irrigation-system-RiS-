#define sens A0
void setup(){
    pinMode(sens, INPUT);
    Serial.begin(9600);
}
void loop(){
    int val = analogRead(sens);
    Serial.println(val);
    delay(1500);
}