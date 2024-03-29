import time
from machine import Pin, RTC,I2C,UART, reset
from machine_i2c_lcd import I2cLcd
from classess.zegar import Zegar
from dht22 import DHT22
from ir_rx.nec import NEC_8 as NEC
import json
import _thread
from classess.polskie_znaki import *
from classess.http.esp8266 import ESP8266
from classess.admin_mode_main import admin_main
from classess.pms_sensor import PMS5003
import bme280
import sys
import uos

# czujnik cisnienia
#bme_i2c=I2C(0,sda=Pin(12), scl=Pin(13), freq=400000)
#print(bme_i2c.scan())
#bme = bme280.BME280(i2c=bme_i2c)
#print(bme.values)

# dioda informacyjna
led = Pin(25, Pin.OUT)
led.off()


# ekran
i2c = I2C(0, sda=Pin(0), scl=Pin(1), freq=400000)
I2C_ADDR = i2c.scan()[0]
lcd = I2cLcd(i2c, I2C_ADDR, 4, 20)
lcd.backlight_on()
lcd.clear()

lcd.custom_char(0,tick_mark)
lcd.custom_char(1,l)
lcd.custom_char(2,a)
lcd.custom_char(3,e)
lcd.custom_char(4,s)
lcd.custom_char(5,c)


# INICJACJA
print("Init")
lcd.putstr("Init")

# guzik trybu administracyjnego
admin_mode = False
def set_admin_mode(button):
    global admin_mode
    if not admin_mode:        
        admin_mode = True
        print('Włączam Admin')

button_admin = Pin(14, Pin.IN, Pin.PULL_DOWN)
button_admin.irq(trigger=Pin.IRQ_FALLING, handler=set_admin_mode, hard=True)


def lcd_toggle(lcd):
    if lcd.backlight==True:
        lcd.backlight_off()
    else:
        lcd.backlight_on()
              

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
            #print(wlan.ifconfig()[0])
            print("other")
    
ir = NEC(Pin(19, Pin.IN),ir_callback)

# czujnik pogody
rp2.PIO(0).remove_program() #?????
sensor = None
try:
    sensor = DHT22(Pin(18,Pin.IN,Pin.PULL_UP))
    if sensor.read() == (None, None):
        lcd.clear()
        lcd.putstr("DHT22 ERR")
        sys.exit() 
except Exception as e:
    lcd.clear()
    lcd.putstr("DHT22 ERR")
    print(e)
    sys.exit()


# czujnik pylow
pms = None
try:
    pms = PMS5003(
        uart=machine.UART(1, tx=machine.Pin(8), rx=machine.Pin(9), baudrate=9600),
        pin_enable=machine.Pin(3),
        pin_reset=machine.Pin(2),
        mode="active"
    )
except Exception as e:
    lcd.clear()
    lcd.putstr("PMS ERR")
    print(e)
    sys.exit()




# uruchamianie esp01
esp01 = None
try:
    esp01 = ESP8266(txPin=(16), rxPin=(17))
    esp8266_at_ver = None
except Exception as e:
    lcd.clear()
    lcd.putstr("ESP ERR")
    print(e)
    sys.exit()


print("Start",esp01.startUP())#esp01.reStart())
esp01._sendToESP8266("AT+RESTORE\r\n")
print("Wyłączam echo",esp01.echoING())
print("\r\n\r\n")

esp8266_at_ver = esp01.getVersion()
if(esp8266_at_ver != None):
    print(esp8266_at_ver)
    time.sleep(0.5)

lcdon = True
def lcdtoggle(p):
    global lcdon, lcd
    try:
        lcdon = not lcdon
        if not lcdon:
            lcd.backlight_off()
        else:
            lcd.backlight_on()
    except Exception as e:
        print(e)
        
def machinereset(p):
    reset()

button_admin.irq(trigger=0)

try:
    f = open('netinfo.txt', "r")
    f.close()
except OSError:  # open failed
    print('Nie znaleziono pliku.')
    admin_mode = True

if admin_mode:# or not admin_mode:
    button_admin.irq(trigger=Pin.IRQ_FALLING, handler=machinereset)
    print("\n###                     ###\n### TRYB ADMINISTRATORA ###\n###                     ###\n")
    admin_main(esp01, lcd)
    print("\n###            ###\n### ZAKOŃCZONO ###\n###            ###\n")
    lcd.clear()
    lcd.putstr("Re Init")
    print("Restart",esp01.reStart())
    print("Wyłączam echo",esp01.echoING())
    print("\r\n\r\n")

button_admin.irq(trigger=0)
button_admin.irq(trigger=Pin.IRQ_FALLING, handler=lcdtoggle)

esp01.setCurrentWiFiMode(1)
print("\r\n\r\nŁączę z WiFi...")

netinfo = open("netinfo.txt","r")
net_lines = netinfo.read().split('\n')
netinfo.close()
lcd.clear()
lcd.putstr(chr(1)+chr(2)+"cz"+chr(3)+" z sieci"+chr(2)+"...  ")
led.on()

# TODO timeout???
while (1):
    if "WIFI CONNECTED" in esp01.connectWiFi(net_lines[0].strip(), net_lines[1].strip()):
        break;
    else:
        print(".")
        time.sleep(2)

if len(net_lines)>3:
    print("not DHCP")
    print("Konfiguracja internetu: "+str(esp01._sendToESP8266(f"AT+CIPSTA=\"{net_lines[2]}\",\"{net_lines[3]}\",\"{net_lines[4]}\"\r\n")))
else:
    print("DHCP")

print("ALL: "+str(str(esp01._sendToESP8266("AT+CIPSTA?\r\n"))))
lcd.putchar(chr(0))
led.off()
print("\nPołączono!")

    
        
def properJSONfromHTTPresponse(http):  
    splits = http[:-1].split('\\n')
    sums = ""
    for x in splits:
        sums=sums+x
    return json.loads(sums)


# pobieranie godziny
def download_and_set_time(show=False):
    if show:
        lcd.putstr("\nPobieram godzin"+chr(3))
    print("\nPróbuję pobrać godzinę",end='')
    godzinaErrCount = 0
    global godzinaIsSet
    while not godzinaIsSet and godzinaErrCount < 3:
        try:
            _, httpRes = esp01.doHttpGet("date.jsontest.com","/","Pi-Pico", port=80)
            tm = time.localtime(int(str(properJSONfromHTTPresponse(httpRes)["milliseconds_since_epoch"])[0:-3])+godzina_local*3600)
            tm = tm[0:3] + (0,) + tm[3:6] + (0,)
            RTC().datetime(tm)
            godzinaIsSet = True
            if show:
                lcd.move_to(19,1)
                lcd.putchar(chr(0))
            print("\nPobrano!")
        except:
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



# czytanie lokalnego dodatku godziny z pliku g.txt
godzina_local=0
try:
    f = open("g.txt","r+")
    godzina_local = int(f.read())
    f.close()
except (OSError, ValueError):
    godzina_local = 0


godzinaIsSet = False
download_and_set_time(True)

# program
lcd.clear()
print("")
esp01._sendToESP8266('AT+CIPMUX=1\r\n')
esp_info = str(esp01._sendToESP8266("AT+CIPSTA?\r\n"))
s= esp_info.find('ip:"') + len('ip:"')
e=esp_info.find('"\\r\\n+')
ip = esp_info[s:e]
print("ip: ",end='')
print(ip)
print("Server: "+str(esp01._sendToESP8266('AT+CIPSERVER=1,80\r\n'))+"\n\n")
uart = esp01.__uartObj
lcd.move_to(0,1)
lcd.putstr(ip)


update_connection_mark()
lcd.move_to(0,2)
lcd.putstr("Temperatura       "+chr(223)+"C")
lcd.move_to(0,3)
lcd.putstr("Wilgotno"+chr(4)+chr(5)+"         %")

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
    pms_data = pms.read().data[:3]
    PM1_0 = pms_data[0]
    PM2_5 = pms_data[1]
    PM10 = pms_data[2]
    
    read = uart.read()
    if read is not None and "+IPD" in read:
        #print(read)
        _FIRST = str(read).index("GET /") + 4
        _LAST = str(read).index("HTTP/1.1")-1
        URL = str(read)[_FIRST:_LAST]
        print(f"URL '{URL}'")
        
        
        
        if 'Authorization: Basic' in read:
            auth = (str(read[read.find(b'Authorization: Basic')+len('Authorization: Basic '):]).split('\\r\\n')[0])
            if auth[2:].strip() == 'YWRtaW46YWRtaW4=': # TODO add changing pass to admin mode
                if URL=='/api':
                    contents = {"temperatura": temp, "wilgoc": wilg, "czas": zegar.time_tuple, "PM1_0": PM1_0, "PM2_5": PM2_5, "PM10": PM10, "lcd": lcd.backlight}
                    contents_json = json.dumps(contents)
                    HTML_CONTENT = contents_json      
                    HTML_SENDER = f'HTTP/1.1 200 OK\r\nContent-Type: application/json;charset=UTF-8\r\nConnection: close\r\n\r\n{HTML_CONTENT}\r\n\r\n'
                elif URL=='/reset':
                    HTML_CONTENT = f"<html><head><meta charset='utf-8'><meta name='viewport' content='width=device-width, initial-scale=1, shrink-to-fit=no'><title>Stacja pogodowa</title></head><body bgcolor='gray' style='color: black'><h1></h1>Resetuje...</body></html>"        
                    HTML_SENDER = f'HTTP/1.1 200 OK\r\nContent-Type: text/html;charset=UTF-8\r\nConnection: close\r\n\r\n<!DOCTYPE HTML>\r\n{HTML_CONTENT}\r\n\r\n'
                    uart.write(f'AT+CIPSEND=0,{len(HTML_SENDER)}\r\n')
                    time.sleep(0.1)
                    uart.write(HTML_SENDER)
                    time.sleep(0.1)
                    lcd.clear()
                    lcd.putstr('Resetuje...')
                    reset()
                elif URL=='/lcd':
                    lcd_toggle(lcd)
                else:
                    HTML_CONTENT = f"<html><head><meta charset='utf-8'><meta name='viewport' content='width=device-width, initial-scale=1, shrink-to-fit=no'><title>Stacja pogodowa</title></head><body bgcolor='gray' style='color: black'><h1>Temperatura: {temp} &#xb0;C</h1><h1>Wilgotnosc: {wilg} %</h1><h1>PM1.0: {PM1_0} ug/m3</h1><h1>PM2.5: {PM2_5} ug/m3</h1><h1>PM10: {PM10} ug/m3</h1><hr><a href='/api'><button><h2>API</h2></button></a><br><a href='/lcd'><button><h2>LCD</h2></button></a><br><a href='/reset'><button><h2>Reset</h2></button></a></body></html>"        
                    HTML_SENDER = f'HTTP/1.1 200 OK\r\nContent-Type: text/html;charset=UTF-8\r\nConnection: close\r\n\r\n<!DOCTYPE HTML>\r\n{HTML_CONTENT}\r\n\r\n'
                uart.write(f'AT+CIPSEND=0,{len(HTML_SENDER)}\r\n')
                time.sleep(0.1)
                uart.write(HTML_SENDER)
            else:
                err_not_autorized_mess='<h1>401 Unauthorized</h1>'
                sender=f'HTTP/1.1 401 Unauthorized\r\nWWW-Authenticate: Basic realm="Restricted"\r\nContent-type: text/html\r\n\r\n<!DOCTYPE HTML>\r\n{err_not_autorized_mess}\r\n\r\n'
                
                
                uart.write(f'AT+CIPSEND=0,{len(sender)}\r\n')
                time.sleep(0.1)
                uart.write(sender)
        else:
            err_not_autorized_mess='<h1>401 Unauthorized</h1>'
            sender=f'HTTP/1.1 401 Unauthorized\r\nWWW-Authenticate: Basic realm="Restricted"\r\nContent-type: text/html\r\n\r\n<!DOCTYPE HTML>\r\n{err_not_autorized_mess}\r\n\r\n'
            
            
            uart.write(f'AT+CIPSEND=0,{len(sender)}\r\n')
            time.sleep(0.1)
            uart.write(sender)
        time.sleep(0.1)
    uart.write('AT+CIPCLOSE=0\r\n')
    time.sleep(.8)
        
