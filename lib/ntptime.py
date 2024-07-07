import utime
from classess.http.esp8266 import ESP8266

# The NTP host can be configured at runtime by doing: ntptime.host = 'myhost.org'
host = "pool.ntp.org"
# The NTP socket timeout can be configured at runtime by doing: ntptime.timeout = 2
timeout = 1


def time(esp):
    NTP_QUERY = bytearray(48)
    NTP_QUERY[0] = 0x1B
    
    txData="AT+CIPSTART="+'"'+"UDP"+'"'+','+'"'+host+'"'+','+str(123)+"\r\n"
    retData = esp._sendToESP8266(txData)

    if(retData != None):
            if "OK\r\n" in retData or "ALREADY CONNECTED" in retData:
                pass
            else:
                raise Exception()
    else:
            raise Exception()
        

    
    txData='AT+CIPSEND='+str(len(NTP_QUERY))+"\r\n"
    esp._sendToESP8266(txData)

    esp.__uartObj.write(NTP_QUERY)
    utime.sleep(1)

    esp.__uartObj.read(38) #'b'\r\nRecv 48 bytes\r\n\r\nSEND OK\r\n\r\n+IPD,48:'
    utime.sleep(1)
    ntp_response = esp.__uartObj.read(48)  # NTP response is also 48 bytes
    esp._sendToESP8266('AT+CIPCLOSE\n\r')
    
    if "OK\r\n" in ntp_response:
        pass
    else:
        Exception()


    val = int.from_bytes(ntp_response[40:44], 'big')





    # 2024-01-01 00:00:00 converted to an NTP timestamp
    MIN_NTP_TIMESTAMP = 3913056000

    if val < MIN_NTP_TIMESTAMP:
        val += 0x100000000

    # Convert timestamp from NTP format to our internal format

    EPOCH_YEAR = utime.gmtime(0)[0]
    if EPOCH_YEAR == 2000:
        # (date(2000, 1, 1) - date(1900, 1, 1)).days * 24*60*60
        NTP_DELTA = 3155673600
    elif EPOCH_YEAR == 1970:
        # (date(1970, 1, 1) - date(1900, 1, 1)).days * 24*60*60
        NTP_DELTA = 2208988800
    else:
        raise Exception("Unsupported epoch: {}".format(EPOCH_YEAR))

    return val - NTP_DELTA


# There's currently no timezone support in MicroPython, and the RTC is set in UTC time.
def settime(esp):
    t = time(esp)
    import machine

    tm = utime.gmtime(t)
    machine.RTC().datetime((tm[0], tm[1], tm[2], tm[6] + 1, tm[3], tm[4], tm[5], 0))


__version__ = '0.1.1'
