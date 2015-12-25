'''
Created on Dec 6, 2015

@author: Juan_Insuasti
'''


from flask import Flask, render_template, redirect, Response
from SerialComms.SerialComms import SerialComms
from ArduIoT.Leonardo import Leonardo
import os
import time
from threading import Thread
from flask.ext.socketio import SocketIO, emit
from Media.Video import Camera



if os.getlogin() == 'Juan_Insuasti':
    comm = SerialComms(port='/dev/tty.usbserial-DA01LNZV')
else:
    comm = SerialComms()

leo1      = Leonardo(comm,"A") # serial comms device "A"
app       = Flask(__name__)
socketio  = SocketIO(app) #SocketIO



def watchSerial():
    '''
    '''
    while True:
        received = leo1.readDeviceResponse()
        #Data should be loaded from DB not IoT device itself
        if received:
            print("New data!")
            if leo1.componentData:
                print(leo1.componentData)
                socketio.emit("new_data", leo1.componentData, broadcast=True)


def process_data():

    leo1.writeDevice("SUMMARY",False)

    templateData = {
      'laser' : leo1.getData("LASER"),
      'comm_status' : comm.getState(),
      'temp' : leo1.getData("TEMPERATURE"),
      'hum'  : leo1.getData("HUMIDITY"),
      'timestamp'  : time.time()
      }


    return templateData

@socketio.on('laser_toggle')
def laser_toggle(message):
    '''
    Receives a message
    '''
    leo1.writeDevice("LASER_TOGGLE",False)

@app.route("/")
def mainpage():
    return render_template('main_sockets.html', **process_data())


@app.route("/laser/")
def laser():
    leo1.writeDevice("LASER_TOGGLE",False)
    return redirect("/")



if __name__ == "__main__":
    Camera()
    t1 = Thread(target=watchSerial)
    t1.start()
    socketio.run(app, host='0.0.0.0', port=80, debug=False, use_reloader=False, threaded=True)
