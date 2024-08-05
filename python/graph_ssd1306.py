class Graph:
    def __init__(self, display, limits_x:tuple = None, limits_y:tuple = None, dimensions_visor:tuple = (128, 64), parameters = None):
        """
        Starts the display
        type:
        - time_series
        - boxplot
        - histogram
        """
        #Parameters:
        self.parameters = {"edge":True,
                           "hard":True,
                           "grid":True,
                           "limits_value":False,
                           "limits":True,
                           "last":True,
                           "type":"time_series",
                           "separations_histogram":9}
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
        if self.parameters["limits_value"] != False and (type(self.parameters["limits_value"]) == list or type(self.parameters["limits_value"]) == tuple):
            min_op = self.parameters["limits_value"][0]
            max_op = self.parameters["limits_value"][1] + 1
        else:
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
            diference = (self.limits_x[1] - self.limits_x[0])/max(len(self.temporary)-1, 1)

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
        if self.parameters["limits"]:
            if self.parameters["limits_value"] != False and (type(self.parameters["limits_value"]) == list or type(self.parameters["limits_value"]) == tuple):
                min_ = min(self.values) #self.parameters["limits_value"][0]
                max_ = self.parameters["limits_value"][1] + 1
                if type(min_) == float:
                    min_ = f"{self.parameters["limits_value"][0]:0.1f}"
                else:
                    min_ = int(self.parameters["limits_value"][0])
            else:
                min_ = min(self.values)
                max_ = max(self.values)
                if type(min_) == float:
                    min_ = f"{min_:0.1f}"
                else:
                    min_ = int(min_)
                
            if type(max_) == float:
                max_ = f"{max_:0.1f}"
            else:
                max_ = int(max_)

            self.oled.text(str(min_), self.limits_x[1], self.limits_y[1] - 6)
            self.oled.text(str(max_), self.limits_x[1], self.limits_y[0])
                
        if self.parameters["type"] == "time_series":
            variation = (self.to_draw[i][1]-self.to_draw[i-1][1])/(self.to_draw[i][0]-self.to_draw[i-1][0])
            intercept = self.to_draw[i-1][1] - variation * self.to_draw[i-1][0]

            for k in range(int(self.to_draw[i-1][0]), int(self.to_draw[i][0]) + 1, 1):
                if int(variation*k + intercept) > self.limits_y[0] and int(variation*k + intercept) < self.limits_y[1]:
                    self.oled.pixel(k, int(variation*k + intercept), 1)
                    if self.parameters["hard"]:
                        for k_ in range(min(int(variation*(k) + intercept), int(variation*(k+1) + intercept)), max(int(variation*(k) + intercept), int(variation*(k+1) + intercept))):
                            self.oled.pixel(k, k_, 1)

            if self.parameters["grid"]:
                for line in range(self.limits_y[0], self.limits_y[1], 10):
                    for len_line in range(self.limits_x[0], self.limits_x[1], 1):
                        if len_line % 5 < 2:
                            self.oled.pixel(len_line, line, 1)
            
            if self.parameters["last"]:
                if type(self.values[-1]) == float:
                    final_value = f"{self.values[-1]:0.1f}"
                else:
                    final_value = int(self.values[-1])
                self.oled.text(str(final_value), self.limits_x[1], int((self.limits_y[1]+self.limits_y[0])/2) - 3)
        
        elif self.parameters["type"] == "boxplot":
            def boxplot_values(data):
                sorted_data = sorted(data)

                q1_index = int(len(sorted_data) * 0.25)
                q3_index = int(len(sorted_data) * 0.75)

                lower_limit = sorted_data[q1_index]
                upper_limit = sorted_data[q3_index]

                outliers = [value for value in sorted_data if value < lower_limit or value > upper_limit]

                median = 0
                for i in data:
                    median += i
                median = median/len(data)

                return {'lower_limit': lower_limit,
                        'upper_limit': upper_limit,
                        'outliers': outliers,
                        'median': median}

            temporary = boxplot_values(list(map(lambda x: x[1], self.to_draw)))
            
            for x in range(int(self.limits_x[0]) + 5, int(self.limits_x[1]) - 5):
                if int(temporary["lower_limit"]) > self.limits_y[0] and int(temporary["lower_limit"]) < self.limits_y[1]:
                    self.oled.pixel(x, int(temporary["lower_limit"]), 1)
                if int(temporary["upper_limit"]) > self.limits_y[0] and int(temporary["upper_limit"]) < self.limits_y[1]:
                    self.oled.pixel(x, int(temporary["upper_limit"]), 1)
            for y in range(int(temporary["lower_limit"]), int(temporary["upper_limit"])):
                if y > self.limits_y[0] and y < self.limits_y[1]:
                    self.oled.pixel(int(self.limits_x[0]) + 5, y, 1)
                    self.oled.pixel(int(self.limits_x[1]) - 5, y, 1)
            for y in temporary["outliers"]:
                if y > self.limits_y[0] and y < self.limits_y[1]:
                    for x in range(int((self.limits_x[0] + self.limits_x[1])/2) - 1, int((self.limits_x[0] + self.limits_x[1])/2) + 2):
                        self.oled.pixel(x, int(y), 1)
            for x in range(int((self.limits_x[0] + self.limits_x[1])/2) - 1, int((self.limits_x[0] + self.limits_x[1])/2) + 2):
                self.oled.pixel(x, int(temporary['median']), 1)

        elif self.parameters["type"] == "histogram":
            def count_by_limit(data_list, limits):
                sorted_list = sorted(data_list)

                results = []
                for limit in limits:
                    count = sum(1 for value in sorted_list if value <= limit)

                    results.append([limit, count])

                return results
            
            diference_graph = (self.limits_x[1] - self.limits_x[0])/(self.parameters["separations_histogram"])
            values_x = list(map(lambda x: x[1], self.to_draw))
            min_ = int(min(values_x))
            max_ = int(max(values_x))
            diference = int((max_ - min_)/(self.parameters["separations_histogram"] - 1))
            limits = [i for i in range(min_, max_, diference)]
            temporary = count_by_limit(data_list = values_x, limits = limits)
            value_temporary = list(map(lambda x: x[1], temporary))
            for i in range(len(value_temporary) - 1, 0, -1):
                value_temporary[i] = value_temporary[i] - value_temporary[i-1]

            k = 0
            for value in value_temporary:
                normalize = value/max(value_temporary) * (self.limits_y[1] - self.limits_y[0])
                for y in range(self.limits_y[1] - int(normalize), self.limits_y[1]):
                    self.oled.pixel(int(self.limits_x[0] + k * diference_graph), y, 1)
                    self.oled.pixel(int(self.limits_x[0] + (k+1) * diference_graph)-1, y, 1)
                for x in range(int(self.limits_x[0] + k * diference_graph), int(self.limits_x[0] + (k+1) * diference_graph)):
                    self.oled.pixel(x, self.limits_y[1] - int(normalize), 1)

                k += 1
