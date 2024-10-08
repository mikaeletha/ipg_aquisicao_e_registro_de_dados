#include <BH1750.h>
#include <Wire.h>

BH1750 lightMeter;
int i = 0;

void setup()
{
    Serial.begin(9600);
    Wire.begin();
    lightMeter.begin();
}

void loop()
{
    float luz = lightMeter.readLightLevel();

    if (i % 3 == 0)
    {
        Serial.print("i: ");
        Serial.print(i);
        Serial.print(" | Luz: ");
        Serial.println(luz);
    }

    Serial.print("i: ");
    Serial.print(i);
    Serial.print(" | Luz: ");
    Serial.println(luz);

    delay(1000);
    i++;
}
