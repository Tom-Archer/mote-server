import time
import random
from mote_thread import MoteThread
from colorsys import hsv_to_rgb

class DiscoThread(MoteThread):
    def __init__(self, mote):
        self.mote = mote
        MoteThread.__init__(self, name="Disco")

    def run(self):
        while not self.stopped():
            channel = random.randint(1, 4)
            pixel = random.randint(1,16)

            hue = random.randint(0, 360)
            sat = 0.75+(random.random()/4)
            val = 0.75+(random.random()/4)

            r, g, b = [int(c * 255) for c in hsv_to_rgb(hue/360.0, sat, val)]
            self.mote.set_pixel(channel, pixel-1, r, g, b)
            self.mote.show()
            self.wait(random.randint(1,10)/1000.0)

if __name__ == "__main__":
    from mote import Mote

    print("""Disco
    Press Ctrl+C to exit.
    """)

    mote = Mote()

    mote.configure_channel(1, 16, False)
    mote.configure_channel(2, 16, False)
    mote.configure_channel(3, 16, False)
    mote.configure_channel(4, 16, False)
    
    testthread = DiscoThread(mote)
    testthread.start()

    time.sleep(20.0)
    testthread.join()
