import socket
import threading
from mote_thread import MoteThread

class SlaveThread(MoteThread):
    """ Expects a byte array of the form p,r,g,b
        Where p is the pixel to be set (0-15)
              r,g,b are the color values (0-255) """
    def __init__(self, mote, udp_ip, udp_port):
        self.mote = mote
        self.ip = udp_ip
        self.port = udp_port

        self.sock = socket.socket(socket.AF_INET, # Internet
                            socket.SOCK_DGRAM) # UDP
        self.sock.bind((self.ip, self.port))
        self.sock.setblocking(0)
        MoteThread.__init__(self, name="Disco")

    def run(self):
        while not self.stopped():
            try:
                data, addr = self.sock.recvfrom(1024) # buffer size is 1024 bytes
                count = len(data)
                for index in range(0, count, 4):
                    pixel = data[index]
                    r = data[index+1]
                    g = data[index+2]
                    b = data[index+3]
                    for channel in range(1, 5):
                        self.mote.set_pixel(channel, pixel, r, g, b)
                self.mote.show()
            except:
                pass

if __name__ == "__main__":
    from mote import Mote
    import time
    mote = Mote()
    for channel in range(1,5):
        mote.configure_channel(channel, 16, False)
    t = SlaveThread(mote, 7777)
    t.start()
    time.sleep(60)
    t.join()
