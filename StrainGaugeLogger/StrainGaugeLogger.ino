#include "VernierLib.h" 

VernierLib Vernier;
float sensorReading;
long t_start;

void setup()
{
  Serial.begin(9600);
  Vernier.autoID(); // Reads the type of sensor attached
  delay(500);
  Serial.println(Vernier.sensorUnits());
  delay(500);
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
