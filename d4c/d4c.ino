
#include <SenseBoxMCU.h>

HDC1080 bmp;
void setup() {
  // initialize digital pin LED_BUILTIN as an output.
  pinMode(LED_BUILTIN, OUTPUT);
  Serial.begin(9600);
 
  if (!bmp.begin()) {  
    Serial.println("Could not find a valid BMP280 sensor, check wiring!");

  }
}

void loop() {
  digitalWrite(LED_BUILTIN, HIGH);  
  delay(300); 
  digitalWrite(LED_BUILTIN, LOW);    
  delay(300);                       
  
float  tempBaro = bmp.getTemperature();
Serial.println(tempBaro);
//    pressure = BMP.readPressure()/100;
  //  altitude = BMP.readAltitude(1013.25); //1013.25 = sea level pressure
}
