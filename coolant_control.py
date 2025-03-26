from machine import Pin
from BLC_control import argon, powder1_state

def update_coolant_pins():
    from modbus_registers import client
    #only update the pins if they were assigned.
    if(argon) :
        argon.value(client.get_hreg(0x100) & 2)
    
    if(powder1_state) :
        powder1_state.value(client.get_hreg(0x100) & 1)


def set_coolant_callback(reg_type, address, val):
    global client
    update_coolant_pins()