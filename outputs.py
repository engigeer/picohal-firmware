from machine import Pin
import state

r1 = Pin(16, Pin.OUT); r1.value(0) #AUX0 OUT
r2 = Pin(17, Pin.OUT); r2.value(0) #AUX1 OUT
r3 = Pin(18, Pin.OUT); r3.value(0) #AUX2 OUT
r4 = Pin(20, Pin.OUT); r4.value(0) #AUX3 OUT
r5 = Pin(21, Pin.OUT); r5.value(0) #AUX4 OUT
r6 = Pin(22, Pin.OUT); r6.value(0) #AUX5 OUT
r7 = Pin(19, Pin.OUT); r7.value(0) #AUX6 OUT
r8 = Pin(23, Pin.OUT); r8.value(0) #AUX7 OUT

def update_digital_outputs():

    #only update the pins if they were assigned.
    r1.value(state.outputs & 1)
    r2.value((state.outputs >> 1) & 1)
    r3.value((state.outputs >> 2) & 1)   
    r8.value((state.outputs >> 7) & 1)

    #state.laser_remotekey = (state.outputs >> 3) & 1
    r4.value(state.laser_remotekey)

    state.laser_mains = (state.outputs >> 4) & 1
    r5.value(state.laser_mains)

    state.laser_guide = (state.outputs >> 5) & 1
    r6.value(state.laser_guide)

    state.laser_reset = (state.outputs >> 6) & 1
    r7.value(state.laser_reset)

    update_IPG_pins()

# def update_analog_outputs():
#     from modbus_registers import client

#     prev_analog1_setpoint = state.analog1_setpoint
#     prev_analog2_setpoint = state.analog2_setpoint

#     analog1_setpoint = client.get_hreg(0x120)
#     analog2_setpoint = client.get_hreg(0x121)
    
#     if analog1_setpoint != prev_analog1_setpoint:
#         print(f'Analog1:{analog1_setpoint}')

#     if analog2_setpoint != prev_analog2_setpoint:
#         print(f'Analog2:{analog2_setpoint}')

def update_IPG_pins():
    
    if((state.laser_guide) and not (state.laser_guide_on)):
        print('enable guide laser')
        state.laser_guide_on = True
        with state.queue_lock:
            state.network_queue.append("cmd=abn")

    elif (not (state.laser_guide) and (state.laser_guide_on)):
        print('disable guide laser')
        state.laser_guide_on = False
        with state.queue_lock:
            state.network_queue.append("cmd=abf")

    if (state.laser_reset):
        print('reset_laser_errors')
        state.laser_reset = False
        with state.queue_lock:
            state.network_queue.append("cmd=rerr")