
'''
Created on Nov 29, 2015

Test: for streaming video

@author: Juan_Insuasti
'''

from flask import Flask, render_template, redirect, Response, send_from_directory
import os
import time
from threading import Thread
from flask.ext.socketio import SocketIO, emit
from Media.Video import Camera



app = Flask(__name__)
socketio = SocketIO(app) #SocketIO


#test

def gen(camera):
    """Video streaming generator function."""
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/video_feed/')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    #return Response(gen(Camera()),
    #                mimetype='multipart/x-mixed-replace; boundary=frame')
	gen(Camera())
	return send_from_directory(os.path.join(app.root_path, 'static'), 'home.jpg',
                           mimetype='image/png')


@app.route("/")
def mainpage():
    return render_template('test.html', **{})

if __name__ == "__main__":
    socketio.run(app, host='0.0.0.0', port=80, debug=False, use_reloader=False)