from nuts_bolts import program_flow
from collections import deque
#import modbus_registers

event_queue = deque((),16)

def process_event():
    global event_queue
    try:
        event = event_queue.popleft()
        print('Processing {}'.format(event))
    except IndexError as e:
        return
    
    if int(event) == int(program_flow.PROGRAM_COMPLETED) :
        print('finish flag')
        return

def event_callback(reg_type, address, val):
    global event_queue
    print('event received')
    event_queue.append(val[0])
    