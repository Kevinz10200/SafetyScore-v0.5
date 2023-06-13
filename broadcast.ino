#include <Wire.h>
#include <SparkFunLSM6DS3.h>
#include <DS3232RTC.h>      // https://github.com/JChristensen/DS3232RTC
#include <BluetoothSerial.h>

#define LSM6DS3_ADDR 0x6B

LSM6DS3 imu;
BluetoothSerial SerialBT;
DS3232RTC myRTC;

// The RTC module is reset at every boot.
// The data processing client would need to
// handle setting a time offset from epoch,
// take note of when the first transmission was
// received, and apply that as an offset.

void printDigits(int digits)
{
    // utility function for digital clock display: prints preceding colon and leading 0
    Serial.print(':');
    if(digits < 10)
        Serial.print('0');
    Serial.print(digits);
}

void setup() {
  Wire.begin();
  Serial.begin(115200);

  myRTC.begin();
  setSyncProvider(myRTC.get);   // Get time from RTC

  Serial.println(" > RTC has set the system time. Time is:");
  Serial.print(hour());
  printDigits(minute());
  printDigits(second());

  Serial.println(" > Initializing serialBT:");
  SerialBT.begin("ESP32"); // Set name

  Serial.println(" > Starting IMU:");
  Serial.println(imu.begin());

  Serial.println(" >>> Setup complete.");
}

void loop() {

  float ax = imu.readFloatAccelX();
  float ay = imu.readFloatAccelY();
  float az = imu.readFloatAccelZ();

  // Prepare the data in CSV format
  String data = String(year()) + "," + String(month()) + "," + String(day()) + "," + String(hour()) + "," + String(minute()) + "," + String(second()) + "," + String(ax, 6) + "," + String(ay, 6) + "," + String(az, 6);

  // Serial.println(data);
  
  if (SerialBT.connected()) {
    Serial.println("---Sending...");\
    Serial.println(data);
    SerialBT.println(data);
    delay(100); // Adjust the delay, set at 10/s
  }
}
