from machine import Pin, I2C
import time
from machine_i2c_lcd import I2cLcd
import ujson
import real_time_clock
import input_drivers
import machine


class Device:
    def __init__(self):
        # declare the LEDs
        self.green_led = Pin(21, Pin.OUT)
        self.yellow_led = Pin(20, Pin.OUT)
        self.red_led = Pin(19, Pin.OUT)
        self.leds = [self.green_led,self.yellow_led,self.red_led]

        # setupt the display
        self.i2c = I2C(0, scl=Pin(9), sda=Pin(8), freq=400000)
        self.addresses = self.i2c.scan()
        self.addr = self.addresses[0]
        self.lcd = I2cLcd(self.i2c, self.addr, 2, 16)

        # setup the beeper
        self.beeper = Pin(2, Pin.OUT)

        # setup the button
        self.button = Pin(18, Pin.IN, Pin.PULL_DOWN)


    def activate(self, component, t):
        component.on()
        time.sleep(t)
        component.off()

    def display_text(self, text):
        self.lcd.clear()
        self.lcd.putstr(text)
    
    def clear_display(self):
        self.lcd.clear()

    def sleep(self, t):
        time.sleep(t)
