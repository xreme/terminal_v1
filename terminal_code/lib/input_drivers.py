import machine
from machine import Pin
import time
import _thread


# setup the button
button = Pin(18, Pin.IN, Pin.PULL_DOWN)

# setup the beeper
beeper = Pin(2, Pin.OUT)

# setup the rotary encoder
DT_Pin = Pin(4, Pin.IN, Pin.PULL_UP)
CLK_Pin = Pin(5, Pin.IN, Pin.PULL_UP)
SW = Pin(3, Pin.IN, Pin.PULL_UP)
previousValue = 1

class InputDrivers:

    def __init__(self,lock):
        self.input_queue = []
        self.button_queue  = []
        self.input_buffer = []
        self.rotary_button_queue = []
        self.lock = lock
        
    def read_rotary(self):
        global previousValue
        global value
        
        if previousValue != CLK_Pin.value():
            if CLK_Pin.value() == 0:
                if DT_Pin.value() == 0:
                    print("counter-clockwise")
                    self.input_buffer.append('CCW')
                else:
                    print("clockwise")
                    self.input_buffer.append('CW')            
            previousValue = CLK_Pin.value()
            
            
        if SW.value() == 0:       
            print("Rotary Button pressed")
            self.rotary_button_queue.append('R_BTN')
            time.sleep(0.2)
    
    def read_button(self):
        if button.value() == 1:
            print("Button pressed")
            self.button_queue.append('BTN')
            time.sleep(0.2)
    
    def read_inputs(self):
        self.read_rotary()
        self.read_button()

    def clear_queue(self):
        self.input_queue.clear()
        self.input_buffer.clear()
        self.button_queue.clear()
        self.rotary_button_queue.clear()
    
    def buffer_to_queue(self):
        # acquire lock
        # make sure main() is not trying to read actions as more are added in
        self.lock.acquire()
        
        # add in the elements from the buffer onto the queue to be read by main()
        for elem in self.input_buffer:
            self.input_queue.append(elem)
        
        # once all items are in the queue remove them
        self.input_buffer.clear()
        
        # release lock, allow main() to read any new inputs
        self.lock.release()
    
    def input_loop(self):
        time.sleep(1)
        ticks = 0
        
        
        # always loop around
        while True:
            self.read_inputs()
            
            flag = False
            
            # check the amount of times the buttons have been pressed in .3 second intervals
            if ticks >= 30:
                ticks = 0
                
                # indicates button hold (or pressed 4 times)
                if len(self.button_queue) >=10:
                    #stop reading inputs
                    machine.reset()
                
                # indicates a button double press
                if len(self.button_queue) >=2:
                    self.input_buffer.append('BTN_2')
                    beeper.on()
                    flag = True
                
                # indicates a single button press
                elif len(self.button_queue) == 1:
                    self.input_buffer.append('BTN')
                    beeper.on()
                    flag = True
                
                # indicates double rotary button press or hold
                if len(self.rotary_button_queue) >=2:
                    self.input_buffer.append('R_BTN_2')
                
                # indicates single button press
                elif len(self.rotary_button_queue) == 1:
                    self.input_buffer.append('R_BTN')
                    beeper.on()
                    flag = True
                
                # once the buffers have been added to the buffer clear them
                self.button_queue.clear()
                self.rotary_button_queue.clear()
            
            # read inputs every 0.01 seconds
            time.sleep(0.01)

            if(flag):
                beeper.off()
                
            # try to transfer items from the buffer into the queue
            self.buffer_to_queue()
            ticks += 1
