#include <BluetoothSerial.h>

// ESP32 Bluetooth MAC address
const char* esp32_bt_address = "xx:xx:xx:xx:xx:xx";

BluetoothSerial SerialBT;

void setup() {
  Serial.begin(115200);
  SerialBT.begin("ESP32");

  // Connect to the Raspberry Pi Zero Bluetooth MAC address
  SerialBT.connect(esp32_bt_address);
}

void loop() {
  if (SerialBT.connected()) {
    // Wait for a request from the Raspberry Pi Zero
    while (SerialBT.available() == 0) {
      delay(10);
    }

    // Read the request
    String request = SerialBT.readStringUntil('\n');
    request.trim();
    Serial.println("Received request: " + request);

    // Process the request
    if (request == "Get data") {
      // Send data to the Raspberry Pi Zero
      String data = "Your message here";
      SerialBT.println(data);
      Serial.println("Sent data: " + data);
    }
  }
}
