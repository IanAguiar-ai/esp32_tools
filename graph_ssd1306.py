from machine import Pin, I2C
import ssd1306
from time import time, ticks_us, sleep
from random import random

class Graph:
    def __init__(self, display, limits_x:tuple = None, limits_y:tuple = None, dimensions_visor:tuple = (128, 64), parameters = None):
        """
        Starts the display
        """
        #Parameters:
        self.parameters = {"edge":True,
                           "hard":True,
                           "scale":True}
        if parameters != None:
            for parameter in parameters.keys():
                if parameter in self.parameters:
                    self.parameters[parameter] = parameters[parameter]

        #Limits of graph:
        if limits_x == None:
            self.limits_x = [0, dimensions_visor[0]]
        else:
            self.limits_x = limits_x
        if limits_y == None:
            self.limits_y = [0, dimensions_visor[1]]
        else:
            self.limits_y = limits_y
        
        #Visor:
        self.dimension = dimensions_visor #Dimensions of visor
        self.oled = display

        #Memory:
        self.values = [] #List of real values, max len = steps
        self.temporary = [] #List of temporary values
        self.treated = [] #List of values treated
        self.to_draw = [] #List of tuples ready to draw

    def run(self):
        self.oled.fill(0)
        self.make_graph()
        self.draw_graph()
        self.oled.show()

    def add(self, value:float, limit:int = None):
        self.values.append(value)
        if limit != None:
            while len(self.values) > limit:
                self.values.pop(0)

    def normalize(self):
        min_op = min(self.temporary)
        max_op = max(self.temporary) - min_op + 1

        for i in range(len(self.temporary)):
            self.treated[i] = (self.temporary[i] - min_op + 1)/max_op * (self.limits_y[1] - self.limits_y[0] - 1)
            self.treated[i] = (self.temporary[i] - min_op + 1)/max_op * (self.limits_y[1] - self.limits_y[0] - 1)

    def make_graph(self):
        if self.temporary != self.values:
            self.temporary = self.values.copy()
            self.treated = [0 for i in range(len(self.temporary))]
            self.normalize()            

            self.to_draw = []
            diference = (self.limits_x[1] - self.limits_x[0])/(len(self.temporary)-1)

            self.to_draw.append([self.limits_x[0], self.limits_y[1] - self.treated[0]])
            for i in range(1, len(self.temporary)):
                self.to_draw.append([self.limits_x[0] + diference*(i), self.limits_y[1] - self.treated[i] + 1])
                
    def draw_graph(self):
        for i in range(1, len(self.temporary)):
            self.draw_simple(i)

        if self.parameters["edge"]:
            for i in range(self.limits_x[0], self.limits_x[1]):
                self.oled.pixel(i, self.limits_y[0], 1)
                self.oled.pixel(i, self.limits_y[1], 1)

    def draw_simple(self, i):
        variation = (self.to_draw[i][1]-self.to_draw[i-1][1])/(self.to_draw[i][0]-self.to_draw[i-1][0])
        intercept = self.to_draw[i-1][1] - variation * self.to_draw[i-1][0]

        for k in range(int(self.to_draw[i-1][0]), int(self.to_draw[i][0]) + 1, 1):
            self.oled.pixel(k, int(variation*k + intercept), 1)
            if self.parameters["hard"]:
                for k_ in range(min(int(variation*(k) + intercept), int(variation*(k+1) + intercept)), max(int(variation*(k) + intercept), int(variation*(k+1) + intercept))):
                    self.oled.pixel(k, k_, 1)

        if self.parameters["scale"]:
            pass
    
i2c = I2C(0, scl = Pin(22), sda = Pin(21))
oled = ssd1306.SSD1306_I2C(128, 64, i2c)

visor = Graph(display = oled, limits_x = None, limits_y = (30, 64), dimensions_visor = (128, 64))

for i in range(10):
    visor.add(random()*30)

while True:
    visor.add(random(), 10)
    visor.run()
    sleep(1)
    print("print")
