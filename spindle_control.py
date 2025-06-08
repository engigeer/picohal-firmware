from machine import Pin, PWM

laser_state_pin  = 16 # AUX OUT 0
laser_power_pin = 13 # PWM 0

rpm_setpoint = 0

#only assign pins if they are defined.
try :
    if(laser_state_pin) :
        laser_on = Pin(laser_state_pin, Pin.OUT)
        laser_on.value(0)
    # if(laser_mains_pin) :
    #     laser_mains = Pin(laser_mains_pin, Pin.OUT)
    #     laser_mains.value(0)
    # if(laser_guide_pin) :
    #     laser_guide = Pin(laser_guide_pin, Pin.OUT)
    #     laser_guide.value(0)
    # if(laser_shutter_pin) :
    #     laser_shutter = Pin(laser_shutter_pin, Pin.OUT)
    #     laser_shutter.value(0)
    # if(laser_reset_pin) :
    #     laser_reset = Pin(laser_reset_pin, Pin.OUT)
    #     laser_reset.value(0)
    if(laser_power_pin) :
        laser_power_pwm = PWM(Pin(laser_power_pin), freq=1000, duty_u16=0) #maxValue 5V = 65536
except NameError:
    laser_on=0
    laser_power_setpoint=0
    # laser_mains=0
    # laser_guide=0
    # laser_shutter=0
    # laser_reset=0

def update_laser_state():
    from modbus_registers import client
    global laser_on
    #only update the pins if they were assigned.

    SPINDLE_reg = client.get_hreg(0x200)

    if(laser_on) :
        laser_on.value(SPINDLE_reg & 1)
        print(f'state:{SPINDLE_reg & 1}')

# def linearize_power_output(rpm):
#     linear_data = [
#         {"slope": 8.463984e-01, "offset": -2.765132e+02, "rpm": 854.8},   # Segment 1
#         {"slope": 8.383298e-01, "offset": -2.834102e+02, "rpm": 2047.6},  # Segment 2
#         {"slope": 8.715443e-01, "offset": -2.847283e+02, "rpm": 3195.0},  # Segment 3
#         {"slope": 8.715443e-01, "offset": -2.847283e+02, "rpm": 4210.5},   # Segment 4
#     ]

#     if not rpm > 0:
#        return 0
    
#     idx = len(linear_data)-1
#     while idx > 0 and rpm < linear_data[idx]["rpm"]:
#         idx -= 1

#     power_out = max(0, min(4000, int(linear_data[idx]["slope"] * rpm - linear_data[idx]["offset"]))) // 40
    
#     return power_out

def update_laser_power():
    from modbus_registers import client
    global rpm_setpoint

    prev_rpm_setpoint = rpm_setpoint

    rpm_setpoint = client.get_hreg(0x201)  # RPM as unit16

    if laser_power_pwm:
        if rpm_setpoint != prev_rpm_setpoint:
            print(f'power:{rpm_setpoint}')
            laser_power_pwm.duty_u16(max(0, min(65536, int(rpm_setpoint)*8))) # todo: proper rpm fitting for non-linear response
        else:
            print('laser power is already at setpoint')

def set_spindle_rpm_callback(reg_type, address, val):
    global client
    #print('Spindle rpm update received')
    update_laser_power()

def set_spindle_state_callback(reg_type, address, val):
    global client
    #print('Spindle state update received')
    update_laser_state()