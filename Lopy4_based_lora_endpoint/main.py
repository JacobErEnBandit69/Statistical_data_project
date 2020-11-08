import binascii
from pycom import heartbeat, wifi_on_boot, rgbled
import socket
from time import sleep
import machine
from network import LoRa
import struct
import ubinascii
from machine import Pin, ADC, UART
from CayenneLPP import CayenneLPP


##-------------------------------COLORS-----------------------------------------------------##
off = 0x000000
red = 0xff0000
green = 0x00ff00
blue = 0x0000ff
pink = 0xff69b4
##------------------------------------------------------------------------------------------##
##-----------------------Pycom default overwritten------------------------------------------##
heartbeat(False)
#Turn off Wifi
wifi_on_boot(False) #Untested
##---------------------------------LoRa-----------------------------------------------------##
# Initialize LoRaWAN radio to Europe and max allowed tx_power 
# according to ETSI standard (expecting antenna gain = cable loss on transmission side)
lora = LoRa(mode=LoRa.LORAWAN, region=LoRa.EU868)
##------------------------------------------------------------------------------------------##
##-------------------------------PIN_setup--------------------------------------------------##
 #------------------------------GPS UART----------------------------------------------------#
gps_reader_uart = UART(1) 
gps_reader_uart.init(baudrate=9600, bits=8, parity=None, stop=1) #Usage of default RX = P4 and TX = P3. UART communication

 #----------------------------Wakeup configuration------------------------------------------#
pin_in = Pin('P13', mode=Pin.IN, pull= Pin.PULL_DOWN)
machine.pin_sleep_wakeup(['P13'], machine.WAKEUP_ANY_HIGH, True)

##------------------------------------------------------------------------------------------##¨


def indicate(rgbHex):
    rgbled(rgbHex)







class Uart_IF:
    #class uses NMEA sentences, and splits by these. 
    def get_gps_buffer(self):
        raw_gps_buffer = str(gps_reader_uart.read())
        telegram_splitted_gps_buffer = raw_gps_buffer.split("$") #Telegrams starts with "$"
        return telegram_splitted_gps_buffer


class GPS_module():
    def get_current_pos(self, recursions):
        
        #Base case
        if (recursions == 0):
            #Conversion from NMES GPGGA version of Latitude degree to Latitude comma coordinate
            default_lat = 0
            default_lon = 0

            return default_lat, default_lon

        gps_buffer = Uart_IF().get_gps_buffer()
        #gps_buffer = read_uart()
        splitted_buffer = ""
        for i in range(len(gps_buffer)):
            splitted_buffer = gps_buffer[i].split(",")
            if(splitted_buffer[0] == "GPGGA"):
                if(splitted_buffer[2] != ''): 
                    raw_lat = str(splitted_buffer[2])
                    raw_lon = str(splitted_buffer[4])

                    #Conversion from NMES GPGGA version of Latitude degree to Latitude comma coordinate
                    lat = float(raw_lat[:2]) + float(raw_lat[2:])/60
                    #Conversion from NMES GPGGA version of Longitude degree to Longitude comma coordinate
                    lon = float(raw_lon[:3]) + float(raw_lon[3:])/60 
                    indicate(pink)
                    sleep(recursions)
                    return lat, lon
                else:
                    print("Critical data not present in gps_buffer")

        if(splitted_buffer == ""):
            print("GPS module not functional") 
            
        sleep(1) #Sleeps for 1 seconds, then retry to fill up buffer then retries if GPGAA is not present. 
        new_recursion = recursions - 1
        return self.get_current_pos(new_recursion)

class LoRa_IF:    
    
    def set_socket_configuration(self):
        s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)
        s.setsockopt(socket.SOL_LORA, socket.SO_DR, 0) 
        #s.setsockopt(socket.SOL_LORA, socket.SO_CONFIRMED, True) #So_fonfirmed flag is set, for confirmed uplinks only, otherwise retransmission 
        s.setblocking(True)
        return s

    def join_sequence(self, dev_eui, app_key):
        lora.join(activation=LoRa.OTAA, auth=(dev_eui, app_key), timeout=0)  #Join the network
		
        while not lora.has_joined(): # Loop until joined
            print('Not joined yet...')
            indicate(red)
            sleep(0.1)
            indicate(off)
            sleep(2)
        print('Joined')
        lora.nvram_save()

        afdsdCtrl2().go_to_sleep(0)#3600000) #3600000 = 1 Hour

    def send_packet(self, s, lpp) :
	    #Serverside will receive a 12 byte payload on the form
        payload = bytes(lpp.get_buffer()) 
        count = s.send(payload)
        print('Sent %s bytes' % count)

class afdsdCtrl2:
    
    def go_to_sleep(self, sleeptime):
        while True:
            indicate(green)
            sleep(0.1)
            indicate(blue)
            sleep(2)
            lora.nvram_save()
            
            machine.deepsleep(sleeptime) #Sleeps for 1 hour

    def deepsleep_wakeup_sequence(self):
        lora_if = LoRa_IF()
        lora.nvram_restore()
        indicate(red) #Red when package sending is started
        s = lora_if.set_socket_configuration()
        lat, lon = GPS_module().get_current_pos(8)

        ##Transmission section##
        indicate(blue) #Switching to blue when GPS is done.

        lpp = self.genereate_gps_lpp(lat, lon)

        lora_if.send_packet(s, lpp)
        self.go_to_sleep(20000)

    def genereate_gps_lpp(self, lat, lon):
        lpp = CayenneLPP()
        lpp.add_gps(1, lat, lon, 0)
        return lpp

#Use saved configuration if awoken
if machine.reset_cause() == machine.DEEPSLEEP_RESET: 
    afdsdCtrl2().deepsleep_wakeup_sequence() #Input to gps tries 1 second pr try
else: 
    #Should only run one time, and activates the device up against the join server with the given keys.
    # OTAA is used in this configuration
    dev_eui = lora.mac()
    app_key = binascii.unhexlify('277a0dc7e86ab61cc6c685c0883c3855')
    LoRa_IF().join_sequence(dev_eui, app_key)