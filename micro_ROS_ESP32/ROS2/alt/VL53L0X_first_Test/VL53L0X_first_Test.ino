// Erster Test des Sensors VL53L0X 
// an einem ESP32
// E-Block EB22
// Anschluss (D8-D15 - D-Sub-Pin 7 und 8)
// D22 SCL Gelb
// D21 SDA Grün
// GND  braun
// 3V3 rot
// OJ 2.1.25
// ggf. $ pip install pyserial
//---------------------------------------------------

#include "Adafruit_VL53L0X.h"

Adafruit_VL53L0X lox = Adafruit_VL53L0X();

void setup() {
  Serial.begin(115200);

  // wait until serial port opens for native USB devices
  while (! Serial) {
    delay(1);
  }

  Serial.println("Adafruit VL53L0X test.");
  if (!lox.begin()) {
    Serial.println(F("Failed to boot VL53L0X"));
    while(1);
  }
  // power
  Serial.println(F("VL53L0X API Continuous Ranging example\n\n"));

  // start continuous ranging
  lox.startRangeContinuous();
}

void loop() {
  if (lox.isRangeComplete()) {
    Serial.print("Distance in mm: ");
    Serial.println(lox.readRange());
  }
}
