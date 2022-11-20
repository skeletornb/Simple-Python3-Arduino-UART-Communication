"""
    Created by skeletornb
    skeletornb@gmail.com
    https://github.com/skeletornb
    Copyright (c) 2022 Balazs Nemeth
    Budapest, 2022.11.
"""

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
            del(self.lConnected[x])
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