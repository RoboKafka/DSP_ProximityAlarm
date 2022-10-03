#!/usr/bin/python3

import numpy as np

import matplotlib.pyplot as plt
import matplotlib.animation as animation

import webcam2rgb
import iir_filter
from scipy import signal
import time
#import csv


class RealtimePlotWindow:

    def __init__(self, channel: str, set_lim=None):
        # create a plot window
        self.fig, self.ax = plt.subplots()
        plt.title(f"Channel: {channel}")
        # that's our plotbuffer
        self.plotbuffer = np.zeros(500)
        # create an empty line
        self.line, = self.ax.plot(self.plotbuffer)
        self.set_lim = set_lim
        # axis
        if self.set_lim is None:
            self.ax.set_ylim(0, 1)
        else:
            self.ax.set_ylim(self.set_lim)
        # That's our ringbuffer which accumluates the samples
        # It's emptied every time when the plot window below
        # does a repaint
        self.ringbuffer = []
        # add any initialisation code here (filters etc)
        # start the animation
        self.ani = animation.FuncAnimation(self.fig, self.update, interval=100)
        #self.filename = open("results.csv","w")
        #self.csvwriter = csv.writer(self.filename)


    # updates the plot
    def update(self, data):
        # add new data to the buffer
        self.plotbuffer = np.append(self.plotbuffer, self.ringbuffer)
        # only keep the 500 newest ones and discard the old ones
        self.plotbuffer = self.plotbuffer[-500:]
        self.ringbuffer = []
        # set the new 500 points of channel 9
        self.line.set_ydata(self.plotbuffer)
        if self.set_lim is None:
            self.ax.set_ylim(0, max(self.plotbuffer)+1)
        else:
            self.ax.set_ylim(self.set_lim)
        return self.line,

    # appends data to the ringbuffer
    def addData(self, v):
        self.ringbuffer.append(v)


realtimePlotWindowBlue = RealtimePlotWindow("Blue Channel - Raw")
realtimePlotWindowBFil= RealtimePlotWindow("Blue Channel - Filtered")
realtimePlotWindowSampRate = RealtimePlotWindow("Sampling Rate of Acquisition", (0, 100))
#realtimePlotWindowRed = RealtimePlotWindow("Red")


fs = 30
duration = 1/fs   
f1 = 1
sos1 = signal.butter(4, f1/fs*2, 'lowpass', output='sos')


iir1 = iir_filter.IIR_filter(sos1)

#create callback method reading camera and plotting in windows
s = time.time()
#avg, count = 0, 0

def hasData(retval, data):
    global s
    #global avg, count
    e = time.time()
    te = e-s
    #avg *= count
    #avg += 1/te
    #count += 1
    #avg /= count
    # print(np.round(1/te, 3), np.round(avg, 2))
    s = e
    
    #b = data[0]
    #g = data[1]
    r = data[2]
    realtimePlotWindowBlue.addData(r)
    y = iir1.filter(r)
    realtimePlotWindowBFil.addData(y)
    realtimePlotWindowSampRate.addData(1/te)
    #print("Sampling rate of acquisition",1/te)
    
    if (y <25):
        print ('Watch your distance     ')
    elif (40< y <130):
        print('Too close     ')
    else:
        print('Safe distance     ')

#create instances of camera
camera = webcam2rgb.Webcam2rgb()
#start the thread and stop it when we close the plot windows
camera.start(callback = hasData, cameraNumber=0)
print("Camera Sampling Rate(Webcam2RGB).....", camera.cameraFs(), "Hz")
plt.show()

camera.stop()
print('finished')

