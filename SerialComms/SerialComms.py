'''
Created on Nov 29, 2015

@author: Juan_Insuasti
'''

import serial
import time
import os
from threading import Thread

def watchSerial():
    '''
    '''
    while True:
        received = comm.serialRead()
        print "<<" , received


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



    if os.getlogin() == 'Juan_Insuasti':
        comm = SerialComms(port='/dev/tty.usbserial-DA01LNZV')
    else:
        comm = SerialComms()

    print 'Enter your commands below.\r\nInsert "exit" to leave the application.'

    t1 = Thread(target=watchSerial)
    t1.start()

    input=1
    while 1 :
        # get keyboard input
        input = raw_input(">> ")
            # Python 3 users
            # input = input(">> ")
        if input == 'exit':
            comm.link.close()
            exit()
        else:
            # send the character to the device
            # (note that I happend a \r\n carriage return and line feed to the characters - this is requested by my device)
            comm.serialWrite(input)
            out = ''
            # let's wait one second before reading output (let's give device time to answer)
            time.sleep(0.1)
            out = comm.serialRead()

            if out != '':
                print ">>",out



