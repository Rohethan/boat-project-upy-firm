from warnings import deprecated

import machine
import utime

global log
import ujson


class GPS:
    def __init__(self, tx_pin, rx_pin, uart_id):
        self.uart = machine.UART(uart_id, tx=tx_pin, rx=rx_pin, baudrate=9600, timeout=2000, parity=None, stop=1)
        self.last_sentence = None

    def _receive_GGA_sentence(self):

        while True:
            uart_raw_line: bytes = self.uart.readline()
            if uart_raw_line[:6] == b'$GPGGA':
                sentence = uart_raw_line
                break

        sentence = sentence[7:-5].decode().split(",")
        if len(sentence) == 15:
            self.utc_time, self.lat, self.lat_dir, self.lon, self.lon_dir, self.fix_time, self.gps_qual, self.num_sats, self.hdop, self.altitude, self.altitude_units, self.geoid_sep, self.geoid_sep_units, self.age_gps_data, self.ref_station_id = sentence
        else :
            log.warn("Invalid GGA sentence length. Position not updated.")


    @deprecated
    def continuous_update_task(self):
        while True:
            self._receive_GGA_sentence()
            utime.sleep_ms(500)


    def get_gps_data_json(self):
        json_data = {
            'gps_lock' : self.gps_qual >= 1,
            'location' : {
                'lat' : f"{self.lat}{self.lat_dir}",
                'lon' : f"{self.lon}{self.lon_dir}"
            },
            'sat_data' : {
                "num_sats" : self.num_sats,
                "gps_time" : self.utc_time,
            }
        }
        return ujson.dumps(json_data)
