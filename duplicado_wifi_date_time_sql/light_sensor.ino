#include <ESP8266WiFi.h>
#include <NTPClient.h>
#include <WiFiUdp.h>
#include <BH1750.h>
#include <Wire.h>

BH1750 lightMeter;
int i = 0;

// Credenciais da rede Wi-Fi
const char *ssid = "NOWO-A0CC3";
const char *password = "";

// Definir o cliente NTP para obter o horário
WiFiUDP ntpUDP;
NTPClient timeClient(ntpUDP, "pool.ntp.org");

// Deslocamento do fuso horário em segundos (ajustar conforme necessário)
const long utcOffsetInSeconds = 0;

void setup()
{
    Serial.begin(9600);
    Wire.begin();
    lightMeter.begin();

    // Conectar ao Wi-Fi
    Serial.print("Conectando a ");
    Serial.println(ssid);
    WiFi.begin(ssid, password);
    while (WiFi.status() != WL_CONNECTED)
    {
        delay(500);
        Serial.print(".");
    }
    Serial.println("Conectado!");

    // Inicializar o cliente NTP para obter o horário
    timeClient.begin();
    timeClient.setTimeOffset(utcOffsetInSeconds);
}

void loop()
{
    // Atualizar a hora do NTPClient
    timeClient.update();

    // Obter o tempo no formato epoch
    time_t epochTime = timeClient.getEpochTime();

    // Converter o tempo epoch para a estrutura tm
    struct tm *ptm = gmtime((time_t *)&epochTime);

    int year = ptm->tm_year + 1900;
    int month = ptm->tm_mon + 1;
    int day = ptm->tm_mday;
    int hour = ptm->tm_hour;
    int minute = ptm->tm_min;
    int second = ptm->tm_sec;

    char dateTime[20];
    sprintf(dateTime, "%04d-%02d-%02d %02d:%02d:%02d", year, month, day, hour, minute, second);

    float luz = lightMeter.readLightLevel();

    // Exibir a data, hora e nível de luz a cada segundo
    if (i % 3 == 0)
    {
        // Serial.println("Linha duplicada.");
        // Serial.print("i: ");
        Serial.print(i);
        Serial.print("; ");
        // Serial.print(" | Luz: ");
        Serial.print(luz);
        Serial.print("; ");
        // Serial.print(" | DateTime: ");
        Serial.println(dateTime);
    }

    // Serial.print("i: ");
    Serial.print(i);
    Serial.print("; ");
    // Serial.print(" | Luz: ");
    Serial.print(luz);
    Serial.print("; ");
    // Serial.print(" | DateTime: ");
    Serial.println(dateTime);

    delay(1000);
    i++;
}
