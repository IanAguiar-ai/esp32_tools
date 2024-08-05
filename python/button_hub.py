from machine import Pin

class Button:
    def __init__(self, porta):
        self.real = Pin(porta, Pin.IN)
        if self.real.value() == 0:
            self.normal = True

    def value(self):
        resp = self.real.value()
        if self.normal:
            return resp
        else:
            if resp == 0:
                return 1
            else:
                0
    
