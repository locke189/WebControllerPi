'''
Created on Dec 4, 2015

@author: Juan_Insuasti
'''

from SerialComms.SerialComms import SerialComms


class Leonardo(object):
    '''
    ArduIoT - Leonardo
    This module controls Arduino Leonardo device using ArduIoT firmware.
    Uses the SerialComms class to control serial hardware on rpi device, data
    is transformed in this module so it can be used in various services.
    '''



    def __init__(self, serial, deviceID='A'):
        '''
        Constructor
        The deviceID correspond to the deviceID in the Arduino's firmware.
        serial must be an object of the class SerialComms.
        '''
        
        self.thisDevice = deviceID
        self.serial = serial
        
        #Data declaration
        
        self.arduinoSensorIDs = { "0": 'LASER',
                                  "2": 'TEMPERATURE',
                                  "3": 'HUMIDITY' }
        
        self.arduinoCommands = { 'SUMMARY': "/",
                                 'LASER_TOGGLE': "0",
                                 'LASER_STATUS': "1",
                                 'TEMPERAUTRE_READ': "2",
                                 'HUMIDITY_READ': "3" }
        
        self.arduinoValues  =   { "+" : "ON",
                                  "-" : "OFF"}
        
        
        self.rawData = []
        
        self.componentData = {}
        
    
    
    def getData(self,ID):
        '''
        getData method to get data from sensors/actuators.
        '''
        if ID in self.componentData.keys():
            return self.componentData[ID]
        else:
            return "No DATA"
        
    
    def decode(self):
        '''
        decode()
        Transforms serial data into sensor data in the corresponding dictionary
        '''
        if self.rawData is not None:
            if self.rawData.pop(0) == self.thisDevice:
                for data in self.rawData:
                    if data == chr(0x04): #endoffile
                        return
                    else:
                        sensor = self.arduinoSensorIDs[data[0]]
                        value  = data[1:]
                        if value in self.arduinoValues.keys():
                            self.componentData[sensor] = self.arduinoValues[value]
                        else:
                            self.componentData[sensor] = value

    
    def readDeviceResponse(self):
        '''
        readDeviceResponse()
        Waits for the arduino to send a response. data is stored in the 
        rawData variable.
        '''
        
        self.rawData = self.serial.serialRead()
        self.decode()
        
        if not self.rawData:
            return False
        else:
            print(self.rawData)
            return True
        
        
    def writeDevice(self, command,response=True):
        '''
        readDeviceResponse()
        Waits for the arduino to send a response. data is stored in the 
        rawData variable.
        '''
        if command in self.arduinoCommands.keys():
            data = self.thisDevice + self.arduinoCommands[command]
            self.serial.serialWrite(data)
        else:
            print("Leonardo: Command not found")
            
        if response:
            self.readDeviceResponse()
        
        
    
        
if __name__ == "__main__":
    comm = SerialComms(port='/dev/tty.usbserial-DA01LNZV')
    leo1 = Leonardo(comm,'A')
    leo1.writeDevice("LASER_TOGGLE")
    leo1.startReadThread()
    print(leo1.componentData)
    
            
        