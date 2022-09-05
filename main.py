import network
import time
import urequests as req
from machine import Pin, RTC,I2C
from machine_i2c_lcd import I2cLcd
from zegar import Zegar
from dht22 import DHT22
from ir_rx.nec import NEC_8 as NEC
import ujson
import _thread
from classess.polskie_znaki import *

#dioda informacyjna
led = Pin("LED", Pin.OUT)
led.off()



# ekran
i2c = I2C(0, sda=Pin(0), scl=Pin(1), freq=400000)
I2C_ADDR = i2c.scan()[0]
lcd = I2cLcd(i2c, I2C_ADDR, 4, 20)


lcd.custom_char(0,tick_mark)
lcd.custom_char(1,l)
lcd.custom_char(2,a)
lcd.custom_char(3,e)
lcd.custom_char(4,s)
lcd.custom_char(5,c)


# czujnik pogody
rp2.PIO(0).remove_program() #?????
sensor = DHT22(Pin(17,Pin.IN,Pin.PULL_UP))




# czytanie lokalnego dodatku godziny z pliku g.txt
godzina_local=0
try:
    f = open("g.txt","r+")
    godzina_local = int(f.read())
    f.close()
except (OSError, ValueError):
    godzina_local = 0
print("Domyślna godzina: "+str(godzina_local))


# dioda IR RX
def ir_callback(data, addr, ctrl):
    global godzina_local
    if data >= 0:  # NEC protocol sends repeat codes.
        #print('Data {}'.format(data))
        if data==9:
            lcd.backlight_off()
        elif data==21:
            lcd.backlight_on()
        elif data == 22 and godzina_local>-6:
            godzina_local = godzina_local - 1
            f = open("g.txt","w")
            f.write(str(godzina_local))
            f.close()
            tm = time.localtime(time.time() - (3600))
            tm = tm[0:3] + (0,) + tm[3:6] + (0,)
            RTC().datetime(tm)
        elif data == 25:
            tm = time.localtime(time.time() - (godzina_local*3600))
            tm = tm[0:3] + (0,) + tm[3:6] + (0,)
            RTC().datetime(tm)
            godzina_local = 0
            f = open("g.txt","w")
            f.write(str(godzina_local))
            f.close()
        elif data == 13 and godzina_local<6:
            godzina_local = godzina_local + 1
            f = open("g.txt","w")
            f.write(str(godzina_local))
            f.close()
            tm = time.localtime(time.time() + (3600))
            tm = tm[0:3] + (0,) + tm[3:6] + (0,)
            RTC().datetime(tm)
        else:
            print(wlan.ifconfig()[0])
    
ir = NEC(Pin(16, Pin.IN),ir_callback)



# laczenie z siecia
netinfo = open("netinfo.txt","r")
net_lines = netinfo.read().split(':::')
netinfo.close()
lcd.putstr(chr(1)+chr(2)+"cz"+chr(3)+" z sieci"+chr(2)+"...  ")
led.on()
print("Łączę z siecią "+net_lines[0]+"...",end='')
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(net_lines[0], net_lines[1])
while not wlan.isconnected():
    time.sleep(1)
wlan.ifconfig(('192.168.254.239', '255.255.255.0', '192.168.254.254', '192.168.254.254'))
lcd.putchar(chr(0))
led.off()
print("\nPołączono!")




# pobieranie godziny
def download_and_set_time(show=False):
    if show:
        lcd.putstr("\nPobieram godzin"+chr(3))
    print("\nPróbuję pobrać godzinę",end='')
    godzinaErrCount = 0
    global godzinaIsSet
    while not godzinaIsSet and godzinaErrCount < 3:
        try:
            res = req.get("http://date.jsontest.com", timeout = 3)
            tm = time.localtime(int(str(res.json()["milliseconds_since_epoch"])[0:-3])+godzina_local*3600)
            tm = tm[0:3] + (0,) + tm[3:6] + (0,)
            RTC().datetime(tm)
            godzinaIsSet = True
            if show:
                lcd.move_to(20,1)
                lcd.putchar(chr(0))
            print("\nPobrano!")
        except OSError:
            print(".",end='')
            godzinaErrCount = godzinaErrCount + 1
            if show:
                lcd.putstr(".")
            if godzinaErrCount >= 3:
                if show:
                    lcd.putstr("X")
                time.sleep(3)
            else:
                time.sleep(3)
    update_connection_mark()
    
def update_connection_mark():
    global godzinaIsSet
    lcd.move_to(19,0)
    if not godzinaIsSet:        
        lcd.putchar('X')
    else:
        lcd.putchar(chr(0))
        
godzinaIsSet = False
download_and_set_time(True)

lcd.clear()
update_connection_mark()
lcd.move_to(0,2)
lcd.putstr("Temperatura       "+chr(223)+"C")
lcd.move_to(0,3)
lcd.putstr("Wilgotno"+chr(4)+chr(5)+"         %")


def send_post_to_pc():
    #try:
        print("\n\tPróbuję przesłać na mój pc")
        res = req.post("http://192.168.254.236:8000/pogoda", data = str(temp), timeout=5)
        print(res.text)
    #except OSError:
     #   godzinaIsSet = False

# program
while True:
    # czas
    lcd.move_to(0,0)
    zegar = Zegar()
    lcd.putstr(str(zegar))
    
    # pogoda
    try:
        temp, wilg = sensor.read()
        lcd.move_to(12,2)
        lcd.putstr("{:.2f}".format(temp))
        lcd.move_to(12,3)
        lcd.putstr("{:.2f}".format(wilg))
    except ValueError:
        lcd.move_to(12,2)
        lcd.putstr("N/A  ")
        lcd.move_to(12,3)
        lcd.putstr("N/A  ")
    
    # laczenie z serwerem
    if True:
        try:
            if not godzinaIsSet:
                _thread.start_new_thread(download_and_set_time, ())           
            #else:
             #   _thread.start_new_thread(send_post_to_pc, ())
        except OSError:
            pass
    
    
    
    time.sleep(1)


