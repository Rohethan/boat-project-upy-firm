import utime
import network
import micropyserver
import _thread
from tinylog import TinyLog
import config as CONFIG

log = TinyLog(CONFIG.LOG_LEVEL)
log.debug("Hello world ! Starting up !")


log.info("Initializing global objects")
supersecret = "sodastream-mitosis"


log.info("Starting Wifi AP")
ap = network.WLAN(network.WLAN.IF_AP)
ap.config(ssid=CONFIG.WIFI_SSID, authmode=network.AUTH_WPA_WPA2_PSK, password=CONFIG.WIFI_PASSWORD.encode())
ap.config(max_clients=CONFIG.WIFI_MAX_CLIENTS)
ap.active(True)


log.info("Starting http server")
server = micropyserver.MicroPyServer(host='0.0.0.0', port=CONFIG.SERVER_PORT)
def wp_root(request):
    server.send("Hello world !")

server.add_route("/", wp_root)
_thread.start_new_thread(server.start, ())


log.info("Starting main loop")
while True :
    utime.sleep(3)