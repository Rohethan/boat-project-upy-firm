import utime
import network

import config
import pulse_count_tester
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
    web_page = open("mainpage.html", "r")
    server.send(web_page.read())


def wp_set_motors(request):
    params = mps_utils.get_request_query_params(request)
    try :
        l_power = float(params['left'])/100
    except KeyError :
        l_power = 0.0

    try :
        r_power = float(params['right'])/100
    except KeyError :
        r_power = 0.0

    motors.set_motors_power(l_power, r_power)
    print("new motor power received", l_power, r_power)
    server.send("ACK")


server.add_route("/", wp_root)
server.add_route("/set_motors", wp_set_motors)

_thread.start_new_thread(pulse_count_tester.pulse_count_task, ())
server.start()