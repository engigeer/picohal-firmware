from wiznet import sendcmd

laser_power_value = 0
laser_emission_on = 0

def update_laser_state():
    from modbus_registers import client
    global laser_emission_on

    laser_emission = client.get_hreg(0x200) & 1 # LASER ON bit

    # Set laser emission state
    if (laser_emission):
        if not (laser_emission_on):
            print('enable laser emmission')
            laser_emission_on = True
            sendcmd("cmd=emon") # Enable laser emission
        else:
            print('laser is already on')
    else:
        if (laser_emission_on):
            print('disable laser emission')
            laser_emission_on = False
            sendcmd("cmd=emoff") # Disable laser emission
        else:
            print('laser is already off')

def linearize_power_output(rpm):
    linear_data = [
        {"slope": 8.463984e-01, "offset": -2.765132e+02, "rpm": 854.8},   # Segment 1
        {"slope": 8.383298e-01, "offset": -2.834102e+02, "rpm": 2047.6},  # Segment 2
        {"slope": 8.715443e-01, "offset": -2.847283e+02, "rpm": 3195.0},  # Segment 3
        {"slope": 8.715443e-01, "offset": -2.847283e+02, "rpm": 4210.5},   # Segment 4
    ]

    if not rpm > 0:
       return 0
    
    idx = len(linear_data)-1
    while idx > 0 and rpm < linear_data[idx]["rpm"]:
        idx -= 1

    power_out = max(0, min(4000, int(linear_data[idx]["slope"] * rpm - linear_data[idx]["offset"]))) // 40
    
    return power_out

def update_laser_power():
    from modbus_registers import client
    global laser_power_value
    rpm_command = client.get_hreg(0x201)  # RPM as unit16

    # Send power setpoint
    laser_power_value = linearize_power_output(rpm_command)
    sendcmd(f"ver=1&sdc={laser_power_value}")

def set_spindle_rpm_callback(reg_type, address, val):
    global client
    #print('Spindle rpm update received')
    update_laser_power()

def set_spindle_state_callback(reg_type, address, val):
    global client
    #print('Spindle state update received')
    update_laser_state()