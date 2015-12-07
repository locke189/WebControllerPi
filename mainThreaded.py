'''
Created on Dec 6, 2015

@author: Juan_Insuasti
'''

'''
Created on Nov 29, 2015

@author: Juan_Insuasti
'''
from flask import Flask, render_template, redirect
from SerialComms.SerialComms import SerialComms
from ArduIoT.Leonardo import Leonardo
import os
import time
from threading import Thread
from flask.ext.socketio import SocketIO, emit



comm = SerialComms(port='/dev/tty.usbserial-DA01LNZV')
leo1 = Leonardo(comm,"A") # serial comms device "A"
app = Flask(__name__)

socketio = SocketIO(app) #SocketIO

def watchSerial():
    '''
    '''
    while True:
        received = leo1.readDeviceResponse()
        if received:
            print("New data!")
            print(leo1.componentData)
            socketio.emit("new_data", leo1.componentData)
        
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

@app.route("/snapshot/")
def snapshot():
    path = os.getcwd()
    fs_string = 'sudo fswebcam -r 640x480 -S 15 --flip h --jpeg 95 --shadow --title "@Juan_Insuasti" --subtitle "Home" --info "Monitor: Active @ 1 fpm" --save ' + path + '/static/home.jpg'
    print(fs_string)
    os.system(fs_string)
    return redirect("/")
    #return render_template('main.html', **process_data())

if __name__ == "__main__":
    t1 = Thread(target=watchSerial)
    t1.start()
    socketio.run(app, host='0.0.0.0', port=80, debug=True, use_reloader=False)