'''
Created on Dec 4, 2015

@author: Juan_Insuasti
'''
from DB.DBController import DBController
from SerialComms.SerialComms import SerialComms
import time


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

        self.DB = DBController()

        self.thisDevice = deviceID
        self.serial = serial

        #Data declaration

        self.arduinoSensorIDs = { "0": 'LASER',
                                  "2": 'TEMPERATURE',
                                  "3": 'HUMIDITY',
                                  "4": 'PIR',
                                  "5": 'LIGHT',
                                  "a": 'SERVO'}

        self.arduinoCommands = { 'SUMMARY': "/",
                                 'LASER_TOGGLE': "0",
                                 'LASER_STATUS': "1",
                                 'TEMPERAUTRE_READ': "2",
                                 'HUMIDITY_READ': "3",
                                 'SERVO_STEP_UP': "a",
                                 'SERVO_STEP_DOWN': "b",
                                 'SERVO_SET': "c"}

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

    def time(self):
        time_data = [time.strftime("%Y"),time.strftime("%m"),time.strftime("%d"),time.strftime("%H:%M:%S")]

        return time_data


    def decode(self):
        '''
        decode()
        Transforms serial data into sensor data in the corresponding dictionary
        '''
        if self.rawData:
            if self.rawData.pop(0) == self.thisDevice:
                self.componentData = {}
                for data in self.rawData:
                    if data == chr(0x04) or data[0] == '\x04' : #endoffile
                        self.componentData["Timestamp"] = self.time()
                        return
                    else:
                        if data[0] in self.arduinoSensorIDs.keys():
                            sensor = self.arduinoSensorIDs[data[0]]
                            value  = data[1:]
                            if value in self.arduinoValues.keys():
                                self.componentData[sensor] = self.arduinoValues[value]
                            else:
                                self.componentData[sensor] = value

                self.componentData["Timestamp"] = self.time()


    def readDeviceResponse(self):
        '''
        readDeviceResponse()
        Waits for the arduino to send a response. data is stored in the
        rawData variable.
        '''

        self.rawData = self.serial.serialRead()
        print("len(): ",len(self.rawData))
        if len(self.rawData) > 7:
            print("RDR >>",self.rawData)
            self.decode()
            self.DB.append("SENSOR_DATA",self.componentData)
            return True
        else:
            return False


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



