import threading

class MoteThread(threading.Thread):
    def __init__ (self, name='MoteThread'):
        self._sleepperiod = 1.0
        self._stopevent = threading.Event( )
        threading.Thread.__init__(self, name=name)

    def stopped(self):
        return self._stopevent.isSet()

    def wait(self, time=None):
        if time==None:
            time = self._sleepperiod
        self._stopevent.wait(time)
        
    def join(self, timeout=None):
        """ Stop the thread and wait for it to end. """
        self._stopevent.set()
        threading.Thread.join(self, timeout)
