'''
Created on Nov 29, 2015

@author: Juan_Insuasti
'''

import serial
import time




class SerialComms(object):
    '''
    classdocs
    '''


    def __init__(self, port='/dev/ttyUSB0', baud = 9600):
        '''
        Constructor
        '''
        try:
            self.link = serial.Serial(port, baud)
            self.status = "ON"
        
            if(not self.link.isOpen()):
                self.link.open()
                self.status = "ON"
            
            print("Serial Comms Open!")
        
        except:
            print("Comm error at creating serial connection")
            self.status = "OFF"
            
    def getState(self):
        '''
        returns connection status
        '''
        return self.status
    
    
    def triggerLaser(self,device="A"):
        '''
        Triggers laser ON/OFF
        '''
        #Handshake with device
        self.link.write(device)
        print("<< " + device)
        time.sleep(1) 
        
        while self.link.inWaiting() > 0:
            response = self.link.read(1)
            print(">> " + response)
            
        if response == device :
            response = "@"
            print("Device " + device + " Handshake")
            self.link.write("0") #lasser toggle serial command
            
            #checking for successful action
            time.sleep(1) 
            while self.link.inWaiting() > 0:
                response = self.link.read(1)
                print(">> " + response)
                
            if response == "0":
                response = "@"
                return "Laser On"
            elif response == "1":
                response = "@"
                return "Laser Off"
        
        return "Laser Error"
    