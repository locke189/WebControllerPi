'''
Created on Nov 29, 2015

@author: Juan_Insuasti
'''
from flask import Flask, render_template
import datetime
from SerialComms.SerialComms import SerialComms



comm = SerialComms()
app = Flask(__name__)


    
def process_data(laser = "unknown" ):
    templateData = {
      'laser' : laser,
      'comm_status' : comm.getState()
      }
    return templateData

@app.route("/connect/")
def connect():
    return render_template('main.html', **process_data())


@app.route("/")
def mainpage():
    return render_template('main.html', **process_data())


@app.route("/laser/")
def laser():
    laser_stat = comm.triggerLaser()
    return render_template('main.html', **process_data(laser = laser_stat))


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=False, use_reloader=False)
