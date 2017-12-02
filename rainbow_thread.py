import time
from mote_thread import MoteThread
from colorsys import hsv_to_rgb

class RainbowThread(MoteThread):
    def __init__(self, mote):
        self.mote = mote
        MoteThread.__init__(self, name="Rainbow")

    def run(self):
        while not self.stopped():
            h = time.time() * 50
            for channel in range(4):
                for pixel in range(16):
                    hue = (h + (channel * 64) + (pixel * 4)) % 360
                    r, g, b = [int(c * 255) for c in hsv_to_rgb(hue/360.0, 1.0, 1.0)]
                    self.mote.set_pixel(channel + 1, pixel, r, g, b)
            self.mote.show()
            self.wait(0.01)

if __name__ == "__main__":
    from mote import Mote

    print("""Rainbow
    Press Ctrl+C to exit.
    """)

    mote = Mote()

    mote.configure_channel(1, 16, False)
    mote.configure_channel(2, 16, False)
    mote.configure_channel(3, 16, False)
    mote.configure_channel(4, 16, False)
    
    testthread = RainbowThread(mote)
    testthread.start()

    time.sleep(5.0)
    testthread.join()
