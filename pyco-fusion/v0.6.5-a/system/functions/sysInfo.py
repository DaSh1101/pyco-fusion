import machine
import utime
from system.functions import oled_i2c

def temp():
    sensor = machine.ADC(4)
    factor = 3.3 / (65535)
    reading = sensor.read_u16() * factor
    temperature = 27 - (reading - 0.706) / 0.001721
    rounded_temperature = round(temperature, 1)
    print("%.1f" % temperature)
    oled_i2c.println('%.1f' % temperature)
