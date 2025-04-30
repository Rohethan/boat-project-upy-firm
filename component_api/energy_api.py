from machine import ADC

import config


class EnergyController:
    def __init__(self, amp_meter_pin, voltage_divider_pin):
        self.voltage_divider_adc = ADC(voltage_divider_pin, ADC.ATTN_11DB) # MAX MEASURE VOLTAGE 2.45V !!
        self.voltage_divider_adc.width(ADC.WIDTH_12BIT)

        self.amp_meter_adc = ADC(amp_meter_pin, ADC.ATTN_11DB)
        self.amp_meter_adc.width(ADC.WIDTH_12BIT)

        self.used_mah_counter = 0


    def measure_voltage(self):
         return self.voltage_divider_adc.read() / 4095 * config.BATTERY_MAX_VOLTAGE

    def measure_amperage(self):
        return self.amp_meter_adc.read() / 4095 * 2.45 * config.ADC_VOLT_PER_AMP