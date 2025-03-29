from machine import Pin, PWM

argon_sol_pin   = 24 # (D8)  ARGON GAS SOLENOID
powder1_sol_pin = 19 # (D12) POWDER1 SOLENOID
powder1_pwm_pin = 26 # (3PIN NEOPIXEL) POWDER1 SOLENOID

powder1_setpoint = 0
powder2_setpoint = 0

#only assign pins if they are defined.
try :
    if(argon_sol_pin) :
        argon = Pin(argon_sol_pin, Pin.OUT)
        argon.value(0)
    if(powder1_sol_pin) :
        powder1_state = Pin(powder1_sol_pin, Pin.OUT)
        powder1_state.value(0)
    if(powder1_pwm_pin) :
        powder1_flow = PWM(Pin(powder1_pwm_pin), freq=1000, duty_u16=0) #maxValue 5V = 65536
except NameError:
    argon=0
    powder1=0

def update_BLC_pins():
    from modbus_registers import client

    BLC_reg = client.get_hreg(0x120)

    #only update the pins if they were assigned.
    if(argon) :
        argon.value(BLC_reg & 1)
    if(powder1_state) :
        powder1_state.value((BLC_reg >> 1) & 1)

def update_BLC_flowrate():
    from modbus_registers import client
    global powder1_setpoint
    global powder2_setpoint

    prev_powder1_setpoint = powder1_setpoint
    prev_powder2_setpoint = powder2_setpoint

    powder1_setpoint = client.get_hreg(0x121) & 0xFF # RPM as unit16
    powder2_setpoint = client.get_hreg(0x121) >> 8   # RPM as unit16

    if powder1_flow:
        if powder1_setpoint != prev_powder1_setpoint:
            print(f'powderflow{powder1_setpoint}')
            powder1_flow.duty_u16(max(1250, min(65536, int(powder1_setpoint)*500)-3750)) # todo: proper rpm fitting for non-linear response
        else:
            print('powder1flow is already at setpoint')
    # Set powder setpoints



def set_BLC_callback(reg_type, address, val):
    global client
    print('BLC pins update recieved')
    update_BLC_flowrate()
    #update_BLC_pins()