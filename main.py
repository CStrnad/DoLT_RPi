try:
    import RPI.GPIO as GPIO   #Used to interface with hardware GPIO pins on RPi.
except:
    from GPIOEmulator.EmulatorGUI import GPIO #import RPi.GPIO as GPIO import time import traceback
import time   #Simple time management library.
from threading import Thread   #Used for multithreading of program.

#Function serves to set up hardware for RPi
def setupHardware():
    #Indicate to GPIO library to utilize Board Pin Designations
    GPIO.setmode(GPIO.BCM)

    #Identify GPIO pin association with hardware.
    laser = 2
    sensor = 3

    #Define Pin-Interface mode
    GPIO.setup(sensor, GPIO.IN)  #Sensor Input
    GPIO.setup(laser, GPIO.OUT) #Laser interface

#GPIO.input(channel)    #Return 0 or 1 (High or Low)
#GPIO.output(channel, state)    #Set channel to state.

def ptSensorInit():
    while True:
        sigValue = GPIO.input(3)
        print(sigValue)
        time.sleep(1)

initializeSensor = Thread(target= ptSensorInit)

def sendData(str_message):
    print("Sending the following message: ", str_message)
    time.sleep(10)

GPIO.cleanup()  #Free up GPIO resources, return channels back to default.


#Main
setupHardware()
initializeSensor.start()
while True:
    consoleInput = input("Enter message to send or type quit: ")
    if (len(consoleInput)==4 and consoleInput == "quit"): break
    trSend = Thread(target = sendData, args=[consoleInput])
    trSend.start()

