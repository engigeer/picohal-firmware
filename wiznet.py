from usocket import socket
from machine import Pin,SPI
import network
import time

import urequests

led = Pin(8, Pin.OUT)
networkup = False

# TO-DO:
# https://github.com/Wiznet/RP2040-HAT-MicroPython/blob/main/examples/HTTP/HTTP_Client/urequests.py

#W5x00 chip init
def w5x00_init():
    global networkup

    spi=SPI(0,2_000_000, mosi=Pin(3),miso=Pin(0),sck=Pin(2))
    nic = network.WIZNET5K(spi,Pin(1),Pin(4)) #spi,cs,reset pin
    nic.active(True)
    # The only difference from the example linked above, using 
    # 'dhcp' instead of manually specifying the network info
    # nic.ifconfig('dhcp')
    nic.ifconfig(('192.168.3.235','255.255.255.0','192.168.3.230','0.0.0.0'))
    while not nic.isconnected():
        time.sleep(1)
        print(nic.regs())
    print(nic.ifconfig())
    networkup = True

def sendcmd(data):
    global networkup

    if not networkup:
        print("Network is down, cannot send:", data)
        return

    url = "http://192.168.3.230/setcmd"
    headers = {
        "accept": "application/json, text/javascript, */*; q=0.01",
        "accept-language": "en-US,en;q=0.9",
        "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
        "x-requested-with": "XMLHttpRequest"
    }
    #data = "ver=1&sdc=5"
    #data = "cmd=eeabc" # enable aiming beam control?

    try:
        response = urequests.post(url, headers=headers, data=data, timeout=1)
        print("Status code:", response.status_code)
        print("Response text:", response.text)
        response.close()
    except Exception as e:
        print("Error:", e)
        
def main():
    print('null main loop')

if __name__ == "__main__":
    main()