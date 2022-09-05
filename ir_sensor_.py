import time
from machine import Pin
from ir_rx.nec import NEC_16

class Sensor:
    def __init__(self, callback):
        ir = NEC_16(Pin(16, Pin.IN), callback)
                    
ir_key = {
    0x45: 'ON',
    0x46: 'MODE',
    0x47: 'OFF',
    0x44: 'FLASH',
    0x40: 'PREV',
    0x43: 'NEXT',
    0x07: 'SMOOTH',
    0x15: 'BRIGHTER',
    0x09: 'DIMMER',
    0x16: 'R',
    0x19: 'G',
    0x0D: 'B',
    0x0C: '1',
    0x18: '2',
    0x5E: '3',
    0x08: '4',
    0x1C: '5',
    0x5A: '6',
    0x42: '7',
    0x52: '8',
    0x4A: '9'    
    }



