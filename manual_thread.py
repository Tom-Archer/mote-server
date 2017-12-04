from mote_thread import MoteThread
from colorsys import hsv_to_rgb, rgb_to_hsv

class ManualThread(MoteThread):

    channels_colour = [0,0,0]
    channels_colour_delta = [0,0,0]
    old_channels_colour = [0,1,0]
    transition_step = 50
    transition_time = 1
    
    def __init__(self, mote, channel, old, new):
        self.mote = mote
        MoteThread.__init__(self, name="ManualThread")

        self.channel = channel
        
        r, g, b = bytearray.fromhex(old.lstrip('#'))
        h,s,v = rgb_to_hsv(r,g,b)             
        self.old_channels_colour[0] = h
        self.old_channels_colour[1] = s
        self.old_channels_colour[2] = v

        r, g, b = bytearray.fromhex(new.lstrip('#'))
        h,s,v = rgb_to_hsv(r,g,b)             
        self.channels_colour[0] = h
        self.channels_colour[1] = s
        self.channels_colour[2] = v

        for idx in range(0,3):
            self.channels_colour_delta[idx] = (self.channels_colour[idx] - self.old_channels_colour[idx]) / float(self.transition_step)
        
    def run(self):
        
        #print(channels_colour_rgb)

        if self.old_channels_colour != self.channels_colour:
            # Do the transition
            for step in range(0, self.transition_step):
                for idx in range(0,3):
                    self.old_channels_colour[idx] += self.channels_colour_delta[idx]
                    r,g,b = hsv_to_rgb(self.old_channels_colour[0],
                                       self.old_channels_colour[1],
                                       self.old_channels_colour[2]);
                    for pixel in range(self.mote.get_pixel_count(self.channel)):
                        self.mote.set_pixel(self.channel, pixel, int(r), int(g), int(b))
                    self.mote.show()
                self.wait(self.transition_time / float(self.transition_step))
                
        for idx in range(0,3):
            self.old_channels_colour[idx] = self.channels_colour[idx]


if __name__ == "__main__":
    from mote import Mote
    mote = Mote()
    mote.configure_channel(1, 16, False)
    t = ManualThread(mote, 1, "#FF0000", "0000FF")
    t.run()
