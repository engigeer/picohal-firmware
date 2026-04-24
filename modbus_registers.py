from machine import Pin
from umodbus.serial import ModbusRTU
import state

# =========================================================
# CONFIGURATION
# =========================================================

slave_addr = 10
modbus_baud = 19200
rtu_pins = (Pin(8), Pin(9))
uart_id = 1

# =========================================================
# CALLBACKS (MUST BE FAST, NO I/O)
# =========================================================

def set_spindle_rpm_callback(reg_type, address, val):
    state.pending_power_update = True

def set_spindle_state_callback(reg_type, address, val):
    state.pending_laser_update = True

def set_output_callback(reg_type, address, val):
    state.pending_output_update = True

def set_keepalive_callback(reg_type, address, val):
    state.keepalive_update = True

registers = {
    "HREGS": {    
        "KEEPALIVE_REGISTER": {
            "register": 0x100,
            "len": 1,
            "val": 0,
            "on_set_cb": set_keepalive_callback    
        },
        "DIGITAL_OUTPUT_REGISTER": {
            "register": 0x110,
            "len": 1,
            "val": 0,
            "on_set_cb": set_output_callback    
        },
        "ANALOG_OUTPUT_REGISTER_0": {
            "register": 0x120,
            "len": 1,
            "val": 0,
            "on_set_cb": set_output_callback    
        },
        "ANALOG_OUTPUT_REGISTER_1": {
            "register": 0x121,
            "len": 1,
            "val": 0,
            "on_set_cb": set_output_callback    
        },
        "SPINDLE_RUN_REGISTER": {
            "register": 0x200,
            "len": 1,
            "val": 0,
            "on_set_cb": set_spindle_state_callback    
        },
        "SPINDLE_SET_RPM_REGISTER": {
            "register": 0x201,
            "len": 1,
            "val": 0,
            "on_set_cb": set_spindle_rpm_callback    
        }
    }    
}

# =========================================================
# MODBUS CLIENT INIT
# =========================================================

client = ModbusRTU(
    addr=slave_addr,        # address on bus
    pins=rtu_pins,          # given as tuple (TX, RX)
    baudrate=modbus_baud,        # optional, default 9600
    data_bits=8,          # optional, default 8
    stop_bits=1,          # optional, default 1
    parity=None,          # optional, default None
    ctrl_pin=27,          # optional, control DE/RE
    uart_id=uart_id         # optional, default 1, see port specific documentation
)

# =========================================================
# SETUP
# =========================================================

print("Setting up registers ...")
client.setup_registers(registers)

print("Register setup done")

print(
    "Serving as RTU client on address {} at {} baud"
    .format(slave_addr, modbus_baud)
)