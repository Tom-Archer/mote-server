import requests
from mote_thread import MoteThread
from colorsys import hsv_to_rgb

class CheerThread(MoteThread):
    def __init__(self, mote):
        self.mote = mote
        MoteThread.__init__(self, name="CheerThread")

    def run(self):
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
                for pixel in range(self.mote.get_pixel_count(channel)):
                    self.mote.set_pixel(channel, pixel, r, g, b)
                channel += 1        

            self.mote.show()

            self.wait(10)
