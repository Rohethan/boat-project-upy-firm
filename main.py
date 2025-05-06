import utime
import network
import config
from component_api import gps_api, motor_api
import _thread
from libraries.tinylog import TinyLog
import config as CONFIG
from libraries import mps_utils, micropyserver
import esp32

log = TinyLog(CONFIG.LOG_LEVEL)
log.debug("Hello world ! Starting up !")



# ------ GLOBAL OBJECTS INIT ZONE -------
log.info("Initializing global objects")
super_top_secret_thing = ...
gps = gps_api.GPS(tx_pin=CONFIG.NEO6M_TX_PIN, rx_pin=CONFIG.NEO6M_RX_PIN, uart_id=CONFIG.UART_ID_GPS)
propulsion_system = motor_api.PropulsionSystem(config.IN1_PIN, config.IN2_PIN, config.ENA_PIN, config.IN3_PIN,
                                               config.IN4_PIN, config.ENB_PIN, config.HALL_LEFT_PIN,
                                               config.HALL_RIGHT_PIN)



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
    landing_page_file = open("landing_page.html", "r").read()
    server.send(landing_page_file)

def wp_gps(request):
    server.send(gps.get_gps_data_json())

def wp_set_motors(request):
    params = mps_utils.get_request_query_params(request)
    try :
        power = float(params['power'])
    except KeyError :
        power = 0.0

    try :
        turn_ratio = float(params['turn_ratio'])
    except KeyError :
        turn_ratio = 0.5

    propulsion_system.update_thrust_ratios(turn_ratio, power)
    server.send("ACK")

def wp_temp(request):
    server.send(str(esp32.mcu_temperature()))

server.add_route("/", wp_root)
server.add_route("/api/temp", wp_temp)
server.add_route("/api/gps", wp_gps)
server.add_route("api/set_motors", wp_set_motors)




_thread.start_new_thread(server.start, ())
_thread.start_new_thread(propulsion_system.motor_task, ())


log.info("Starting main loop")
while True :
    utime.sleep(3)