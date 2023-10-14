import gfx #Need this library to run

def normalize_list(y, a, b):
    min_y = min(y)
    max_y = max(y)
    normalized_list = []
    
    for value in y:
        normalized_value = a + ((value - min_y) * (b - a) / (max_y - min_y))
        normalized_list.append(normalized_value)
    
    return normalized_list

class Graph:
    def __init__(self, oled, x:list, y:list, steps = 5, dimensions_visor = (128, 64)):
        self.x_0 = x[0]
        self.x_1 = x[1]
        self.y_0 = y[0]
        self.y_1 = y[1]
        self.oled = oled
        self.steps = steps
        self.len_list = int((self.x_1 - self.x_0 + 1)/steps)
        self.y = [0 for i in range(self.len_list)]
        self.x = [i*self.steps + self.x_0 for i in range(self.len_list)]
        self.graphics = gfx.GFX(*dimensions_visor, oled.pixel) #oled = ssd1306.SSD1306_I2C(oled_width, oled_height, i2c)

    def add(self, value):
        self.values.append(-value)
        if len(self.y) > self.len_list:
            del self.y[0]

    def pass_to_graph(self, fill = False):
        self.graphics.rect(self.x_0, self.y_0, self.x_1-self.x_0, self.y_1-self.y_0, 1)
        self.y_real = normalize_list(self.y, self.y_0, self.y_1)
        for i in range(len(self.x) - 1):
            self.graphics.line(self.x[i], self.y_real[i], self.x[i+1], self.y_real[i+1], 1)
            graphics.circle(self.x[i+1], self.y_real[i+1], max(int(self.steps/3), 7), 1)
        oled.show()
        if fill:
            self.oled.fill(0)
        
            

