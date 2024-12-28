from machine import Pin

argon_sol_pin   = 24 # (D8)  ARGON GAS SOLENOID
powder1_sol_pin = 19 # (D12) POWDER1 SOLENOID
#powder1_rate_pin = 26 # (D12) POWDER1 FLOWRATE (NEED TO IMPLEMENT)

#only assign pins if they are defined.
try :
    if(argon_sol_pin) :
        argon = Pin(argon_sol_pin, Pin.OUT)
        argon.value(0)
    if(powder1_sol_pin) :
        powder1 = Pin(powder1_sol_pin, Pin.OUT)
        powder1.value(0)
except NameError:
    argon=0
    powder1=0

def update_BLC_pins():
    from modbus_registers import client
    #only update the pins if they were assigned.
    if(argon) :
        argon.value(client.get_hreg(0x120) & 1)
    if(powder1) :
        powder1.value(client.get_hreg(0x120) & 2)

def set_BLC_callback(reg_type, address, val):
    global client
    global displayline1
    update_BLC_pins()