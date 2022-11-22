#Begin file for DoLT Laser code.

import time
from time import sleep, gmtime
from gpiozero import LED, Button

led=LED(12)
sensor = Button(1)
time.gmtime(0)
led.blink(.1)

while True:
    if sensor.is_pressed:
        print("Strike", gmtime())
    sleep(0.5)