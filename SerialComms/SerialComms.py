'''
Created on Nov 29, 2015

@author: Juan_Insuasti
'''

import serial
import time




class SerialComms(object):
    '''
    SerialComms
    Class that encapsulates the communication protocol between
    RaspberryPi and Arduino.
    
    If a Xbee module is to be used, then caution must be taken to 
    match the baud rate of the Xbee to the especified in this module.
    otherwise communication between devices will fail.
    '''    



    def __init__(self, port='/dev/ttyUSB0', baud = 57600, timeout = 2):
        '''
        Constructor,
        Opens serial port in RaspberryPi and gets status
        '''
        
        self.RS = chr(0x1E) #Record Separator
        self.SOH = chr(0x01) #Start of header
        self.EOT = chr(0x04) #End of transmition
        
        
        
        #String
        self.buffer = ''
        self.data = []  
        
        #Initializing Serial Port
        
        try:
            self.link = serial.Serial(port, baud, timeout=1)
            self.status = "ON"
        
            if(not self.link.isOpen()):
                self.link.open()
                self.status = "ON"
            
            print("SERIAL: Comms Open!")
        
        except:
            print("SERIAL: Comm error at creating serial connection")
            self.status = "OFF"
    
            
    def getState(self):
        '''
        getState()
        Gets status from serial port.
        '''
        if( self.link.isOpen() ):
            self.status = "ON"
        else:
            self.status = "OFF"
        
        return self.status
    
    
    def serialRead(self):
        '''
        Serial Read:
        
        Reads serial data until EOT is received, data received is separated using
        RS character.
        
        Structure example:
        
        data = [<data0> , ... , <dataN> , EOT ]
        
        '''
        try:
            self.buffer = self.link.readline()
            self.data   = self.buffer.split( self.RS )
            return self.data
        except:
            print("SERIAL: Read error or timeout")
        
    
    def serialWrite(self, write):
        '''
        Serial write
        
        send 'write' parameter trough serial port.
        
        tx << SOH + write + EOT
        
        '''
        
        try:
            self.link.write(self.SOH + write + self.EOT)
         
        except:
            print("SERIAL: Write error")

    
    
if __name__ == "__main__":
    comm = SerialComms(port='/dev/tty.usbserial-DA01LNZV')
    print(comm.getState())
    comm.serialWrite("A0")
    data = comm.serialRead()
    
    print(data.pop(0))
    print(data)
    for info in data:
        print(info)    
    
    