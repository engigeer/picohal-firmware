from machine import Pin
relay1_pin   = 18 # (D4)  
relay2_pin   = 22 # (D7)  
relay3_pin   = 24 # (D8)  
relay4_pin   = 19 # (D12) 

analog1_setpoint = 0
analog2_setpoint = 0

#only assign pins if they are defined.
try :
    if(relay1_pin) :
        relay1 = Pin(relay1_pin, Pin.OUT)
        relay1.value(0)
    if(relay2_pin) :
        relay2 = Pin(relay2_pin, Pin.OUT)
        relay2.value(0)
    if(relay3_pin) :
        relay3 = Pin(relay3_pin, Pin.OUT)
        relay3.value(0)
    if(relay4_pin) :
        relay4 = Pin(relay4_pin, Pin.OUT)
        relay4.value(0)
except NameError:
    relay1=0
    relay2=0
    relay3=0
    relay4=0

def update_digital_outputs():
    from modbus_registers import client

    dout_reg = client.get_hreg(0x110)

    #only update the pins if they were assigned.
    if(relay1) :
        relay1.value(dout_reg & 1)
    if(relay2) :
        relay2.value((dout_reg >> 1) & 1)
    if(relay3) :
        relay3.value((dout_reg >> 2) & 1)
    if(relay4) :
        relay4.value((dout_reg >> 3) & 1)

def update_analog_outputs():
    from modbus_registers import client
    global analog1_setpoint
    global analog2_setpoint

    prev_analog1_setpoint = analog1_setpoint
    prev_analog2_setpoint = analog2_setpoint

    analog1_setpoint = client.get_hreg(0x120)
    analog2_setpoint = client.get_hreg(0x121)
    
    if analog1_setpoint != prev_analog1_setpoint:
        print(f'Analog1:{analog1_setpoint}')

    if analog2_setpoint != prev_analog2_setpoint:
        print(f'Analog2:{analog2_setpoint}')

def set_output_callback(reg_type, address, val):
    global client
    print('output pins update recieved')
    update_digital_outputs()
    update_analog_outputs()