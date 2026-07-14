from modbus_registers import client
from machine import Pin
import state

mod_pin = Pin(25, Pin.OUT); mod_pin.value(0) #modulate signal

def update_laser_state():

    # Set laser emission state
    if (state.laser_emission):
        if not (state.laser_emission_on):
            print('enable laser emission')
            state.laser_emission_on = True # Enable laser emission
            mod_pin.value(False) # Set modulate signal off by default

            with state.queue_lock:
                state.network_queue.append("cmd=emon")
        else:
            print('laser is already on')
    else:
        if (1):#state.laser_emission_on):
            print('disable laser emission')
            state.laser_emission_on = False # Disable laser emission
            mod_pin.value(False) # Set modulate signal off by default

            state.power_setpoint = 0 # Null power signal when laser emission is off
            print(f"laser power ={state.power_setpoint}%")

            with state.queue_lock:

                state.network_queue.append("cmd=emoff") # Disable laser emission
                state.network_queue.append("ver=1&sdc=0") # Set power to zero
        else:
            print('laser is already off')

def linearize_power_output(rpm):
    linear_data = [
        {"slope": 8.463984e-01, "offset": -2.765132e+02, "rpm": 854.8},   # Segment 1
        {"slope": 8.383298e-01, "offset": -2.834102e+02, "rpm": 2047.6},  # Segment 2
        {"slope": 8.715443e-01, "offset": -2.847283e+02, "rpm": 3195.0},  # Segment 3
        {"slope": 8.715443e-01, "offset": -2.847283e+02, "rpm": 4210.5},  # Segment 4
    ]

    if not rpm > 0:
       return 0
    
    idx = len(linear_data)-1
    while idx > 0 and rpm < linear_data[idx]["rpm"]:
        idx -= 1

    power_out = max(0, min(4000, int(linear_data[idx]["slope"] * rpm - linear_data[idx]["offset"]))) // 40
    
    return power_out

def update_laser_power():

    if (state.rpm_command == 0):
        mod_pin.value(False) # Modulate laser emission off
        print(f"laser off by modulation")
        return
    
    if state.laser_emission_on and state.rpm_command > 0:
        mod_pin.value(True) # Modulate laser emission on
        print(f"laser on by modulation")

    # Send power setpoint
    state.laser_power_command = linearize_power_output(state.rpm_command)
    if state.laser_power_command != state.power_setpoint:
        state.power_setpoint = state.laser_power_command
        print(f"laser power ={state.power_setpoint}%")

        with state.queue_lock:
            state.network_queue.append(f"ver=1&sdc={state.power_setpoint}")