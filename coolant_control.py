from machine import Pin

relay1_pin = 18 # (D4) MIST
relay2_pin = 22 # (D7) FLOOD
relay3_pin = 24 # (D8)
relay4_pin = 19 # (D12)

#only assign pins if they are defined.
try :
    if(relay1_pin) :
        mist = Pin(relay1_pin, Pin.OUT)
        mist.value(0)
    if(relay2_pin) :
        flood = Pin(relay2_pin, Pin.OUT)
        flood.value(0)
except NameError:
    mist=0
    flood=0

def update_coolant_pins():
    from modbus_registers import client
    #only update the pins if they were assigned.
    if(mist) :
        mist.value(client.get_hreg(0x100) & 1)
    
    if(flood) :
        flood.value(client.get_hreg(0x100) & 2)


def set_coolant_callback(reg_type, address, val):
    global client
    global displayline1
    update_coolant_pins()