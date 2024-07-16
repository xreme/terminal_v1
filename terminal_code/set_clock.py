import machine
import time
import input_drivers
import real_time_clock

class SetClockTime:
    
    def __init__(self,display,leds,beeper,inputs,lock):
        self.rtc = machine.RTC()
        self.display = display
        self.leds = leds
        self.input = inputs
        self.beeper = beeper
        self.lock = lock
        self.content = ''
        self.position = 0
        self.screen = 0
        self.newDate = []
        self.newTime = []
        self.status = False
    
    def set_display(self, content):
        if (content != self.content):
            self.content = content
            self.display.clear()
            self.display.putstr(content)
    
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
            if(self.screen == 0):
                if((self.position%2)==0):
                    self.position = 0
                    self.screen = 1
                if((self.position%2)==1):
                    self.position = 0
                    self.screen = 2
            if(self.screen == 1 or self.screen==2):
                self.position +=1
        elif (action == 'BTN'):
            if(self.screen == 0):
                self.status = True
            if(self.screen == 1):
                self.setDateTime()
                self.set_display('Date Set!')
                time.sleep(2)
                self.screen = 0
            if(self.screen == 2):
                self.setDateTime()
                self.set_display('Time Set!')
                time.sleep(2)
                self.screen = 0
        elif (action == 'BTN_2'):
            pass
        elif (action == 'CW'):
            if(self.screen == 0):
                self.position +=1

            if(self.screen == 1):
                if((self.position%3) == 0 and self.newDate[0] < 2099):
                    self.newDate[0] += 1

                if((self.position%3) == 1):
                    self.newDate[1] += 1
                    if self.newDate[1] > 12:
                        self.newDate[1] = 1
                
                if((self.position%3) == 2):
                    self.newDate[2] += 1
                    if self.newDate[2] > 31:
                        self.newDate[2] = 1
            
            if(self.screen == 2):
                if((self.position%3) == 0):
                    self.newTime[0] += 1
                    if self.newTime[0] > 23:
                        self.newTime[0] = 0

                if((self.position%3) == 1):
                    self.newTime[1] += 1
                    if self.newTime[1] > 59:
                        self.newTime[1] = 0
                
                if((self.position%3) == 2):
                    self.newTime[2] += 1
                    if self.newTime[2] > 59:
                        self.newTime[2] = 0


        elif (action == 'CCW'):
            if(self.screen == 0):
                self.position +=1

            if(self.screen == 1):
                if((self.position%3) == 0 and self.newDate[0] > 2000):
                    self.newDate[0] -= 1

                if((self.position%3) == 1):
                    self.newDate[1] -= 1
                    if self.newDate[1] < 1:
                        self.newDate[1] = 12
                
                if((self.position%3) == 2):
                    self.newDate[2] -= 1
                    if self.newDate[2] < 1:
                        self.newDate[2] = 31
            
            if(self.screen == 2):
                if((self.position%3) == 0):
                    self.newTime[0] -= 1
                    if self.newTime[0] < 0:
                        self.newTime[0] = 23

                if((self.position%3) == 1):
                    self.newTime[1] -= 1
                    if self.newTime[1] < 0:
                        self.newTime[1] = 59
                
                if((self.position%3) == 2):
                    self.newTime[2] -= 1
                    if self.newTime[2] < 0:
                        self.newTime[2] = 59
        return
    
    def setDateTime(self):
        rtc = machine.RTC()
        rtc.datetime((self.newDate[0], self.newDate[1],self.newDate[2], 0, 
                      self.newTime[0], self.newTime[1], self.newTime[2], 0))

    def run(self):
        clock  = real_time_clock.RealTimeClock(self.display, self.leds, self.beeper,self.input)
        self.newDate = clock.get_date_array()
        self.newTime = clock.get_time_array()
        while True:

            if (self.screen == 0):
                content = 'Set \n'
                if((self.position%2)==0):
                    content += ' ->Date   Time'
                if((self.position%2)==1):
                    content += '   Date ->Time'

            
            if (self.screen == 1):
                content = 'Date (YMD):\n'

                if ((self.position%3) == 0):
                    content += '->'+ str(self.newDate[0]) + '/'
                else:
                    content = content + str(self.newDate[0]) + '/'
                if ((self.position%3) == 1):
                    content += '->'+str(self.newDate[1]) + '/'
                else:
                    content +=str(self.newDate[1]) + '/'
                if ((self.position%3) == 2):
                    content += '->'+str(self.newDate[2])
                else:
                    content +=str(self.newDate[2])

            if (self.screen == 2):
                content = 'Set Time:\n'

                if ((self.position%3) == 0):
                    content += '->'+ str(self.newTime[0]) + ':'
                else:
                    content = content + str(self.newTime[0]) + ':'
                if ((self.position%3) == 1):
                    content += '->'+str(self.newTime[1]) + ':'
                else:
                    content +=str(self.newTime[1]) + ':'
                if ((self.position%3) == 2):
                    content += '->'+str(self.newTime[2])
                else:
                    content +=str(self.newTime[2])
            
            self.read_input_queue()            
            self.set_display(content)
            if (self.status):
                return str("APP_"+'')