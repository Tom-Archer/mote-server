import requests
from mote_thread import MoteThread
from colorsys import hsv_to_rgb, rgb_to_hsv

transition_time = 1 # seconds
transition_step = 100

class CheerThread(MoteThread):
    def __init__(self, mote):
        self.mote = mote
        MoteThread.__init__(self, name="CheerLights")

    def run(self):
        channels_colour_rgb = [[0,0,0], [0,0,0], [0,0,0], [0,0,0]]
        channels_colour = [[0,0,0], [0,0,0], [0,0,0], [0,0,0]]
        channels_colour_delta = [[0,0,0], [0,0,0], [0,0,0], [0,0,0]]
        old_channels_colour = [[0,1,0], [0,1,0], [0,1,0], [0,1,0]]
    
        while not self.stopped():
            r = requests.get('http://api.thingspeak.com/channels/1417/feed.json')
            j = r.json()
            f = j['feeds'][-8:]

            f = [element for index, element in enumerate(f) if index%2==0]

            #print(f)

            channel = 1
            for col in f:
                col = col['field2']
                r, g, b = bytearray.fromhex(col.lstrip('#'))
                h,s,v = rgb_to_hsv(r,g,b)
                channels_colour_rgb[channel - 1][0] = r
                channels_colour_rgb[channel - 1][1] = g
                channels_colour_rgb[channel - 1][2] = b
                channels_colour[channel - 1][0] = h
                channels_colour[channel - 1][1] = s
                channels_colour[channel - 1][2] = v
                #calculate the count for each
                for idx in range(0,3):
                    channels_colour_delta[channel - 1][idx] = (channels_colour[channel - 1][idx] - old_channels_colour[channel - 1][idx]) / float(transition_step)
                channel += 1     

            #print(channels_colour_rgb)

            if old_channels_colour != channels_colour:
                # Do the transition
                for step in range(0, transition_step):
                    for channel in range(1, 5):
                        for idx in range(0,3):
                            old_channels_colour[channel - 1][idx] += channels_colour_delta[channel - 1][idx]
                        r,g,b = hsv_to_rgb(old_channels_colour[channel - 1][0],
                                           old_channels_colour[channel - 1][1],
                                           old_channels_colour[channel - 1][2]);
                        for pixel in range(self.mote.get_pixel_count(channel)):
                            self.mote.set_pixel(channel, pixel, int(r), int(g), int(b))
                        self.mote.show()
                    self.wait(transition_time / transition_step)

            for channel in range(0, 4):
                for idx in range(0,3):
                    old_channels_colour[channel][idx] = channels_colour[channel][idx]

            self.wait(10)
