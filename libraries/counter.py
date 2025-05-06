import machine

class Counter:
    def increment(self, pin):  # Accept the IRQ argument.
        self.count += 1

    def __init__(self, pin, start=0):
        self.count = start
        self.pin = machine.Pin(pin, machine.Pin.IN)
        self.pin.irq(trigger=machine.Pin.IRQ_FALLING, handler=self.increment)