import machine


class Counter:
    def increment(self):
        self.count += 1

    def __init__(self, pin, start=0):
        self.count = start
        self.pin = machine.Pin(pin, machine.Pin.IN)
        self.pin.irq(trigger=machine.Pin.IRQ_FALLING, handler=self.increment)



