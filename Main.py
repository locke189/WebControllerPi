'''
Created on Nov 29, 2015

@author: Juan_Insuasti
'''
from flask import Flask, render_template
from SerialComms.SerialComms import SerialComms
import os
import time


comm = SerialComms()
app = Flask(__name__)


    
def process_data():
    templateData = {
      'laser' : comm.readLaser(),
      'comm_status' : comm.getState(),
      'temp' : comm.readTemperature(),
      'hum'  : comm.readHumidity(),
      'timestamp'  : time.time()
      }
    return templateData


@app.route("/")
def mainpage():
    return render_template('main.html', **process_data())


@app.route("/laser/")
def laser():
    comm.triggerLaser()
    return render_template('main.html', **process_data())

@app.route("/snapshot/")
def snapshot():
    path = os.getcwd()
    fs_string = 'sudo fswebcam -r 640x480 -S 15 --flip h --jpeg 95 --shadow --title "@Juan_Insuasti" --subtitle "Home" --info "Monitor: Active @ 1 fpm" --save ' + path + '/static/home.jpg'
    print(fs_string)
    os.system(fs_string)
    return render_template('main.html', **process_data())

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=False, use_reloader=False)
