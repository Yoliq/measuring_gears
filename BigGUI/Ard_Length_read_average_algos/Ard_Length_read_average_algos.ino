
#include <Wire.h>
#include "Adafruit_VL53L1X.h"

#define IRQ_PIN 2
#define XSHUT_PIN 3

Adafruit_VL53L1X vl53 = Adafruit_VL53L1X(XSHUT_PIN, IRQ_PIN);

// Konstanty pro lankový snímač
const int analogPin = A0; // Analogový pin, ze kterého čteme hodnotu
const int resolution = 16383; // Maximální hodnota při 14-bitovém rozlišení
const float conversionFactor = 1000.0 / resolution; // Převodní faktor pro převod na milivolty
const unsigned long readInterval = 50; // Interval čtení v milisekundách

// Proměnné pro Kalmanův filtr lankového snímače
float Q = 0.001; // Process noise covariance (nižší pro stabilitu)
float R = 10; // Measurement noise covariance (vyšší pro redukci šumu)
float P = 10; // Estimation error covariance (vyšší pro rychlou inicializaci)
float K; // Kalman gain (vypočítává se dynamicky)
float X = 0; // Hodnota (odhadovaná)

// Proměnné pro ukládání hodnot
float lankoValue = 0;
int16_t laserValue = 0;

void setup() {
  Serial.begin(115200);
  while (!Serial) delay(10);

  // Inicializace lankového snímače
  analogReadResolution(14);

  // Inicializace laserového snímače
  Wire.begin();
  if (! vl53.begin(0x29, &Wire)) {
    while (1) delay(10);
  }

  if (! vl53.startRanging()) {
    while (1) delay(10);
  }

  vl53.setTimingBudget(50);
}

void loop() {
  // Čtení lankového snímače
  int sensorValue = analogRead(analogPin);
  float measurement = sensorValue * conversionFactor;

  // Kalmanův filtr
  P = P + Q; // Aktualizace chyby odhadu
  K = P / (P + R); // Výpočet Kalmanova zisku
  X = X + K * (measurement - X); // Aktualizace odhadu
  P = (1 - K) * P; // Aktualizace chyby odhadu

  lankoValue = X;

  // Čtení laserového snímače
  if (vl53.dataReady()) {
    int16_t distance = vl53.distance();
    if (distance != -1) {
      laserValue = distance;
      vl53.clearInterrupt();
    }
  }

  // Posílání dat do sériového monitoru
  Serial.print("Lanko:");
  Serial.print(lankoValue, 2); // Dvě desetinná místa
  Serial.print(",Laser:");
  Serial.println(laserValue);

  delay(readInterval);
}


/*
//EMA
// Definování konstant
const int analogPin = A0; // Analogový pin, ze kterého čteme hodnotu
const int resolution = 16383; // Maximální hodnota při 14-bitovém rozlišení
const float conversionFactor = 1000.0 / resolution; // Převodní faktor pro převod na milivolty
const unsigned long readInterval = 50; // Interval čtení v milisekundách
const float alpha = 0.1; // Váha pro exponenciální klouzavý průměr (0 < alpha <= 1)

// Proměnné pro exponenciální klouzavý průměr
float emaValue = 0;
bool firstRead = true;

// Funkce setup() se spustí jednou po resetu
void setup() {
  // Inicializace sériové komunikace s rychlostí 115200 baudů
  Serial.begin(115200);
  // Nastavení rozlišení analogového čtení na 14 bitů
  analogReadResolution(14);
}

// Funkce loop() běží stále dokola
void loop() {
  // Čtení nové hodnoty z analogového pinu
  int sensorValue = analogRead(analogPin);
  // Převod hodnoty na milivolty
  float converted = sensorValue * conversionFactor;

  // Pokud je to první čtení, inicializujeme emaValue
  if (firstRead) {
    emaValue = converted;
    firstRead = false;
  } else {
    // Výpočet exponenciálního klouzavého průměru
    emaValue = alpha * converted + (1 - alpha) * emaValue;
  }
  Serial.print(converted);
  Serial.print(",");
  // Vytisknutí EMA hodnoty do sériového monitoru
  Serial.println(emaValue);
  // Zpoždění mezi čteními pro stabilitu
  delay(readInterval);
}
*/
/*
// Definování konstant
const int lanko_Pin = A0; // Analogový pin, ze kterého čteme hodnotu
const int resolution = 16383; // Maximální hodnota při 14-bitovém rozlišení
const float conversionFactor = 1000.0 / resolution; // Převodní faktor pro převod na milivolty
const unsigned long readInterval = 50; // Interval čtení v milisekundách
const int numReadings = 75; // Počet čtení pro klouzavý průměr

// Proměnné pro klouzavý průměr
float readings[numReadings]; // Pole pro uložení čtení
int readIndex = 0; // Index aktuálního čtení
bool arrayFull = false; // Flag indikující naplnění pole

void setup() {
  Serial.begin(115200); // Inicializace sériové komunikace s rychlostí 115200 baudů
  analogReadResolution(14); // Nastavení rozlišení analogového čtení na 14 bitů
  // Inicializace pole readings na nulu
  for (int i = 0; i < numReadings; i++) {
    readings[i] = 0;}
}

void loop() {
  // Čtení nové hodnoty z analogového pinu
  int sensorValue = analogRead(lanko_Pin);
  // Převod hodnoty na milivolty
  float converted = sensorValue * conversionFactor;
  // Uložení nové hodnoty do pole
  readings[readIndex] = converted;
  // Posun indexu na další pozici v poli
  readIndex = readIndex + 1;
  // Pokud jsme na konci pole, začneme od začátku a nastavíme flag
  if (readIndex >= numReadings) {
    readIndex = 0;
    arrayFull = true;
  }
  // Pokud pole není plné, nebudeme ještě počítat průměr
  if (!arrayFull && readIndex != 0) {
    return;
  }

  // Kopírování pole pro řazení
  float sortedReadings[numReadings];
  memcpy(sortedReadings, readings, sizeof(readings));
  // Seřazení hodnot v poli
  for (int i = 0; i < numReadings - 1; i++) {
    for (int j = i + 1; j < numReadings; j++) {
      if (sortedReadings[i] > sortedReadings[j]) {
        float temp = sortedReadings[i];
        sortedReadings[i] = sortedReadings[j];
        sortedReadings[j] = temp;
      }
    }
  }

  // Výpočet průměru bez extrémů (odečtení první a poslední hodnoty)
  float total = 0;
  for (int i = 1; i < numReadings - 1; i++) {
    total += sortedReadings[i];
  }
  float average = total / (numReadings - 2);

  // Vytisknutí průměrné hodnoty do sériového monitoru
  Serial.print(converted);
  Serial.print(",");
  Serial.println(average);
  // Zpoždění mezi čteními pro stabilitu
  delay(readInterval);
}*/