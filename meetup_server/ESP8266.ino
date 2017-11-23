#include <ESP8266WiFi.h>
#include <SPI.h>
#include <MFRC522.h>

/*
RST     = GPIO4
SDA     = GPIO5
MOSI    = GPIO13
MISO    = GPIO12
SCK     = GPIO14
GND     = GND
3.3V    = 3.3V
*/

#define RST 4
#define SDA 5
#define BUZZER 2
#define LED 0

const char *id = "id";
const char *pass = "pw";
const char *IP = "ip";

MFRC522 mfrc522(SDA, RST);
WiFiClient client;

void sparkle(){
  digitalWrite(LED, HIGH);
  digitalWrite(BUZZER, HIGH);
  delay(300);
  digitalWrite(LED, LOW);
  digitalWrite(BUZZER, LOW);

}

void setup() {
  pinMode(LED, OUTPUT);
  pinMode(BUZZER, OUTPUT);
  Serial.begin(9600);
  SPI.begin();
  mfrc522.PCD_Init();

  WiFi.begin(id, pass);
  while ((WiFi.status() != WL_CONNECTED))
      delay(300);

  sparkle();
  Serial.println(F("Setup Done!"));
}

void loop() {
    if (mfrc522.PICC_IsNewCardPresent() && mfrc522.PICC_ReadCardSerial()) {
        String uid = "";
        for (byte i=0; i<mfrc522.uid.size; i++){
            String unit = String(mfrc522.uid.uidByte[i],HEX);
            if (unit.length() < 2)
              unit = "0" + unit;
            uid+=unit;
        }
        Serial.println(uid);
        while (!client.connect(IP,5000))
            delay(10);
        client.print("uid_artir;"+uid);
        client.stop();
        sparkle();
        digitalWrite(BUZZER, LOW);
    }
}
