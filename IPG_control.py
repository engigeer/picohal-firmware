from machine import Pin

laser_ready_pin  = 18 # (D4)  LASER READY  (KEYSWITCH ON)
laser_mains_pin  = 22 # (D7)  LASER MAINS  (POWERSUPPLY ACTIVE)
#laser_guide_pin  = 00 # (XX)  LASER GUIDE  (GUIDE ON)
#laser_enable_pin = 00 # (XX)  LASER ENABLE (EMISSION ON!!)

#only assign pins if they are defined.
try :
    if(laser_ready_pin) :
        laser_ready = Pin(laser_ready_pin, Pin.OUT)
        laser_ready.value(0)
    if(laser_mains_pin) :
        laser_mains = Pin(laser_mains_pin, Pin.OUT)
        laser_mains.value(0)
except NameError:
    laser_ready=0
    laser_mains=0

def update_IPG_pins():
    from modbus_registers import client
    #only update the pins if they were assigned.
    if(laser_ready) :
        laser_ready.value(client.get_hreg(0x110) & 1)
    
    if(laser_mains) :
        laser_mains.value(client.get_hreg(0x110) & 2)

def set_IPG_callback(reg_type, address, val):
    global client
    global displayline1
    update_IPG_pins()