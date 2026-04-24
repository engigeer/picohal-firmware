import _thread

# =========================================================
# CORE 0 <-> CORE 1 SHARED STATE
# =========================================================

queue_lock = _thread.allocate_lock()

# Network command queue (Core 0 writes, Core 1 reads)
network_queue = []
network_up = False

# =========================================================
# EVENT FLAGS (Modbus → Main loop)
# =========================================================

pending_laser_update = False
pending_power_update = False
pending_output_update = False

# =========================================================
# DEBUG / WATCHDOG
# =========================================================

debug_mode = False  # Set to True via REPL to disable watchdog

# =========================================================
# SYSTEM STATE
# =========================================================

laser_emission_on = False
laser_guide_on = False
laser_power_value = 0

keepalive_update = False

#
outputs = 0
analog1_setpoint = 0
analog2_setpoint = 0
rpm_command = 0

laser_reset = False
laser_mains = False
laser_remotekey = False
laser_guide = False
laser_emission = False