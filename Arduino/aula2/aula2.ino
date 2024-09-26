#include <BH1750.h>
#include <Wire.h>

BH1750 lightMeter;

void setup() {
  Serial.begin(9600);
  Wire.begin();
  lightMeter.begin();
}

void loop() {
    float luz = lightMeter.readLightLevel();
    Serial.println(luz);    
    delay(1000);
}
