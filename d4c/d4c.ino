
#include <SenseBoxMCU.h>
#include <ArduinoJson.h>

HDC1080 bmp;


typedef struct sensorData {
  char  *name;
  float data;
  //char units[20];
  //char info[20];
  //long timestamp;
} sensorData;


void setup() {
  // initialize digital pin LED_BUILTIN as an output.
  pinMode(LED_BUILTIN, OUTPUT);
  Serial.begin(9600);

  if (!bmp.begin()) {
    Serial.println("Could not find a valid BMP280 sensor, check wiring!");

  }
}

void printJson(sensorData* data) {
  StaticJsonBuffer<200> jsonBuffer;
  JsonObject& root = jsonBuffer.createObject();
  root["name"] = data->name;
  root["data"] = data->data;
  //root["units"] = data.units;
  //root["timestamp"] = data.timestamp;
  root.printTo(Serial);

}

sensorData* makeStruct(char *name, float sensorVal) {
  struct sensorData d;

  d.name = name;
  d.data = sensorVal;

  return &d;
}


void loop() {
  digitalWrite(LED_BUILTIN, HIGH);
  delay(300);
  digitalWrite(LED_BUILTIN, LOW);
  delay(300);

  float  tempBaro = bmp.getTemperature();
  sensorData* data = makeStruct("niggers", 2);
  printJson(data);
  //    pressure = BMP.readPressure()/100;
  //  altitude = BMP.readAltitude(1013.25); //1013.25 = sea level pressure
}
