from mote_thread import MoteThread
from colorsys import hsv_to_rgb, rgb_to_hsv

class TransitionClass():
    def __init__(self, channel, new_color):
        self.channel = channel
        self.color = new_color

class ManualThread(MoteThread):
    """ Allows manual setting of Mote stick colors with a soft fade between colors.
        Fading can be interrupted by setting a new color during a running fade.
          It will then transition from the current color to the new color."""
    max_transition_steps = 100
    max_transition_time = 2

    channels_colour_delta = [[0,0,0], [0,0,0], [0,0,0], [0,0,0]]
    channels_colour = [[0,1,0], [0,1,0], [0,1,0], [0,1,0]]
    channels_steps = [0,0,0,0]
    
    def __init__(self, mote, queue):
        self.mote = mote
        self.queue = queue
        
        MoteThread.__init__(self, name="Manual")

    def run(self):

        while not self.stopped():
            try:
                transition = self.queue.get(False)

                r, g, b = bytearray.fromhex(transition.color.lstrip('#'))
                h,s,v = rgb_to_hsv(r,g,b)             

                # Find the shortest transition
                delta_h = (h - self.channels_colour[transition.channel -1][0])
                
                if delta_h > 0.5:
                    delta_h = -1 + delta_h
                elif delta_h < -0.5:
                    delta_h =  1 + delta_h
   
                # Animation steps depend on the total hue change
                steps = int(self.max_transition_steps * delta_h)
                if steps == 0:
                    steps = 1
                elif steps < 0:
                    steps = steps * -1

                self.channels_steps[transition.channel -1] = steps
                self.channels_colour_delta[transition.channel -1][0] = delta_h/float(steps)
                self.channels_colour_delta[transition.channel -1][1] = (s - self.channels_colour[transition.channel -1][1])/float(steps)
                self.channels_colour_delta[transition.channel -1][2] = (v - self.channels_colour[transition.channel -1][2])/float(steps)
            except:
                pass

            # Continue running animation
            for channel in range(1,5):
                if self.channels_steps[channel - 1] > 0:
                    
                    # Apply delta
                    for idx in range(0,3):
                        self.channels_colour[channel - 1][idx] += self.channels_colour_delta[channel - 1][idx]
                        
                    # Protect against out of range
                    if self.channels_colour[channel - 1][0] > 1.0:
                        self.channels_colour[channel - 1][0] = self.channels_colour[channel - 1][0] - 1.0
                    elif self.channels_colour[channel - 1][0] < 0.0:
                        self.channels_colour[channel - 1][0] = 1.0 + self.channels_colour[channel - 1][0]
                    
                    # Reduce remaining steps
                    self.channels_steps[channel - 1] = self.channels_steps[channel -1] - 1
                    
                    # Set pixel
                    r,g,b = hsv_to_rgb(self.channels_colour[channel -1][0],
                                       self.channels_colour[channel -1][1],
                                       self.channels_colour[channel -1][2]);
                    for pixel in range(self.mote.get_pixel_count(channel)):
                        self.mote.set_pixel(channel, pixel, int(r), int(g), int(b))
                        
            self.mote.show()   
            self.wait(self.max_transition_time / float(self.max_transition_steps))


if __name__ == "__main__":
    from mote import Mote
    import time
    from queue import Queue
    mote = Mote()
    mote.configure_channel(1, 16, False)
    queue = Queue()
    t = ManualThread(mote, queue)
    t.start()
    time.sleep(5)
    queue.put(TransitionClass(1, "0000FF"))
    time.sleep(1)
    queue.put(TransitionClass(1, "00FF00"))
    time.sleep(0.5)
    queue.put(TransitionClass(1, "FF0000"))
    time.sleep(5)
    t.join()
    
