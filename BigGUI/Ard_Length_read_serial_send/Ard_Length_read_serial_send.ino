#include <Wire.h>
#include "Adafruit_VL53L1X.h"

#define IRQ_PIN 2
#define XSHUT_PIN 3

Adafruit_VL53L1X vl53 = Adafruit_VL53L1X(XSHUT_PIN, IRQ_PIN);

// Konstanty pro lankový snímač
const int analogPin = A0; // Analogový pin, ze kterého čteme hodnotu
const int resolution = 16383; // Maximální hodnota při 14-bitovém rozlišení
const float conversionFactor = 1000.0 / resolution; // Převodní faktor pro převod na milivolty
const unsigned long readInterval = 10; // Interval čtení v milisekundách
const int numReadings = 75; // Počet čtení pro průměr

// Proměnné pro průměrování lankového snímače
float lankoReadings[numReadings]; // Pole pro uložení čtení
int lankoReadIndex = 0; // Index aktuálního čtení pro lankový snímač
bool lankoArrayFull = false; // Flag indikující naplnění pole lankového snímače

// Proměnné pro průměrování laserového snímače
int laserReadings[numReadings]; // Pole pro uložení čtení
int laserReadIndex = 0; // Index aktuálního čtení pro laserový snímač
bool laserArrayFull = false; // Flag indikující naplnění pole laserového snímače

// Proměnné pro ukládání hodnot
float lankoValue = 0;
int laserValue = 0; // Hodnota laserového snímače v mm

void setup() {
  Serial.begin(115200);
  while (!Serial) delay(10);

  // Inicializace lankového snímače
  analogReadResolution(14);

  // Inicializace laserového snímače
  Wire.begin();
  if (!vl53.begin(0x29, &Wire)) {
    while (1) delay(10);
  }

  if (!vl53.startRanging()) {
    while (1) delay(10);
  }

  vl53.setTimingBudget(50);

  // Inicializace polí readings na nulu
  for (int i = 0; i < numReadings; i++) {
    lankoReadings[i] = 0;
    laserReadings[i] = 0;
  }
}

void loop() {
  // Čtení lankového snímače
  int sensorValue = analogRead(analogPin);
  float lankoMeasurement = sensorValue * conversionFactor;

  // Uložení nové hodnoty do pole lankového snímače
  lankoReadings[lankoReadIndex] = lankoMeasurement;
  lankoReadIndex = (lankoReadIndex + 1) % numReadings;

  // Pokud je pole plné, vypočítáme průměr bez extrémů pro lankový snímač
  if (lankoReadIndex == 0) {
    lankoArrayFull = true;
  }

  if (lankoArrayFull) {
    float sortedLankoReadings[numReadings];
    memcpy(sortedLankoReadings, lankoReadings, sizeof(lankoReadings));

    // Seřazení hodnot v poli lankového snímače
    for (int i = 0; i < numReadings - 1; i++) {
      for (int j = i + 1; j < numReadings; j++) {
        if (sortedLankoReadings[i] > sortedLankoReadings[j]) {
          float temp = sortedLankoReadings[i];
          sortedLankoReadings[i] = sortedLankoReadings[j];
          sortedLankoReadings[j] = temp;
        }
      }
    }

    // Výpočet průměru bez extrémů pro lankový snímač
    float total = 0;
    for (int i = 1; i < numReadings - 1; i++) {
      total += sortedLankoReadings[i];
    }
    lankoValue = total / (numReadings - 2);
  }

  // Čtení laserového snímače
  if (vl53.dataReady()) {
    int16_t distance = vl53.distance();

    // Uložení nové hodnoty do pole laserového snímače
    laserReadings[laserReadIndex] = distance;
    laserReadIndex = (laserReadIndex + 1) % numReadings;

    // Pokud je pole plné, vypočítáme průměr bez extrémů pro laserový snímač
    if (laserReadIndex == 0) {
      laserArrayFull = true;
    }

    if (laserArrayFull) {
      int sortedLaserReadings[numReadings];
      memcpy(sortedLaserReadings, laserReadings, sizeof(laserReadings));

      // Seřazení hodnot v poli laserového snímače
      for (int i = 0; i < numReadings - 1; i++) {
        for (int j = i + 1; j < numReadings; j++) {
          if (sortedLaserReadings[i] > sortedLaserReadings[j]) {
            int temp = sortedLaserReadings[i];
            sortedLaserReadings[i] = sortedLaserReadings[j];
            sortedLaserReadings[j] = temp;
          }
        }
      }

      // Výpočet průměru bez extrémů pro laserový snímač
      int total = 0;
      for (int i = 1; i < numReadings - 1; i++) {
        total += sortedLaserReadings[i];
      }
      laserValue = total / (numReadings - 2);
    }

    vl53.clearInterrupt();
  }

  // Posílání dat do sériového monitoru
  //Serial.print("Lanko:");
  Serial.print(lankoValue, 1); // Dvě desetinná místa
  //Serial.print(", Laser: ");
  Serial.print(",");
  Serial.print(laserValue); // Hodnota v mm bez desetinných míst
  Serial.println();
  delay(readInterval);
}
