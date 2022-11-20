/*
    Created by skeletornb
    skeletornb@gmail.com
    https://github.com/skeletornb
    Copyright (c) 2022 Balazs Nemeth
    Budapest, 2022.11.
*/

// --- ARDUINO UNO --------------------
#define Firmware "1.22.11"                                                  // This is just a sample it can be anything
char sCommand[10] = { '0', '0', '0', '0', '0', '0', '0', '0', '0', '\0' };  // 9pcs useful char and finally an NUL
bool bSerialReady = false;
//--- METHODS LISTING --------------------
void vCommandExecutor(char sCommand);
int iCharToInt(char in);
void cCommandErase();
//--- SETUP --------------------
void setup() {
  Serial.begin(115200);          // BAUD-rate: 115200
  pinMode(LED_BUILTIN, OUTPUT);  // It can be any pin e.g. with MOSFET, relay, SSL relay or 3-phase contactor.
}
//--- MAIN LOOP --------------------
void loop() {
  if (Serial.available()) {
    for (int i = 0; i <= 8; i++) {  // Read 9pcs char
      sCommand[i] = Serial.read();
      delay(2);  // Waiting for UNO's USB-Uart conversion
      if (i == 8) bSerialReady = true;
    }
  }
  if (bSerialReady) {
    vCommandExecutor(sCommand);
    bSerialReady = false;
  }
}
//--- CHAR TO INT CONVERSION --------------------
int iCharToInt(char cIn) {  // If substract '0' ASCII from a number ASCII code we can get the number.
  int iOut;
  iOut = cIn - '0';
  return iOut;
}
//--- EXECUTOR METHOD --------------------
void vCommandExecutor(char sCommand[]) {
  /*
    DESCRIPTION OF COMMANDS:
    ADDxxxyyy : xxx + yyy
    SUBxxxyyy : xxx - yyy
    LEDx      : Builtin LED: x=1 ON, x=0 OFF
    FW        : Firmware query
*/
  int iX;
  int iY;
  // --- MAKING iX --------------------
  iX = iCharToInt(sCommand[3]) * 100;
  iX = iX + (iCharToInt(sCommand[4]) * 10);
  iX = iX + iCharToInt(sCommand[5]);
  // --- MAKING iY --------------------
  iY = iCharToInt(sCommand[6]) * 100;
  iY = iY + (iCharToInt(sCommand[7]) * 10);
  iY = iY + iCharToInt(sCommand[8]);
  // --- COMMAND ADD --------------------
  if (sCommand[0] == 'A' && sCommand[1] == 'D' && sCommand[2] == 'D') {
    Serial.print("Result of addition: ");
    Serial.print(iX + iY);
    Serial.println();
    return;
  }
  // --- COMMAND SUB --------------------
  if (sCommand[0] == 'S' && sCommand[1] == 'U' && sCommand[2] == 'B') {
    Serial.print("Result of substraction: ");
    Serial.print(iX - iY);
    Serial.println();
    return;
  }
  // --- COMMAND LED0 --------------------
  if (sCommand[0] == 'L' && sCommand[1] == 'E' && sCommand[2] == 'D' && sCommand[3] == '0') {
    digitalWrite(LED_BUILTIN, LOW);
    Serial.print("Builtin LED switched OFF");
    return;
  }
  // --- COMMAND LED1 --------------------
  if (sCommand[0] == 'L' && sCommand[1] == 'E' && sCommand[2] == 'D' && sCommand[3] == '1') {
    digitalWrite(LED_BUILTIN, HIGH);
    Serial.print("Builtin LED switched ON");
    return;
  }
  // --- COMMAND FW --------------------
  if (sCommand[0] == 'F' && sCommand[1] == 'W') {
    Serial.println(Firmware);
    return;
  }
  cCommandErase();
}
//--- sCommand ERASER METHOD --------------------
void cCommandErase() {
  for (int i = 0; i <= 8; i++) {
    sCommand[i] = 0;
  }
}