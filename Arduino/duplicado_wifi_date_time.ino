#include <ESP8266WiFi.h>
#include <NTPClient.h>
#include <WiFiUdp.h>
#include <BH1750.h>
#include <Wire.h>

BH1750 lightMeter;
int i = 0;

// Credenciais da rede Wi-Fi
const char *ssid = "turma";
const char *password = "turma1234";

// Definir o cliente NTP para obter o horário
WiFiUDP ntpUDP;
NTPClient timeClient(ntpUDP, "pool.ntp.org");

// Deslocamento do fuso horário em segundos (ajustar conforme necessário)
const long utcOffsetInSeconds = 0;

void setup()
{
    // Inicializar o monitor serial
    Serial.begin(9600);

    // Inicializar o sensor de luz
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

    // Extrair ano, mês, dia, hora, minuto e segundo
    int year = ptm->tm_year + 1900;
    int month = ptm->tm_mon + 1;
    int day = ptm->tm_mday;
    int hour = ptm->tm_hour;
    int minute = ptm->tm_min;
    int second = ptm->tm_sec;

    // Formatar e exibir a data e hora no formato yyyy/mm/dd hh:mm:ss
    char dateTime[20];
    sprintf(dateTime, "%04d/%02d/%02d %02d:%02d:%02d", year, month, day, hour, minute, second);

    // Ler o nível de luz
    float luz = lightMeter.readLightLevel();

    // Exibir a data, hora e nível de luz a cada segundo
    if (i % 3 == 0)
    {
        Serial.println("Linha duplicada.");
        Serial.print("i: ");
        Serial.print(i);
        Serial.print(" | Luz: ");
        Serial.print(luz);
        Serial.print(" | DateTime: ");
        Serial.println(dateTime);
    }

    Serial.print("i: ");
    Serial.print(i);
    Serial.print(" | Luz: ");
    Serial.print(luz);
    Serial.print(" | DateTime: ");
    Serial.println(dateTime);

    delay(1000); // Aguardar 1 segundo antes de atualizar
    i++;
}
