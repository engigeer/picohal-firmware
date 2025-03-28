from machine import Pin
from wiznet import sendcmd
import time

laser_ready_pin  = 18 # (D4)  LASER READY  (KEYSWITCH ON)
laser_mains_pin  = 22 # (D7)  LASER MAINS  (POWERSUPPLY ACTIVE)
# laser_guide_pin  = 21 # (D6)  LASER GUIDE  (GUIDE ON)
# laser_shutter_pin = 20 # (D5)  LASER SHUTTER (EMISSION MAY BE ON!!)
# laser_reset_pin = XX

laser_guide_on = False
laser_emission_on = False
laser_power_value = 0

#only assign pins if they are defined.
try :
    if(laser_ready_pin) :
        laser_ready = Pin(laser_ready_pin, Pin.OUT)
        laser_ready.value(0)
    if(laser_mains_pin) :
        laser_mains = Pin(laser_mains_pin, Pin.OUT)
        laser_mains.value(0)
    # if(laser_guide_pin) :
    #     laser_guide = Pin(laser_guide_pin, Pin.OUT)
    #     laser_guide.value(0)
    # if(laser_shutter_pin) :
    #     laser_shutter = Pin(laser_shutter_pin, Pin.OUT)
    #     laser_shutter.value(0)
    # if(laser_reset_pin) :
    #     laser_reset = Pin(laser_reset_pin, Pin.OUT)
    #     laser_reset.value(0)
except NameError:
    laser_ready=0
    laser_mains=0
    # laser_guide=0
    # laser_shutter=0
    # laser_reset=0

def update_IPG_pins():
    from modbus_registers import client
    global laser_guide_on
    #only update the pins if they were assigned.

    IPG_reg = client.get_hreg(0x110)

    if(laser_ready) :
        laser_ready.value(IPG_reg & 1)
    
    if(laser_mains) :
        laser_mains.value((IPG_reg >> 1) & 1) # laser mains is momentary signal
        time.sleep(0.05)
        laser_mains.value(0)

    # if(laser_guide) :
    #     laser_guide.value((IPG_reg >> 2) & 1)

    # if(laser_shutter) :
    #     laser_shutter.value((IPG_reg >> 3) & 1)

    # if(laser_reset) :
    #     laser_reset.value((IPG_reg >> 4) & 1)

    # Guide beam control
    laser_guide = ((IPG_reg >> 2) & 1)

    if((laser_guide) and not (laser_guide_on)):
        print('enable guide laser')
        laser_guide_on = True
        sendcmd("cmd=abn")
    elif not (laser_guide) and (laser_guide_on):
        print('disable guide laser')
        laser_guide_on = False
        sendcmd("cmd=abf")

    # Reset laser errors
    laser_reset = ((IPG_reg >> 4) & 1)
           
    if (laser_reset):
        print('reset_laser_errors')
        laser_guide_on = False
        sendcmd("cmd=rerr")

def update_IPG_laser_power():
    from modbus_registers import client

    rpm_setpoint = client.get_hreg(0x201)  # RPM as unit16

    # Send power setpoint
    rpm_limit = max(0, min(4000, int(rpm_setpoint)))
    laser_power_value = rpm_limit // 40
    sendcmd(f"ver=1&sdc={laser_power_value}")

def update_IPG_laser_state():
    from modbus_registers import client
    global laser_emission_on

    laser_emission = client.get_hreg(0x200) & 1 # LASER ON bit

    # Set laser emission state
    if((laser_emission) and not (laser_emission_on)):
        print('enable laser emmission')
        laser_emission_on = True
        sendcmd("cmd=emon") # Enable laser emission
    elif not (laser_emission) and (laser_emission_on):
        print('disable laser emission')
        laser_emission_on = False
        sendcmd("cmd=emoff") # Disable laser emission

def set_IPG_callback(reg_type, address, val):
    global client
    print('IPG pins update recieved')
    update_IPG_pins()

def set_spindle_rpm_callback(reg_type, address, val):
    global client
    print('Spindle rpm update received')
    update_IPG_laser_power()

def set_spindle_state_callback(reg_type, address, val):
    global client
    print('Spindle state update received')
    update_IPG_laser_state()