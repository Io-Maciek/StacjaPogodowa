"""
Klasa zawierająca zegar i jego formatowanie
"""
import time

class Zegar:
    rok = 0
    godzina = 0
    minuta = 0
    sekunda = 0
    
    def __init__(self):
        self.time_tuple = time.localtime()
        
        self.rok = self.time_tuple[0]
        self.godzina = self.time_tuple[3]
        self.minuta = self.time_tuple[4]
        self.sekunda = self.time_tuple[5]
    
    def __str__(self):
        return "{0:02d}:{1:02d}:{2:02d}".format(self.godzina,self.minuta,self.sekunda)
    

