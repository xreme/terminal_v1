from machine import Pin, I2C
import time
from machine_i2c_lcd import I2cLcd

#setup the  display
i2c = I2C(0, scl=Pin(9), sda=Pin(8), freq=400000)
addresses = i2c.scan()
addr = addresses[0]
lcd = I2cLcd(i2c, addr, 2, 16)

# declare the LEDs
green_led = Pin(21, Pin.OUT)
yellow_led = Pin(20, Pin.OUT)
red_led = Pin(19, Pin.OUT)

# setup the beeper
beeper = Pin(2, Pin.OUT)

# setup the button
button = Pin(18, Pin.IN, Pin.PULL_DOWN)

# setup the rotary encoder
DT_Pin = Pin(4, Pin.IN, Pin.PULL_UP)
CLK_Pin = Pin(5, Pin.IN, Pin.PULL_UP)
SW = Pin(3, Pin.IN, Pin.PULL_UP)

values = [0,0,0,0]
previousValue = 1


class ComponentTest:
    
    def __init__(self, lcd, leds, beeper, input, lock):
        self.display = lcd
        self.leds = leds
        self.input = input
        self.beeper = beeper
        self.lock = lock
        self.tick = 0
        
    def read_input_queue(self):
        self.lock.acquire()
        while len(self.input.input_queue) > 0:
            # clear the input queue
            self.input.input_queue.pop(0)
        self.lock.release()

    def rotary_changed(self):
        
        global previousValue
        global value
        
        if previousValue != CLK_Pin.value():
            if CLK_Pin.value() == 0:
                if DT_Pin.value() == 0:
              
                    values[0] = (values [0]- 1)%20
                    #values[1] = 0
                    values[2] = (values [2]+ 1)%20
                    print("anti-clockwise", values)
                else:
                    values[1] = (values [1]+ 1)%20
                    values[0] = (values[0] + 1)%20
                    #values[2] = 0
                    print("clockwise", values)                
            previousValue = CLK_Pin.value()
             
             
        if SW.value() == 0:       
            print("Button pressed")
            values[3] = (values[3] + 1)%99
            time.sleep(1) 


    def test_leds(self):
        
        # test the individual LEDs
        green_led.on()
        time.sleep(1)
        green_led.toggle()

        yellow_led.on()
        time.sleep(1)
        yellow_led.toggle()

        red_led.on()
        time.sleep(1)
        red_led.toggle()
        
        # test load of all LEDs
        green_led.toggle()
        time.sleep(1)
        
        yellow_led.toggle()
        time.sleep(1)
        
        red_led.toggle()
        time.sleep(1)
        
        red_led.off()
        green_led.off()
        yellow_led.off()
        
    def test_beeper(self):
        beeper.on()
        time.sleep(0.1)
        beeper.off()
        
    def test_screen(self):
        lcd.display_off()
        lcd.backlight_off()
        
        time.sleep(2)
        
        lcd.display_on()
        lcd.backlight_on()
        
        
        test_chars = ['#','A','B','C']
        for char in test_chars:
            lcd.putstr(char*32)
            time.sleep(1)
            lcd.clear()
            
    def test_button(self):
        n = 0
        
        lcd.clear()
        lcd.putstr("Press Button \n" + str(n) + "/3")
        
        while n  < 3:
            if button.value() == 1:
                n +=1
                lcd.clear()
                lcd.putstr("Press Button \n" + str(n) + "/3")
                beeper.on()
                time.sleep(0.1)
                beeper.off()
                time.sleep(0.1)
        
        time.sleep(1)
        lcd.clear()
        
    def test_rotary_encoder(self):
        
        lcd.clear()
        old = values[3]
        lcd.putstr("PRESS ROTARY BUTTON")
        
        while values[3] == old:
            self.rotary_changed()
            time.sleep(0.05)
        
        beeper.on()
        time.sleep(0.1)
        beeper.off()

        
        lcd.clear()
        t = 5

        lcd.putstr("TWIST RIGHT "+ str(t) + " \n   TIMES >>>>>")
        
        old = values[1]
        
        while t > 0 :
            self.rotary_changed()
            
            if old != values[1]:
                t -= 1
                lcd.clear()
                lcd.putstr("TWIST RIGHT "+ str(t) + " \n   TIMES >>>>>")
                old = values[1]
                beeper.on()
                time.sleep(0.1)
                beeper.off()
            time.sleep(0.001)
        
        
        lcd.clear()    
        t = 5

        lcd.putstr("TWIST LEFT "+ str(t) + " \n   TIMES <<<<")
        
        old = values[2]
        
        while t > 0 :
            self.rotary_changed()
            
            if old != values[2]:
                t -= 1
                lcd.clear()
                lcd.putstr("TWIST LEFT "+ str(t) + " \n   TIMES <<<<")
                old = values[2]
                beeper.on()
                time.sleep(0.1)
                beeper.off()
            time.sleep(0.001)
        
     
        
        time.sleep(3)
        
    def run(self):
        lcd.clear()
        lcd.putstr("testing LEDs...")
        self.test_leds()
        lcd.clear()
        
        lcd.putstr("testing lcd...")
        time.sleep(1)
        self.test_screen()
        lcd.clear()
        
        lcd.putstr("testing \n beeper...")
        self.test_beeper()
        lcd.clear()
        
        lcd.putstr("testing \n button")
        time.sleep(1)
        self.test_button()
        lcd.clear()
        
        lcd.putstr("Testing \n Rotary Encoder...")
        time.sleep(1)
        self.test_rotary_encoder()
        
        
        beeper.on()
        time.sleep(0.1)
        beeper.off()
        
        lcd.clear()
        lcd.putstr("TESTS COMPLETE")
        time.sleep(3)
        self.read_input_queue()
        return('APP_')

                                                          