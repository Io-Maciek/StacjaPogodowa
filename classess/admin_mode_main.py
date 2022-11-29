import time

def admin_main(e, lcd):
    e.setCurrentWiFiMode(2)
    e._sendToESP8266('AT+CWSAP="stacjapogodowa","",11,0,3\r\n')
    e._sendToESP8266('AT+CIPMUX=1\r\n')
    print("Server: "+str(e._sendToESP8266('AT+CIPSERVER=1,8000\r\n')))
    uart = e.__uartObj
    ip = str(e._sendToESP8266("AT+CIPAP?\r\n"))[13:24]
    print("IP = "+ip)
    lcd.clear()
    lcd.putstr("ADMIN\n"+ip+":8000")
    SERVER_LOOP= True
    
    while SERVER_LOOP:
        read = uart.read(2000)
        if read is not None and "+IPD" in read:
            post_args = None
            try:
                _FIRST = str(read).index("GET /") + 4
            except ValueError:
                post_args = {}
                all_args = str(read).split('\\r\\n')
                for i, arg in enumerate(all_args):
                    if "ssid" in arg and "pwd" in arg:
                        print(str(arg)[:-1])
                        arg=arg[:-1]
                        for a in arg.split('&'):
                            info = a.split('=')
                            post_args[info[0]]=info[1]
                        break
                
                _FIRST = str(read).index("POST /") + 5
            _LAST = str(read).index("HTTP/1.1")-1
            URL = str(read)[_FIRST:_LAST]
            print(f"URL '{URL}'")
            time.sleep(0.1)
            if URL=='/end':
                SERVER_LOOP=False
            if URL=='/wifi':
                if post_args is None:
                    
                    try:
                        netinfo = open("netinfo.txt","r")
                        net_lines = netinfo.read().split('\n')
                        netinfo.close()
                    except OSError:
                        net_lines = ['BRAK', 'BRAK']
                    
                    HTML_CONTENT = f"<html><head><meta charset='utf-8'><meta name='viewport' content='width=device-width, initial-scale=1, shrink-to-fit=no'><title>Stacja pogodowa</title></head><body bgcolor='gray' style='color: black'><h1>WiFi</h1><form method='POST' action='/wifi'><label>SSID</label><input value={net_lines[0]} name='ssid' type='text'/><br><label>HASLO</label><input value={net_lines[1]} name='pwd' type='text'/><br></br><button type='submit'><h2>Zapisz</h2></button></form></body></html>"        
                    HTML_SENDER = f'HTTP/1.1 200 OK\r\nContent-Type: text/html;charset=UTF-8\r\nConnection: close\r\n\r\n<!DOCTYPE HTML>\r\n{HTML_CONTENT}\r\n\r\n'
                else:
                    netinfo = open("netinfo.txt",'w')
                    netinfo.write(f"{post_args['ssid']}\n{post_args['pwd']}")
                    netinfo.close()
                    HTML_SENDER = "HTTP/1.1 302  Found\r\nLocation: \ \r\n\r\n"
                time.sleep(0.1)
                uart.write(f'AT+CIPSEND=0,{len(HTML_SENDER)}\r\n')
                time.sleep(0.1)
                uart.write(HTML_SENDER)
            else:         
                HTML_CONTENT = f"<html><head><meta charset='utf-8'><meta name='viewport' content='width=device-width, initial-scale=1, shrink-to-fit=no'><title>Stacja pogodowa</title></head><body bgcolor='gray' style='color: black'><h1>ADMIN</h1><br><h3><a href='/wifi'>WiFi</a></h3><br><br><hr><br><a href='/end'><button><h2>Wylacz</h2></button></a></body></html>"        
                HTML_SENDER = f'HTTP/1.1 200 OK\r\nContent-Type: text/html;charset=UTF-8\r\nConnection: close\r\n\r\n<!DOCTYPE HTML>\r\n{HTML_CONTENT}\r\n\r\n'
                uart.write(f'AT+CIPSEND=0,{len(HTML_SENDER)}\r\n')
                time.sleep(0.1)
                uart.write(HTML_SENDER)
            time.sleep(0.1)
        uart.write('AT+CIPCLOSE=0\r\n')
        time.sleep(.3)

