import socket
import machine
import time
from system.functions import oled_i2c

def serve():
    led = machine.Pin("LED", machine.Pin.OUT)
    oled_i2c.println("Specify IP:")
    ip = input('please enter the IP you want to host on... ')
    oled_i2c.println("Port,default=80:")
    port = int(input('please enter the Port you want to host on... Default is 80. '))
    oled_i2c.println('Filename host:')
    filename = input('please enter the filename of what you want to host. ')
    def blink_led():
        led.on()
        time.sleep(0.2)
        led.off()
        time.sleep(0.2)
 
    def get_html(html_name):
        with open(html_name, 'r') as file:
            html = file.read()
        return html

    addr = socket.getaddrinfo(ip, port)[0][-1]

    s = socket.socket()
    s.bind(addr)
    s.listen(1)

    print('Listening on', addr)
    oled_i2c.println('Listening:')
    oled_i2c.println(addr)

# Listen for connections
    while True:
        try:
            cl, addr = s.accept()
            print('Client connected from', addr)
            oled_i2c.println('Client connected')
            oled_i2c.println(addr)
            request = cl.recv(1024)
            print(request)
        
            request = str(request)
            led_on = request.find('?led=on')
            led_off = request.find('?led=off')
            led_blink = request.find('?led=blink')
            print('led_on = ', led_on)
            print('led_off = ', led_off)
            print('led_blink = ', led_blink)
            if led_on > -1:
                print('LED ON')
            led.on()
            
            if led_off > -1:
                print('LED OFF')
                led.off()
            
            if led_blink > -1:
                print('LED BLINK')
                blink_led()
            
            response = get_html(filename)
            cl.send('HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n')
            cl.send(response)
            cl.close()
        
        except OSError as e:
            cl.close()
            print('Connection closed')
