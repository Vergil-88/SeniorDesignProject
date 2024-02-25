#include <MPU9250_asukiaaa.h>
MPU9250_asukiaaa mySensor;
float mDirection;
uint16_t mX, mY, mZ;

void setup() {
  Serial.begin(9600);
  Wire.begin();
  mySensor.setWire(&Wire);
  mySensor.beginMag(0x6);
  

}

void loop() {
  auto result = mySensor.magUpdate();
  if (result != 0) {
    mySensor.beginMag();
    result = mySensor.magUpdate();
  }
  mX = mySensor.magX();
  mY = mySensor.magY();
  mZ = mySensor.magZ();
  mDirection = mySensor.magHorizDirection();
  // Do what you want

  Serial.print("X: ");
  Serial.print(mX); // Prints the first variable

  Serial.print("    Y: ");
  Serial.print(mY); // Prints the second variable

  Serial.print("    Z: ");
  Serial.print(mZ); // Prints the third variable

  Serial.print("    Direction: ");
  Serial.print(mDirection); // Prints the third variable

  
  Serial.println("");
  Serial.print(result);
  Serial.println("");
  // Wait for a half second (500 milliseconds)
  delay(500);

}