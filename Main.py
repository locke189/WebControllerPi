'''
Created on Nov 29, 2015

@author: Juan_Insuasti
'''
from flask import Flask, render_template
import datetime
from SerialComms.SerialComms import SerialComms



comm = SerialComms()
app = Flask(__name__)


    
def process_data():
    templateData = {
      'laser' : comm.readLaser(),
      'comm_status' : comm.getState(),
      'temp' : comm.readTemperature(),
      'hum'  : comm.readHumidity()
      }
    return templateData


@app.route("/")
def mainpage():
    return render_template('main.html', **process_data())


@app.route("/laser/")
def laser():
    comm.triggerLaser()
    return render_template('main.html', **process_data())


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=False, use_reloader=False)
