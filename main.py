import machine
import utime
from machine import Pin
import network
import neopixel

import camera
import micropyserver
import _thread

def hsv_to_rgb(h, s, v):
    # Ensure inputs are within valid ranges
    h = (h % 360) / 360.0
    s = max(0.0, min(s, 1.0))
    v = max(0.0, min(v, 1.0))

    # If S == 0, then it is a shade of gray
    if s == 0.0:
        r = g = b = v
    else:
        i = int(h * 6.)
        f = (h * 6) - i
        p = v * (1. - s)
        q = v * (1. - s * f)
        t = v * (1. - s * (1. - f))

        if i == 0: r, g, b = v, t, p
        elif i == 1: r, g, b = q, v, p
        elif i == 2: r, g, b = p, v, t
        elif i == 3: r, g, b = p, q, v
        elif i == 4: r, g, b = t, p, v
        else:     r, g, b = v, p, q

    return int(r * 255), int(g * 255), int(b * 255)




print("Hello world !\nStarting up the wifi net work !")
# Setting up network access point
ap = network.WLAN(network.WLAN.IF_AP) # create access-point interface
ap.config(ssid='Team4-BP', authmode=network.AUTH_WPA_WPA2_PSK, password=b'sodastream-mitosis')
ap.config(max_clients=10)             # set how many clients can connect to the network
ap.active(True)

print("Starting global objects")
# Init the global objects (camera, sensors, etc)
arducam = camera.Camera(machine.SPI(2, baudrate=8000000, sck=Pin(19), miso=Pin(20), mosi=Pin(21)), Pin(47, Pin.OUT), skip_sleep=False, debug_text_enabled=True)
arducam.startup_routine_3MP()


print("Starting micropyserver")
# Init the http server
server = micropyserver.MicroPyServer(host='0.0.0.0', port=80)

def wp_root(request):
    server.send("Hello world !")
    server.send("sodastream-mitosis")

def get_curr_img(request):
    camera_data = arducam.get_JPG_bytes()
    server.send(camera_data)


server.add_route("/", wp_root)
server.add_route("/img.jpg", get_curr_img)

_thread.start_new_thread(server.start, ())


i = 0
led = neopixel.NeoPixel(Pin(48, Pin.OUT), 1)
while True:
    led[0] = hsv_to_rgb(i, 1.0, 0.25)
    led.write()
    i += 1
    utime.sleep_ms(100)

