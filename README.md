# esp32_tools
Libraries for micropython using esp32.

**For more details about the libraries enter:**
```
help(name_of_library)
```

## ```button_hub.py```
Class that allows you to use both normal buttons and inverted buttons:

```
from button_hub import Button

door = 5
botton_1 = Botton(door)

if botton_1.value():
  print("Botton is ON")
else:
  print("Botton is OFF")
```

## ```register.py```
Shift Register adaptable for number displays.
It's still in testing, but here's an example:

```
from register import Register

pin_data = 2
pin_clock = 3
pin_latch = 4
shift_register_and_display = Register(pin_data, pin_clock, pin_latch)

# Here how the number is constructed in the display is already defined, but you can still pass a dictionary to define this and put it in the 'number' argument.
#Defalt number:
#self.number = {0:[1,1,1,1,1,1,0],
#                1:[0,0,1,1,0,0,0],
#                2:[1,1,0,1,1,0,1],
#                3:[0,1,1,1,1,0,1],
#                4:[0,0,1,1,0,1,1],
#                5:[0,1,1,0,1,1,1],
#                6:[1,1,1,0,1,1,1],
#                7:[0,0,1,1,1,0,0],
#                8:[1,1,1,1,1,1,1],
#                9:[0,1,1,1,1,1,1]}

shift_register_and_display.put_number(2023)
```

You can still call a timer:
```
from register import Register

pin_data = 2
pin_clock = 3
pin_latch = 4
shift_register_and_display = Register(pin_data, pin_clock, pin_latch)

shift_register_and_display.timer() #Preferably leave this running in a thread
```


## ```ws2812b_hub.py```

### This library allows for easier handling of LED strips using the ```Leds``` class, adding predefined colors and some effects. Additionally, it is possible to assemble an LED display using this library, utilizing the ```Matrix_Leds``` class.

Example ```Leds```:
```
from ws2812b_hub import color, numbers, Leds
 
pin = 5
width = 7*3*5 #7 is the number of 'blocks,' 3 is the number of LEDs per block, and 5 is the number of digits on a board with this strip
my_tape_led = Leds(pin, width)

my_tap_led.add_numbers(numbers, values = "57281") #If the strip is allocated correctly, it will display '57281' on the LEDs
```

Example ```Matrix_Leds```:
```
from ws2812b_hub import color, numbers, Matrix_Leds

#If you assemble a matrix of LEDs from top to bottom like this:
#    >>>>>>>>>>>>>>v
#    v<<<<<<<<<<<<<<
#    >>>>>>>>>>>>>>v
#    v<<<<<<<<<<<<<<
 
pin = 5
width = 30*10 #Width and height of LEDs, Note that in reality, this is a strip with 300 LEDs:
lines = 10
my_led_tv = Matrix_Leds(pin, width, lines)

you_dict = {"C":[[1,1,1,1,1],
                  [1,0,0,0,0],
                  [1,0,0,0,0],
                  [1,0,0,0,0],
                  [1,1,1,1,1]]}

my_led_tv.strings = you_dict #Your dict of characters

my_led_tv.write("ABCDEFGHIJ")
```

## ```graph_ssd1306.py```
Library made to generate time series graphs, example:

```
from machine import Pin, I2C
import ssd1306
from graph_ssd1306 import Graph

from random import random
i2c = I2C(0, scl = Pin(22), sda = Pin(21))
oled = ssd1306.SSD1306_I2C(128, 64, i2c)

visor = Graph(display = oled, limits_x = (5, 90), limits_y = (20, 60), dimensions_visor = (128, 64), parameters = {"limits":False, "last":False})
visor_2 = Graph(display = oled, limits_x = (5, 90), limits_y = (20, 60), dimensions_visor = (128, 64), parameters = {"limits":False, "last":False})

for i in range(10):
    visor.add(random()*30)

last = 200
while True:
    value = random() * 200 + 100
    last = value+random()*30
    visor.add(value, 7)
    visor_2.add(last, 7)

    oled.fill(0)
    visor.make_graph()
    visor.draw_graph()
    visor_2.make_graph()
    visor_2.draw_graph()
    oled.show()

    sleep(0.1)
```

<img src="https://raw.githubusercontent.com/IanAguiar-ai/esp32_tools/main/images/ssd1306_1.PNG">

```
from machine import Pin, I2C
import ssd1306
from graph_ssd1306 import Graph
from time import time, ticks_us, sleep
from random import random

i2c = I2C(0, scl=Pin(22), sda=Pin(21))
oled = ssd1306.SSD1306_I2C(128, 64, i2c)
visor = Graph(display = oled, limits_x = [0, 110], limits_y = (20, 63), dimensions_visor = (128, 64))

tempo_visor = time()
t0 = ticks_us()
tempo_medio = 0
operacoes_loop = 10


precicao_barra = 12
grafico = [int(5 + random() * 30) for i in range(precicao_barra)]
for i in grafico:
    visor.add(i, precicao_barra)

while True:
    if time() - tempo_visor >= 0.5:
        oled.fill(0)
        oled.text(f"{int(tempo_medio)}us", 0, 0)
        oled.text(f"Operacoes: {operacoes_loop}", 0, 10) 
        visor.add(operacoes_loop, precicao_barra)
        visor.make_graph()
        visor.draw_graph()
        oled.show()

        tempo_visor = time()

    if tempo_medio < 4000:
        operacoes_loop += 1
    elif tempo_medio > 4000:
        operacoes_loop -= 1

    for i in range(operacoes_loop):
        k = i

    t1 = ticks_us()
    tempo_medio = (t1-t0)*0.1 + tempo_medio*0.9
    t0 = t1   
```

<img src="https://raw.githubusercontent.com/IanAguiar-ai/esp32_tools/main/images/ssd1306_2.PNG">

## ```wifi_esp32.py```
Library to help connect esp32 to wifi, exemple:

```
def web_page(t):
  html = """<html><head> <title>ESP Web Server</title> <meta name="viewport" content="width=device-width, initial-scale=1">
  <link rel="icon" href="data:,"> <style>html{font-family: Helvetica; display:inline-block; margin: 0px auto; text-align: center;}
  h1{color: #0F3376; padding: 2vh;}p{font-size: 1.5rem;}.button{display: inline-block; background-color: #e7bd3b; border: none; 
  border-radius: 4px; color: white; padding: 16px 40px; text-decoration: none; font-size: 30px; margin: 2px; cursor: pointer;}
  .button2{background-color: #4286f4;}</style></head><body> <h1>ESP Web Server</h1> 
  <p>GPIO state: <strong> """ + str(t) + """ /strong></p><p><a href="/?led=on"><button class="button">ON</button></a></p>
  <p><a href="/?led=off"><button class="button button2">OFF</button></a></p></body></html>"""
  return html
    
def logic(text):
  if text.find("led=on") > -1:
    print(">>> LED IS 1")
  if text.find("led=off") > -1:
    print(">>> LED IS 0")

wifi = Wifi(["net_1", "net_2"], ["pass_1", "pass_2", "pass_3"])
wifi.connect()
ok = wifi.open_web_page(web_page, logic, args_page = {"t":"test"})
```

## ```log.py```
Library to create log:

```
log = Log("log_esp")
log.add("My log!")
log.size()
my_log = log.read()
print(my_log)
```

## ```OTA_esp32.py```
Library to update code!

Full OTA example:

```
from OTA_esp32 import ota

link = 'link_github_raw_code'
ota(link)

...
rest of application
...
```

OTA download and update:

```
from OTA_esp32 import ota

link = 'link_github_raw_code'
ota_donwload(link)
ota_update(link)

...
rest of application
...
```

<img src="https://raw.githubusercontent.com/IanAguiar-ai/esp32_tools/main/images/graph_ota.svg">

## ```VOTA.py```
Library to update code esp to esp!

Example:

```
from VOTA import Vota
ips_esp = ['esp1', 'esp2', 'esp2'] #mac ESPs

point = Vota(ips = ips_esp)
point.information() #SELF MAC

point.update_programs() #If can update
point.viral()
```
