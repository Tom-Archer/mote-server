from mote_thread import MoteThread
from colorsys import hsv_to_rgb
import numpy
import random
#from numpy import append, linspace

class FairyThread(MoteThread):
    def __init__(self, mote):
        self.mote = mote
        MoteThread.__init__(self, name="Fairy Lights")
        #self.values = append(linspace(0,1,50), linspace(1,0,50))
        self.max_value = 0.40
        self.min_value = 0.02
        self.values = numpy.random.rand(4, 16)
        self.values = self.values * (self.max_value - self.min_value)
        self.values = self.values + self.min_value
        #print(self.values)
        self.dir = numpy.random.randint(2, size=(4,16))
        
    def set_pixel_hsv(self, channel, pixel, h, s, v):
        r, g, b = [int(x*255) for x in hsv_to_rgb(h,s,v)]
        self.mote.set_pixel(channel,pixel,r,g,b)

    def run(self):
        self.mote.clear()
        while not self.stopped():
            """
            for phase in range(2):
                for value in self.values:
                    for channel in range(4):
                        for pixel in range(phase,16,2):
                            self.set_pixel_hsv(channel+1, pixel, 0.14, 0.75, value)
     
                    self.mote.show()
                    self.wait(0.05)"""

            for channel in range(4):
                for pixel in range(16):
                    value = self.values[channel, pixel]
                    if self.dir[channel, pixel] == 1:
                        value = value + 0.01
                    else:
                        value = value - 0.01

                    if value > self.max_value:
                        value = self.max_value
                        self.dir[channel, pixel] = 0
                    elif value < self.min_value:
                        value = self.min_value
                        self.dir[channel, pixel] = 1
                    self.values[channel, pixel] = value
                    
                    self.set_pixel_hsv(channel+1, pixel, 0.14, 0.9, value)
            self.mote.show()
            self.wait(0.1)
