import utime
import network

import gps_api
import micropyserver
import _thread
from tinylog import TinyLog
import config as CONFIG

log = TinyLog(CONFIG.LOG_LEVEL)
log.debug("Hello world ! Starting up !")



# ------ GLOBAL OBJECTS INIT ZONE -------
log.info("Initializing global objects")
super_top_secret_thing = ...
gps = gps_api.GPS(tx_pin=CONFIG.NEO6M_TX_PIN, rx_pin=CONFIG.NEO6M_RX_PIN)


# ------ WIFI AP SETUP ZONE
log.info("Starting Wifi AP")
ap = network.WLAN(network.WLAN.IF_AP)
ap.config(ssid=CONFIG.WIFI_SSID, authmode=network.AUTH_WPA_WPA2_PSK, password=CONFIG.WIFI_PASSWORD.encode())
ap.config(max_clients=CONFIG.WIFI_MAX_CLIENTS)
ap.active(True)


# ------ SYSTEM TASKS ZONE
log.info("Starting system tasks")

log.info("Starting http server")
server = micropyserver.MicroPyServer(host='0.0.0.0', port=CONFIG.SERVER_PORT)

def wp_root(request):
    server.send("Hello world !")

def wp_gps(request):
    server.send(gps.get_gps_data_json())

server.add_route("/", wp_root)
server.add_route("/gps", wp_gps)
_thread.start_new_thread(server.start, ())


log.info("Starting main loop")
while True :
    utime.sleep(3)