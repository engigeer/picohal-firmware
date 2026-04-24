import time
import _thread
import gc

from machine import WDT

from wiznet import w5x00_init, sendcmd
from modbus_registers import client
from outputs import update_digital_outputs
from spindle_control import update_laser_power, update_laser_state

import state

# =========================================================
# NETWORK INIT (CORE 1 DEPENDENCY)
# =========================================================

w5x00_init()

# =========================================================
# WATCHDOG
# =========================================================

print("Watchdog starting in 2s...")
time.sleep(2)

wdt = WDT(timeout=3000)

# =========================================================
# NETWORK CORE (CORE 1)
# =========================================================

def network_core():
    gc.collect()

    while True:
        cmd = None

        with state.queue_lock:
            if state.network_queue:
                cmd = state.network_queue.pop(0)

        if cmd:
            try:
                sendcmd(cmd)   # blocking OK here
            except Exception as e:
                print("network error:", e)
        else:
            time.sleep_ms(2)

_thread.start_new_thread(network_core, ())

# =========================================================
# MAIN LOOP (CORE 0 - REAL TIME)
# =========================================================

print("System deploying...")

while True:

    # ----------------------------
    # MODBUS (highest priority)
    # ----------------------------
    client.process()

    # ----------------------------
    # EVENT FLAGS (from state.py)
    # ----------------------------

    if state.pending_output_update:
        state.outputs = client.get_hreg(0x110)
        update_digital_outputs()
        state.pending_output_update = False

    if state.pending_laser_update:
        state.laser_emission = client.get_hreg(0x200)
        update_laser_state()
        state.pending_laser_update = False

    if state.pending_power_update:
        state.rpm_command = client.get_hreg(0x201)
        update_laser_power()
        state.pending_power_update = False

    # ----------------------------
    # WATCHDOG
    # ----------------------------
    if state.debug_mode or state.keepalive_update:
        wdt.feed()

    # ----------------------------
    # LIGHT IDLE
    # ----------------------------
    time.sleep_ms(1)

        