"""
Class Register
"""
from machine import Pin
from time import sleep_ms as sleep
from time import time as t

class Register:
    """
    Comments:
    You don't need to pass the number of registers in series;
    'number' is a dictionary with the display values;
    This class is made for 8-bit registers.
    """
    def __init__(self, data:int, clock:int, latch:int, time:int = 1, number:dict = False):
        self.data = Pin(data, Pin.OUT, value = 0)
        self.clock = Pin(clock, Pin.OUT, value = 0)
        self.latch = Pin(latch, Pin.OUT, value = 0)

        if not number:
            self.number = {0:[1,1,1,1,1,1,0],
                           1:[0,0,1,1,0,0,0],
                           2:[1,1,0,1,1,0,1],
                           3:[0,1,1,1,1,0,1],
                           4:[0,0,1,1,0,1,1],
                           5:[0,1,1,0,1,1,1],
                           6:[1,1,1,0,1,1,1],
                           7:[0,0,1,1,1,0,0],
                           8:[1,1,1,1,1,1,1],
                           9:[0,1,1,1,1,1,1]}
        else:
            self.number = number

        self.time = time
        self.reset_ = False
        self.connected = None

    def put_number(self, number:int):
        """
        Example:
        reg = Register(data = 3, clock = 4, latch = 5) #Pins
        reg.put_number("010008")
        """
        number = str(number)
        self.connected = len(number)

        d = []
        for i in range(len(number) - 1, 0 - 1, -1):
            d.append(int(number[i]))
            
        for number in d:
            self.put(number)

    def put(self, number:int):
        print(number)
        data.value(0)
        clock.value(1)
        clock.value(0)
        latch.value(1)
        latch.value(0)
        for i in range(7):
            data.value(self.number[int(number)][i])
            clock.value(1)
            clock.value(0)
            latch.value(1)
            latch.value(0)

            sleep(self.time)

    def timer(self, format_ = "{m}{s}{d_s}"):
        """
        If the registers control a timer, activate this function in a thread and leave it running.
        
        m = minutes;
        s = seconds;
        d_s = ten of seconds.
        """
        t0 = t()
        while not self.reset_:
            t_now = t() - t0
            m = int(t_now/60)
            s = int(t_now % 60)
            d_s = int((t_now % 60 - s)*10)
            put_number(format_.format(m = m, s = s, d_s = d_s))
            sleep(30)

    def reset(self):
        if self.reset_ == False:
            self.reset_ = True
            self.put("0" for i in range(8*self.connected))
            sleep(40) # timer_sleep < reset_sleep
            self.reset_ = False
        
            

class Pulse_Button:
    def __init__(self, pin:int):
        self.button = Pin(pin, Pin.IN)

    def press(self):
        b = 0
        if self.button.value() == 1:
            b = 1
            while self.button.value() == 1:
                sleep(10)
        return b

    def value(self):
        return self.button.value()
        
