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
bitrate = 50 #bits per second or laser switches per second

#Identify GPIO pin association with hardware.
laser = 2
sensor = 3

#Function serves to set up hardware for RPi
def setupHardware():
    #Indicate to GPIO library to utilize Board Pin Designations
    GPIO.setmode(GPIO.BCM)

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
# I was very tired when writing this...
def toBinary(textArr):
    binaryArray = []
    binaryArray = "".join(format(ord(c), "b") for c in textArr)
    binaryArray = int(binaryArray)
    logging.info("From toBinary: Binary of payload is:\t" + str(binaryArray))
    binaryArray = [int(x) for x in str(binaryArray)]
    return binaryArray #Returns array of single bit elements.

def encode(binaryArray):   #Takes in array of single bit elements of type int
    changeMe = []
    #Aishik does his cool stuff here
    return changeMe   #Returns array of single bit elements of type int, but 4B5B style

#GPIO.input(channel)    #Return 0 or 1 (High or Low)
#GPIO.output(channel, state)    #Set channel to state.

def ptSensorInit():
    logging.info("ptSensorInit: Sensor Initialized.")
    while True:
        tic = time.perf_counter()
        sigValue = GPIO.input(3)
        toc = time.perf_counter()
        time.sleep(1)
        

initializeSensor = Thread(target= ptSensorInit)

#TODO: Add 4B5B Functionality shit
def sendData(str_message):
    print("Sending the following message: ", str_message)
    logging.info("sendData: message to be transmitted is:\t" + str(str_message))
    payload = toBinary(str_message)
    for i in range(len(payload)):
        GPIO.output(laser, payload[i])
        print("State should be:\t" + str(payload[i]))
        time.sleep(1/bitrate)
    GPIO.output(laser, 0) #Return transmitter to 0 at end.
    logging.info("sendData: Transmission complete. Killing thread.") 

GPIO.cleanup()  #Free up GPIO resources, return channels back to default.


#Main
setupHardware()
initializeSensor.start()

testMessage = "Hello World!"

while True:
    # consoleInput = str(input("Enter message to send or type quit: "))
    consoleInput = testMessage
    trSend = Thread(target = sendData, args=[consoleInput])
    trSend.start()

    time.sleep(6000)
