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


    def __init__(self, port='/dev/ttyUSB0', baud = 115200):
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
    
    
    def handshake(self,device="A"):
        '''
        Handshake with de selected device
        '''
        #Handshake with device
        self.link.write(device)
        print("<< " + device)
        time.sleep(0.5) 
        
        while self.link.inWaiting() > 0:
            response = self.link.read(self.link.inWaiting())
            print(">> " + response)
        
        if response == device :
            print("Device " + device + " Handshake")
            return True
            
        else:
            print("Device " + device + " Handshake Failed")
            return False
        
        return response
    
    def triggerLaser(self,device="A"):
        '''
        Triggers laser ON/OFF
        '''
        #Handshake with device
        handshake = self.handshake(device)
            
        if handshake :
            response = "@"
            self.link.write("0") #lasser toggle serial command
            
            #checking for successful action
            time.sleep(0.5) 
            while self.link.inWaiting() > 0:
                response = self.link.read(self.link.inWaiting())
                print(">> " + response)
                
            if response == "0":
                response = "@"
                return "Laser On"
            elif response == "1":
                response = "@"
                return "Laser Off"
        
        return "Laser Error"
    
    def readLaser(self,device='A'):
        '''
        reads laset status
        '''
        handshake = self.handshake(device)
            
        if handshake :
            self.link.write("1") #lasser toggle serial command
            response = "";
            #checking for successful action
            time.sleep(0.5) 
            while self.link.inWaiting() > 0:
                response += self.link.read(1)
            
            print(">> Laser: " + response)
            
            if response[0] == '0':
                return "Laser is OFF"
            else:
                return "Laser is ON"
            
        return "Laser Error"
    
    def readTemperature(self,device='A'):
        '''
        reads temperature from M30-DHT11 module
        '''
        handshake = self.handshake(device)
            
        if handshake :
            self.link.write("2") #lasser toggle serial command
            response = "";
            #checking for successful action
            time.sleep(0.5) 
            while self.link.inWaiting() > 0:
                response += self.link.read(self.link.inWaiting())
            
            print(">> Temp: " + response)
                
            return response
            
        return "Temperature Error"
    
    def readHumidity(self,device='A'):
        '''
        reads humidity data from M30-DHT11 module
        '''
        handshake = self.handshake(device)
            
        if handshake :
            self.link.write("3") #lasser toggle serial command
            response = "";
            #checking for successful action
            time.sleep(0.5) 
            while self.link.inWaiting() > 0:
                response += self.link.read(self.link.inWaiting())
            
            print(">> Hum: " + response)
                
            return response
            
        return "Humidity Error"
    
    
    
    
    