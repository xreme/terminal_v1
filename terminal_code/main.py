import local_web_socket
import network
import socket
import time
import ujson
import real_time_clock
import input_drivers
import _thread
import main_menu
import garage_status
import machine
import splash_screen
import wificonnect
import device
import component_test
import set_clock

terminal = device.Device()


#setup the lock
lock = _thread.allocate_lock()

# set up the input
input = input_drivers.InputDrivers(lock)

#setup the clock // other applications
current_app = real_time_clock.RealTimeClock(terminal.lcd, terminal.green_led, terminal.beeper,input)
second_thread = _thread.start_new_thread(input.input_loop, ())

# reset LEDs and Display
terminal.green_led.off()
terminal.yellow_led.off()
terminal.red_led.off()
terminal.clear_display()

def activate(items,t):
    for item in items:
        item.on()
    
    time.sleep(t)

    for item in items:
        item.off()    
    
def read_input_queue(input_source):
    lock.acquire()
    while len(input_source.input_queue) > 0:
        input_handler(input_source.input_queue.pop(0))
    lock.release()

def input_handler(action):
    if (action == 'R_BTN_2'):
        terminal.lcd.backlight_off()
        activate([terminal.beeper, terminal.red_led],0.1)
    elif (action == 'R_BTN'):
        terminal.lcd.backlight_on()
        activate([terminal.beeper, terminal.red_led],0.2)
    elif (action == 'BTN'):
        activate([terminal.beeper, terminal.red_led],0.05)
        switchApp("menu")
    elif (action == 'BTN_2'):
        switchApp("SDS")

def statusHandler(status):
    if status.startswith("APP"):
        switchApp(status.strip("APP_"))

def switchApp(application):
    global current_app
    print("switching applications...")
    if application == "menu":
        print("switching to menu")
        current_app = main_menu.MainMenu(terminal.lcd,terminal.leds, terminal.beeper,input, lock)
    
    elif (application == "SDS" or application == "Garage"):
        terminal.yellow_led.on()
        current_app = garage_status.GarageStatus(terminal.lcd,terminal.leds,terminal.beeper,input)
        
    elif (application == "Splash Screen"):
        current_app = splash_screen.SplashScreen(terminal.lcd, terminal.leds, terminal.beeper,input)
    
    elif (application == "Set Clock"):
          current_app = set_clock.SetClockTime(terminal.lcd, terminal.leds, terminal.beeper,input,lock)
   
    elif (application == "CMP Test"):
        current_app = component_test.ComponentTest(terminal.lcd, terminal.leds, terminal.beeper,input, lock)
   
    else:
        current_app = real_time_clock.RealTimeClock(terminal.lcd, terminal.leds, terminal.beeper,input)
    
terminal.red_led.on()
time.sleep(0.1)
terminal.red_led.off()

prev_status = ''
while True:
    status = current_app.run()
    prev_status = status
    
    if(status != prev_status):
        print("current status:",status)
    
    if (status):
        statusHandler(status)
        status = None
        
    read_input_queue(input)   
