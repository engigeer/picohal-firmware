
from outputs import set_output_callback
from spindle_control import set_spindle_state_callback, set_spindle_rpm_callback
from event_handler import event_callback
from machine import WDT

from nuts_bolts import enum
import time

print('initializing watchdog in 2s, interrupt code now to cancel')
time.sleep(2)
wdt = WDT(timeout=3000)

def set_status_callback(reg_type, address, val):
    print('status pin update received')

def set_keepalive_callback(reg_type, address, val):
    global wdt
    timestamp = time.time()
    wdt.feed()


def set_coolant_callback(reg_type, address, val):
   print('coolant pin update received')

registers = {
    "HREGS": {
        "STATUS_REGISTER": {
            "register": 0x01,
            "len": 1,
            "val": 255,
            "on_set_cb": set_status_callback    
        },
        "ALARM_REGISTER": {
            "register": 0x02,
            "len": 1,
            "val": 0,   
        },         
        "INPUT_REGISTER": {
            "register": 0x03,
            "len": 1,
            "val": 255,    
        },
        "OUTPUT_REGISTER": {
            "register": 0x04,
            "len": 1,
            "val": 0,
            "on_set_cb": set_output_callback    
        },
        "EVENT_REGISTER": {
            "register": 0x05,
            "len": 1,
            "val": 0,
            "on_set_cb": event_callback    
        },          
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

from machine import Pin   
from umodbus.serial import ModbusRTU

slave_addr = 10             # address on bus as client
modbus_baud = 19200
rtu_pins = (Pin(8), Pin(9))     # (TX, RX)
uart_id = 1

#import modbus_registers

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

# define Modbus Registers here
#register_definitions = modbus_registers.registers

print('Setting up registers ...')
# use the defined values of each register type provided by register_definitions
client.setup_registers(registers)
print('Register setup done')

print('Serving as RTU client on address {} at {} baud'.
      format(slave_addr, modbus_baud))
