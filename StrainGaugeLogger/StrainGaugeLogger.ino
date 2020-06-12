#include "VernierLib.h" 

VernierLib Vernier;
float sensorReading;
long t_start;

const int PIN_LED = 13;
const int PIN_BUTTON = 12;

void setup()
{
  pinMode(PIN_LED, OUTPUT);
  pinMode(PIN_LED, INPUT);
  Serial.begin(9600);
  Vernier.autoID(); // Reads the type of sensor attached
  delay(500);
  digitalWrite(PIN_LED, HIGH);
  Serial.println(Vernier.sensorUnits());
  digitalWrite(PIN_LED, LOW);
  delay(500);
  digitalWrite(PIN_LED, HIGH);
  t_start = millis();
}

void loop()
{
  sensorReading = Vernier.readSensor();
  float t_curr = (millis() - t_start)/1000.0;
  Serial.print(sensorReading);
  Serial.print(' ');
  Serial.println(t_curr);
  delay(5);
}
