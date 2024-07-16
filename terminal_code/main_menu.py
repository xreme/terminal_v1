import machine
import input_drivers
import connection
import time


class MainMenu:
    
    def __init__(self, display, leds,beeper, input,lock):
        self.rtc = machine.RTC()
        self.display = display
        self.leds = leds
        self.input = input
        self.beeper = beeper
        self.lock = lock
        self.position = 0;
        self.tick = 0
        self.app_list = ["Clock","Garage","Set Clock","Splash Screen","CMP Test"]
        self.app_list_length = len(self.app_list)
        self.chosen_app = None
        self.display_content = ''
        
    def read_input_queue(self):
        self.lock.acquire()
        while len(self.input.input_queue) > 0:
            self.input_handler(self.input.input_queue.pop(0))
        self.lock.release()
    
    def input_handler(self,action):
        
        self.tick = 100
        
        if (action == 'R_BTN_2'):
            pass
        elif (action == 'R_BTN'):
            self.chosen_app = self.app_list[(self.position)%self.app_list_length]
        elif (action == 'BTN'):
             self.chosen_app = 'Clock'
        elif (action == 'BTN_2'):
            pass
        elif (action == 'CW'):
            self.position +=1
        elif (action == 'CCW'):
            self.position -=1
            return
    
    def set_display(self, text):
        if (text != self.display_content):
            self.display_content = text
            self.display.clear()
            self.display.putstr(self.display_content)
            # print(self.display_content)
    
    def run(self):
 

        while True:
            self.read_input_queue()
            
            if self.chosen_app:
                print("app chosen")
                return str("APP_"+self.chosen_app)
            
            list_string = ("> " + str(self.app_list[self.position%self.app_list_length])
                           +" | "+ str(self.app_list[(self.position+1)%self.app_list_length] + ""))
            if len(list_string) >= 16:
                list_string = list_string[0:15]
            
            self.set_display("Main Menu \n"+list_string)
            # print(self.app_list[(self.position)%self.app_list_length])
            
            time.sleep(0.01)
            
        return False
            
