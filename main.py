import utime
import network

import config
from component_api import motor_api
import _thread
import config as CONFIG
from libraries import mps_utils, micropyserver

print("Hello world ! Starting up !")



# ------ GLOBAL OBJECTS INIT ZONE -------
print("Initializing global objects")
motors = motor_api.Motors()


# ------ WIFI AP SETUP ZONE
print("Starting Wifi AP")
ap = network.WLAN(network.WLAN.IF_AP)
ap.config(ssid=CONFIG.WIFI_SSID, authmode=network.AUTH_WPA_WPA2_PSK, password=CONFIG.WIFI_PASSWORD.encode())
ap.config(max_clients=CONFIG.WIFI_MAX_CLIENTS)
ap.active(True)


# ------ SYSTEM TASKS ZONE
print("Starting system tasks")

print("Starting http server")
server = micropyserver.MicroPyServer(host='0.0.0.0', port=CONFIG.SERVER_PORT)

def wp_root(request):
    server.send("Hello world !")


def wp_set_motors(request):
    params = mps_utils.get_request_query_params(request)
    try :
        l_power = float(params['left'])
        l_power = max(min(l_power, 0), 1)
    except KeyError :
        l_power = 0.0

    try :
        r_power = float(params['right'])
        r_power = max(min(r_power, 0), 1)
    except KeyError :
        r_power = 0.0

    motors.set_motors_power(l_power, r_power)
    server.send("ACK")


server.add_route("/", wp_root)
server.add_route("/set_motors", wp_set_motors)

server.start()