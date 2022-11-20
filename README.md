# Simple-Python3-Arduino-UART-Communication

This is my first repository. :tada::tada::tada:

It's a simple `Python 3` and `Arduino Uno` communication demo with `Tkinter`, `PySerial`, Uno's `builtin LED`, and tiny command interpreter on Arduino.

I selected Uno because it have builtin LED and it can demonstrate switching without additional stuffs. And it have at home. :sweat_smile: Instead of builtin LED you can use any pin with e.g. MOSFET, relay, SSL relay or 3-phase contactor. It is possible to send command from any serial tools e.g. Arduino IDE serial monitor. If Arduino receive command it will do something and/or transmit response.

## Usage
![Port query and port select](/Connect.png)
![Data entry](/Operation.png)
![On MacOS](/Onmacos.png)
* If you start app before connect Arduino you can query ports.
* The message can be entered directly in the upper large field too.
* Input values can be entered in two lower fields and then "+" or "-" buttons write to command line.
* "FIRMWARE", "LED ON", "LED OFF" are instant commands.


## Installation
Only [PySerial](https://github.com/pyserial/pyserial) need to install.
### Opportunities on Windows:
```
pip install pyserial
pip3 install pyserial
python -m pip install pyserial
python3 -m pip install pyserial
```
### Opportunities on MAC/Linux:
```
sudo pip3 install pyserial
sudo python3 -m pip install pyserial
```

## Serial commands
* ADDxxxyyy	: xxx + yyy
* SUBxxxyyy	: xxx - yyy
* LED0 		  : Builtin LED OFF
* LED1      : Builtin LED ON
* FW 		    : Firmware query

## Arduino C code
```c
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
    vCommandErase();
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
  // --- RESPONSE FOR WRONG COMMAND --------------------
  Serial.println("Wrong command");
}
//--- sCommand ERASER METHOD --------------------
void vCommandErase() {
  for (int i = 0; i <= 8; i++) {
    sCommand[i] = 0;
  }
}
```

## Python 3 code
```python3
import serial
from serial.tools import list_ports
from time import sleep
from tkinter import *

class uart(object):
    def __init__(self, iBAUD):
        self.serial= serial.Serial(baudrate= iBAUD, timeout= 0.2)
        self.lConnected=[]
        self.ports= list_ports.comports()

    def close(self):
        self.serial.close()

    def send(self, message):
        try:
            self.serial.write(message.encode('utf-8'))
        except:
            return "Communication doesn't working"
        else:
            return self.serial.readline().strip()

    def portquery(self):                            # Query connected devices's ports
        self.ports= list_ports.comports()
        for x in range(len(self.lConnected)):        # Emptying lConnected[]
            del(self.lConnected[-1])
        for p in self.ports:                        # Uploading lConnected[]
            self.lConnected.append(p.device)
        return self.lConnected

    def portselect(self, iSel):                      # Portselect & opening port
        self.serial.port = self.lConnected[iSel]
        try:
            self.serial.open()
        except:
            return False
        else:
            sleep(1.8)                              # Waiting for pyserial awaken
            return True

class gui(object):
    def __init__(self, UART):
        self.u=UART
        self.connectedports= self.u.portquery()
        self.puff = "0"
        self.root = Tk()

        self.eConsol = Entry(self.root, width= 55)                                      # Consol entry
        self.eConsol.grid(row= 0, column= 0, columnspan= 3, padx= 5, pady= 5)
        self.bSend= Button(self.root, text= "SEND", width= 5, command= self.send)       # Send button
        self.bSend.grid(row= 0, column= 3, padx= 5, pady= 5)

        self.lFrame= LabelFrame(self.root, text= "TOOLS", padx= 5, pady= 5)             # Tools labelframe
        self.lFrame.grid(row= 1, column= 0, columnspan= 4, padx= 5, pady= 5 )

        self.eEntry1= Entry(self.lFrame, width= 20)                                     # Entry 1
        self.eEntry1.grid(row=1, column=0, padx= 5, pady= 5)
        self.eEntry2= Entry(self.lFrame, width= 20)                                     # Entry 2
        self.eEntry2.grid(row=1, column=1, padx= 5, pady= 5)
        self.bAdd= Button(self.lFrame, text= "+", width= 5, command= self.add)          # Add button
        self.bAdd.grid(row= 1, column= 2, padx= 5, pady= 5)
        self.bSub= Button(self.lFrame, text= "-", width= 5, command= self.sub)          # Substract button
        self.bSub.grid(row= 1, column= 3, padx= 5, pady= 5)
        self.bFW= Button(self.lFrame, text= "FIRMWARE", width= 14, command= self.fw)    # Firmware require button
        self.bFW.grid(row= 2, column= 0, padx= 5, pady= 5)
        self.bLED1= Button(self.lFrame, text= "LED ON", width= 14, command= self.led1 ) # LED ON buttton
        self.bLED1.grid(row= 2, column= 1, padx= 5, pady= 5)
        self.bLED0= Button(self.lFrame, text= "LED OFF", width= 14, command= self.led0 )# LED OFF button
        self.bLED0.grid(row= 2, column= 2, columnspan=2, padx= 5, pady= 5)

        self.root.option_add("*tearoff", FALSE)
        mMenu= Menu(self.root)
        self.root.config(menu=mMenu)
        self.mPorts= Menu(mMenu, tearoff= 0)
        mMenu.add_cascade(label="Ports", menu= self.mPorts)

        self.mPorts.add_command(label= "Port query", command= self.portlistrefresh )
        self.mPorts.add_command(label= "Port close", command= self.portclose )
        self.mPorts.add_separator()
        self.portlistrefresh()

        self.root.mainloop()

    def portlistrefresh(self):
        self.connected= self.u.portquery()
        self.mPorts.delete(3,END)
  
        if (len(self.connected)>=1):
            self.mPorts.add_command(label=self.connected[0], command= lambda: self.portselect(0) )
        if (len(self.connected)>1):
            self.mPorts.add_command(label=self.connected[1], command= lambda: self.portselect(1) )
        if (len(self.connected)>2):
            self.mPorts.add_command(label=self.connected[2], command= lambda: self.portselect(2) )
        if (len(self.connected)>3):
            self.mPorts.add_command(label=self.connected[3], command= lambda: self.portselect(3) )
        if (len(self.connected)>4):
            self.mPorts.add_command(label=self.connected[4], command= lambda: self.portselect(4) )

    def portselect(self, i):
        self.eConsol.delete(0, END)
        self.eConsol.insert(0, "Port opening...")
        if self.u.portselect(i):
            self.eConsol.delete(0, END)
            self.eConsol.insert(0, self.u.serial.port + " port opened")
        else:
            self.eConsol.delete(0, END)
            self.eConsol.insert(0, "Port don't opened")

    def portclose(self):
        self.u.close()
        self.eConsol.delete(0, END)
        self.eConsol.insert(0, "Port closed")

    def send(self):
        self.puff=self.u.send(self.eConsol.get())
        self.eConsol.delete(0, END)
        self.eConsol.insert(0, self.puff)
          
    def add(self):      # add
        self.eConsol.delete(0, END)
        self.eConsol.insert(0, "ADD" + ("000" + self.eEntry1.get())[-3:] + ("000"+self.eEntry2.get())[-3:])

    def sub(self):      # subtract
        self.eConsol.delete(0, END)
        self.eConsol.insert(0, "SUB" + ("000" + self.eEntry1.get())[-3:] + ("000"+self.eEntry2.get())[-3:])

    def led1(self):     # LED switch ON 
        self.eConsol.delete(0, END)
        self.puff= self.u.send("LED1")
        self.eConsol.insert(0, self.puff)

    def led0(self):     # LED switch OFF
        self.eConsol.delete(0, END)
        self.puff= self.u.send("LED0")
        self.eConsol.insert(0, self.puff)

    def fw(self):       # Firmware query
        self.eConsol.delete(0, END)
        self.puff= self.u.send("FW")
        self.eConsol.insert(0, self.puff)

if __name__ == '__main__':
    oUart = uart(115200)
    oGui = gui(oUart)
```
