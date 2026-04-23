import time
import urequests
from machine import Pin,SPI
import network
import state

# TO-DO: NETWORK HEALTH MANAGEMENT

# =========================================================
# NETWORK INITIALIZATION
# =========================================================

def w5x00_init():

    spi=SPI(0,2_000_000, mosi=Pin(3),miso=Pin(0),sck=Pin(2))
    nic = network.WIZNET5K(spi,Pin(1),Pin(4)) #spi,cs,reset pin
    nic.active(True)

    nic.ifconfig(('192.168.3.235','255.255.255.0','192.168.3.230','0.0.0.0'))
    
    timeout = 10
    start = time.time()

    while not nic.isconnected():
        time.sleep(1)
        print("Waiting for network...")

        if time.time() - start > timeout:
            print("Network init failed (timeout)")
            state.network_up = False
            return

    print("Network up:", nic.ifconfig())
    state.network_up = True

def sendcmd(data):

    if not state.network_up:
        print("Network not ready:", data)
        return

    url = "http://192.168.3.230/setcmd"

    headers = {
        "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
        "x-requested-with": "XMLHttpRequest"
    }

    try:
        response = urequests.post(url, headers=headers, data=data, timeout=2)
        print("HTTP:", response.status_code)
        response.close()

    except Exception as e:
        print("sendcmd error:", e)