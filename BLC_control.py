from machine import Pin

argon_sol_pin   = 24 # (D8)  ARGON GAS SOLENOID
powder1_sol_pin = 19 # (D12) POWDER1 SOLENOID

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

    BLC_reg = client.get_hreg(0x120)

    #only update the pins if they were assigned.
    if(argon) :
        argon.value(BLC_reg & 1)
    if(powder1) :
        powder1.value((BLC_reg >> 1) & 1)

def set_BLC_callback(reg_type, address, val):
    global client
    print('BLC pins update recieved')
    update_BLC_pins()