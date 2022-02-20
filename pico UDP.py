from machine import Pin, UART
import utime
uart0 = UART(0,baudrate=115200,rx=Pin(1),tx=Pin(0))
LED = Pin(25,Pin.OUT)
LED.value(0)
SSID = "Telecentro-3e0f"
PASSWORD = "7QHCAC3HCMYA"
UDP = '"UDP"'
DIRUDP = '"0.0.0.0"'
def sendCMD_waitResp(cmd, uart=uart0, timeout=2000):
    print("CMD: " + cmd)
    uart.write(cmd)
    waitResp(uart, timeout)
    print()   
def waitResp(uart=uart0, timeout=2000):
    prvMills = utime.ticks_ms()
    resp = b""
    while (utime.ticks_ms()-prvMills)<timeout:
        if uart.any():
            resp = b"".join([resp, uart.read(1)])
    print("resp:")
    try:
        print(resp.decode())
    except UnicodeError:
        print(resp)
def waitResp_command(uart=uart0, timeout=2000):
    salida = ""
    prvMills = utime.ticks_ms()
    resp = b""
    while (utime.ticks_ms()-prvMills)<timeout:
        if uart.any():
            resp = b"".join([resp, uart.read(1)])
    print("resp:")
    try:
        print(resp.decode())
        salida = resp.decode()
    except UnicodeError:
        print(resp)
    return salida
def ConnectToWiFi():
    sendCMD_waitResp("AT+RST\r\n")
    utime.sleep(5)
    
    sendCMD_waitResp("AT+CWMODE=1\r\n")
    utime.sleep(1)
    
    send = "AT+CWJAP=\""+SSID+"\",\""+PASSWORD+"\""
    sendCMD_waitResp(send+'\r\n')
    utime.sleep(7)
    
    sendCMD_waitResp("AT+CPIMUX=0\r\n")
    utime.sleep(3)
    
    sendCMD_waitResp("AT+CIFSR\r\n")
    utime.sleep(3)
    
    send = "AT+CIPSTART=" + UDP + "," + DIRUDP + ",5000,5000,2"
    sendCMD_waitResp(send+'\r\n')
    utime.sleep(3)
    
ConnectToWiFi()

while True:
    dat = waitResp_command()
    n = dat.find("LON")
    if n > 0:
        LED.value(1)
    n = dat.find("LOFF")
    if n > 0:
        LED.value(0)