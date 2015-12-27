'''
Created on Dec 7, 2015

@author: Juan_Insuasti
'''

import time
import os
from threading import Thread

class  Camera(object):
    '''
    OS capture from camera
    '''

    def __init__(self):

        path = os.getcwd()
        self.fs_string = ('sudo fswebcam -b -q -r 640x480 -S 8 -F 2 --flip h --jpeg 95 --shadow --title "@Juan_Insuasti" --subtitle "Home" --info "Monitor: Active @ 1 fps" --save ' + path + '/static/home.jpg' + ' &')
        print(self.fs_string)
        self.t1 = Thread(target=self.thread)
        self.t1.start()

    def thread(self):
        while True:
            time.sleep(3)
            os.system(self.fs_string)
            #if its been 10 seconds since the last access terminate thread
            #if time.time() - self.last_access > 10:
            #        break

    def get_frame(self):
        self.last_access = time.time()
        path = os.getcwd()
        self.frame = open(path + '/static/home.jpg', 'rb').read()
        return self.frame

if __name__ == "__main__":
    pass
