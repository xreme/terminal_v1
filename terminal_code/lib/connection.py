import network
import socket
from time import sleep
import machine

class Connection:

    def __init__(self):
        self.pico_led = machine. Pin("LED", machine.Pin.OUT)
        
        self.pico_led.on()
        #connect to the network
        self.ip = self.connect()
        self.pico_led.on()
        self.pico_led.off()

    #Connect to the Wi-Fi
    def connect(self):
        #open the file containing the ssid and password
        config_info_file = open('config.txt', 'r')

        #read the ssid and password
        config_info = config_info_file.readlines()
        ssid = config_info[0].strip()
        password = config_info[1].strip()

        #close the file
        config_info_file.close()
        
        #create an instance of the WLAN class
        wlan = network.WLAN(network.STA_IF)
        wlan.active(True)
        wlan.connect(ssid, password)
        
        #continue to send requests to connect to the network
        #until the connection is successful
        #FUTUTRE: add a timeout
        count = 0
        while not wlan.isconnected():
            self.pico_led.off()
            print('Waiting for Connection ' + str(count))
            count +=1
            self.pico_led.on()
            sleep(1)
        
        self.pico_led.off()
        #get the pico's local IP address
        ip = wlan.ifconfig()[0]
        print(f'Connected on {ip}')
        return ip