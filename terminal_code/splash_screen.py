import machine
import input_drivers
import time


class SplashScreen:
    
    def __init__(self, display, leds,beeper, inputs):
        self.rtc = machine.RTC()
        self.display = display
        self.leds = leds
        self.inputs = inputs
        self.beeper = beeper
    
    def run(self):
        self.display.clear()
        self.display.putstr("Hello Wolld!")
        time.sleep(3)
        self.display.clear()
        self.display.putstr("Terminal V1" + '\n' + "September 2023")
        time.sleep(3)
        self.display.clear()
        self.display.putstr("    Osereme" + '\n' + "    Ibazebo")
        time.sleep(3)
        