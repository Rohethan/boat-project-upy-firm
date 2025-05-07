from machine import PWM, Pin

import config


class Motors:
    def __init__(self):
        self.ena = PWM(Pin(config.ENA_PIN))
        self.enb = PWM(Pin(config.ENB_PIN))

    def set_motors_power(self, l, r):
        self.ena.duty_u16(int(l*65535))
        self.enb.duty_u16(int(r*65535))
