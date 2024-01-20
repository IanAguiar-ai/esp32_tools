from time import sleep
from machine import Pin, UART
import _thread

class Uart:
    def __init__(self, rx:int = 18, tx:int = 5, logic = None):
        self.rx = rx
        self.tx = tx
        self.logic = logic #funcion
        self.uart = UART(2, 115200, tx=18, rx=5)
        SELF.init(115200, bits = 8, parity = None, stop = 1)

    def run(self):
        def thread_run():
            self.uart.write(">>>")
            while True:
                try:
                    line = self.uart.readline()
                    if line != None:
                        novo = line.decode('utf-8')
                        if novo == "\b" and len(text_full) > 0:
                            text_full = text_full[:-1]
                        text_full = f"{text_full}{novo}"
                        self.uart.write(line.decode('utf-8'))
                    if text_full.find("\r") > -1:
                        self.uart.write(f"\n")
                        self.logic(text_full)
                        text_full = ""
                        self.uart.write("\n>>>")
            
                except Exception as error:
                    uart.write(str(error))
                    print(error)
                    sleep(0.1)

                sleep(0.02)

        _thread.start_new_thread(thread_run,())
