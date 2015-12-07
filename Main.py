'''
Created on Nov 29, 2015

@author: Juan_Insuasti
'''
from flask import Flask, render_template, redirect
from SerialComms.SerialComms import SerialComms
from ArduIoT.Leonardo import Leonardo
import os
import time


comm = SerialComms()
leo1 = Leonardo(comm,"A") # serial comms device "A"
app = Flask(__name__)


    
def process_data():
    leo1.writeDevice("SUMMARY")
    
    templateData = {
      'laser' : leo1.componentData["LASER"],
      'comm_status' : comm.getState(),
      'temp' : leo1.componentData["TEMPERATURE"],
      'hum'  : leo1.componentData["HUMIDITY"],
      'timestamp'  : time.time()
    }
    return templateData


@app.route("/")
def mainpage():
    return render_template('main.html', **process_data())


@app.route("/laser/")
def laser():
    leo1.writeDevice("LASER_TOGGLE")
    return redirect("/")

@app.route("/snapshot/")
def snapshot():
    path = os.getcwd()
    fs_string = ('sudo fswebcam -r 640x480 -S 15 --flip h --jpeg 95 --shadow --title'
                '"@Juan_Insuasti" --subtitle "Home" --info "Monitor: Active @ 1 fpm"'
                ' --save %s/static/home.jpg' % (path))
    print(fs_string)
    os.system(fs_string)
    return redirect("/")
    #return render_template('main.html', **process_data())

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=False, use_reloader=False)
