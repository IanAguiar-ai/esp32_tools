# esp32_tools
Libraries for micropython using esp32.

## button_hub.py
Class that allows you to use both normal buttons and inverted buttons:

```
from button_hub import Button

door = 5
botton_1 = Botton(door)

if botton_1.value():
  print("Botton is 1")
else:
  print("Botton is 0")
```

## register.py
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

shift_register_and_display
```

## ws2812b_hub.py

## graph_in_ssd1306.py
