try:
    import RPi.GPIO as GPIO   #Used to interface with hardware GPIO pins on RPi.
except:
    from GPIOEmulator.EmulatorGUI import GPIO #import RPi.GPIO as GPIO import time import traceback
    #If error occurs in VSCode, use "pip install GPIOEmulator to add package"

import time   #Simple time management library.
from threading import Thread   #Used for multithreading of program.
import logging   #Python logging facility for debugging and stuff

#Initiate logging
logging.basicConfig(
    filename='RPiLog.log',
    level=logging.DEBUG,
    format='%(asctime)s.%(msecs)03d %(levelname)s %(module)s - %(funcName)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
)
logging.info("Program initiating.")

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
    logging.debug("Setup complete.")


#Takes input of array of bytes, returns array of ascii chars.
def binary_to_ascii(input):
    output = []
    count = 0
    total = 0
    for i in input:
        for j in i:
            total += int(j)*pow(2, 7-count)
            count+=1
        output.append(chr(total))
        count = 0
        total = 0
    print(output)

#Takes input as string and returns array of binary bytes equiv to each char
def toBinary(a):
  l,m=[],[]
  for i in a:
    l.append(ord(i))
  for i in l:
    m.append(int(bin(i)[2:]))
  return m

#GPIO.input(channel)    #Return 0 or 1 (High or Low)
#GPIO.output(channel, state)    #Set channel to state.

def ptSensorInit():
    while True:
        tic = time.perf_counter()
        sigValue = GPIO.input(3)
        toc = time.perf_counter()
        print(f"time to poll sensor:\t {toc-tic:0.10f}")
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
