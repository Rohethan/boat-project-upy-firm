from machine import Pin

class Counter:
    def irq_handler(self, pin):
        self.count += 1


    def __init__(self, pin_id):
        self.pin = Pin(pin_id, Pin.IN)
        self.pin.init(Pin.IN)
        self.count = 0
        self.pin.irq(trigger=Pin.IRQ_FALLING, handler=self.irq_handler)

    def get_count(self):
        return self.count
    def reset_count(self):
        self.count = 0
