"""
Klasa zawierająca zegar i jego formatowanie
"""
import time
#import datetime error

class Zegar:
    rok = 0
    godzina = 0
    minuta = 0
    sekunda = 0
    
    def __init__(self):
        time_tuple = time.localtime()
        
        self.rok = time_tuple[0]
        self.godzina = time_tuple[3]
        self.minuta = time_tuple[4]
        self.sekunda = time_tuple[5]
    
    def __str__(self):
        return "{0:02d}:{1:02d}:{2:02d}".format(self.godzina,self.minuta,self.sekunda)
    
