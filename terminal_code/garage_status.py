import machine
import input_drivers
import connection
import time
import network
import socket
import local_web_socket
from machine import Pin, I2C



class GarageStatus:
    
    def __init__(self, display, leds,beeper, inputs):
        self.rtc = machine.RTC()
        self.lcd = display
        self.leds = leds
        self.inputs = inputs
        self.beeper = beeper
        self.local_socket = local_web_socket.LocalWebSocket()
        self.ai = socket.getaddrinfo("192.168.2.254", 80)
        self.addr = self.ai[0][-1]
        self.connection = self.local_socket.connection
        self.previousVal = None
        self.tick = 0;
    

    def run(self):
       
            
             # Create a socket and make a HTTP request 18 s = socket.socket()
            self.leds[2].on()
            s = socket.socket()
            time.sleep(0.5)
            self.leds[1].on()
            time.sleep(0.5)
            s.connect(self.addr)
            self.leds[0].on()
            
            time.sleep(1)
            
            self.leds[0].off()
            self.leds[1].off()
            self.leds[2].off()
            
            try:
                self.leds[1].on()
                s.send(b"GET /data HTTP/1.0\r\n\r\n")
                time.sleep(1)
                response = str(s.recv(256)).split('"')[-2]
                self.leds[1].off()
                
                if not (self.previousVal == response):
                    self.lcd.clear()
                    self.previousVal == response
                
                    self.lcd.putstr('The Garage is \n'+response)
                    if response == 'CLOSED':
                        self.leds[0].on()
                        time.sleep(0.5)
                        self.leds[0].off()
                        self.leds[2].off()
                    else:
                       self.leds[2].on()
                
                time.sleep(3)
                print(response)
            except:
                return "APP_Clock"
