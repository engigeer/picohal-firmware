from modbus_registers import client
import state

def update_laser_state():

    # Set laser emission state
    if (state.laser_emission):
        if not (state.laser_emission_on):
            print('enable laser emission')
            state.laser_emission_on = True

            with state.queue_lock:
                state.network_queue.append("cmd=emon")
        else:
            print('laser is already on')
    else:
        if (state.laser_emission_on):
            print('disable laser emission')
            state.laser_emission_on = False
            
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

    # Send power setpoint
    state.laser_power_value = linearize_power_output(state.rpm_command)
    with state.queue_lock:
        state.network_queue.append(f"ver=1&sdc={state.laser_power_value}")