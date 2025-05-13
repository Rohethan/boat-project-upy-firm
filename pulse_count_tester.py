import config
import utime
from libraries.pulsectr import Counter


def pulse_count_task():
    counter = Counter(config.HALL_LEFT_PIN)

    last_timestamp = utime.ticks_ms()
    utime.sleep_ms(100)
    while 1:
        pulse_count = counter.get_count()
        new_timestamp = utime.ticks_ms()

        counter.reset_count()
        dt = last_timestamp - new_timestamp
        frequency = pulse_count / dt * 1000
        rpm = frequency * 60


        print("RPM :", rpm)

        last_timestamp = new_timestamp
        utime.sleep_ms(1000)