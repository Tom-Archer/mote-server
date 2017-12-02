from colorsys import hsv_to_rgb
from flask import Flask, render_template
import datetime
from mote import Mote
from rainbow_thread import RainbowThread
from cheer_thread import CheerThread
from disco_thread import DiscoThread
from fairy_thread import FairyThread

app = Flask(__name__)
mote = Mote()
mote.configure_channel(1, 16, False)
mote.configure_channel(2, 16, False)
mote.configure_channel(3, 16, False)
mote.configure_channel(4, 16, False)

mote_on = True
current_mode = "Manual"

channel_colors = {}
channel_colors[1] = "FF0000"
channel_colors[2] = "00FF00"
channel_colors[3] = "0000FF"
channel_colors[4] = "FFFFFF"

animation_thread = None

def set_mode(mode):
    global current_mode
    current_mode = mode

def get_mode(error=False):
    if (mote_on):
        if not error:
            return "MoteServer is currently on and in '"+current_mode+"' mode!"
        else:
            return "MoteServer is current on but hit a snag running '"+current_mode+"' :("
    return "MoteServer is currently off :("

def home(error=False):
    templateData = {
      'status' : get_mode(error)
      }
    
    return render_template('home.html', **templateData)

def set_pixel_hex(channel, pixel, hex_string):
    r, g, b = hex_to_rgb(hex_string)
    mote.set_pixel(channel, pixel, r, g, b)

def hex_to_rgb(value):
    return bytearray.fromhex(value)

def mote_off():
    global mote_on
    global animation_thread
    
    if animation_thread != None:
        animation_thread.join()
        animation_thread = None
    
    mote.clear()
    mote.show()
    mote_on = False
    return True

def get_channel_color(channel):
    return channel_colors[channel]

def init_mote(show=True):
    set_mode("Manual")
    for channel in range(1,5):
        r, g, b = hex_to_rgb(channel_colors[channel])
        for pixel in range(16):
            mote.set_pixel(int(channel), pixel, r, g, b)
    if show:
        mote.show()

def run_animation(thread):
    global animation_thread
    exception = False

    try:
        if animation_thread != None:
            animation_thread.join()
            animation_thread = None
        
        if mote_on:
            animation_thread = thread
            animation_thread.start()
            set_mode(animation_thread.name)
    except:
        animation_thread = None
        exception = True
    return home(exception)

@app.route("/")
def root():
    return home();

@app.route("/manual")
def manual():
    return render_template('manual.html')
    
@app.route("/getColor/<channel>/")
def getColor(channel):
    return channel_colors[int(channel)]

@app.route("/setColor/<channel>/<color>")
def setColor(channel, color):
    set_mode("Manual")
    
    if stop_animation():
        # set all channels
        init_mote(False)
    
    response = ""
    try:
        channel_colors[int(channel)] = str(color)
        for pixel in range(16):
            set_pixel_hex(int(channel), pixel, color)
            
        if (mote_on):
            mote.show()
            
        response = "Channel " + str(channel) + "."
    except:
        response = "There was an error setting the color."

    return response

@app.route("/rainbow")
def rainbow():
    return run_animation(RainbowThread(mote))

@app.route("/cheer")
def cheer():
    return run_animation(CheerThread(mote))

@app.route("/disco")
def disco():
    return run_animation(DiscoThread(mote))

@app.route("/fairy")
def fairy():
    return run_animation(FairyThread(mote))

@app.route("/on")
def on():
    global mote_on
    mote_on = True
    init_mote()

    return home()

@app.route("/off")
def off():
    mote_off()

    return home()

if __name__ == "__main__":
    init_mote()
    app.run(host='0.0.0.0', port=80, debug=True)
    # When app terminated:
    mote_off()
        
   
