try:
    import RPi.GPIO as GPIO   #Used to interface with hardware GPIO pins on RPi.
except:
    from GPIOEmulator.EmulatorGUI import GPIO #import RPi.GPIO as GPIO import time import traceback
    #If error occurs in VSCode, use "pip install GPIOEmulator to add package"

import time   #Simple time management library.
from threading import Thread   #Used for multithreading of program.
import logging   #Python logging facility for debugging and stuff
import binascii
import numpy as np


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
def toBinary(a):
    l,m=[],[]
    for i in a:
        l.append(ord(i))
    for i in l:
        m.append(int(bin(i)[2:]))
    m_str = str(m[0])
    while len(m_str) < 8:
        m_str = "0" + m_str

    return m_str

dictionary = {'0000' : '11110', '0001' : '01001', '0010' : '10100', '0011' : '10101', '0100' : '01010',\
                '0101' : '01011', '0110' : '01110', '0111' : '01111', '1000' : '10010', '1001' : '10011',\
                '1010' : '10110', '1011' : '10111', '1100' : '11010', '1101' : '11011', '1110' : '11100',\
                '1111' : '11101'}

#input needs to be multiple of 4 in length
def encode(binaryArray):   #Takes in array of single bit elements of type int

    chunk = ''
    chunk_list = []

    count = 0
    for i in binaryArray:
        chunk += str(i)
        if (count+1)%4 == 0:
            chunk_list.append(chunk)
            chunk = ''
        count += 1
    # print(len(chunk_list))

    output_list = []
    for j in chunk_list:
        five_b = dictionary[j]
        for k in five_b:
            output_list.append(int(k))

    return output_list #Returns array of single bit elements of type int, but 4B5B style

#output must be multiple of 5
def decode(binaryArray):
    dictionary_correct = {v: k for k, v in dictionary.items()}

    chunk = ''
    chunk_list = []
    count = 0
    for i in binaryArray:
        chunk += str(i)
        if (count+1)%5 == 0:
            chunk_list.append(chunk)
            chunk = ''
        count += 1

    # 10101,01010,1010101010
    output_list = []
    for j in range(0, len(chunk_list)):
        #print(chunk_list[j])
        four_b = dictionary_correct[chunk_list[j]]
        
        #print(chunk_list[j])
        # if (j+1)%2 == 0:
        #     four_b = four_b[:-1]
        for k in four_b:
            output_list.append(k)

    #print(output_list)


    output_list2 = [0]*(len(output_list)-len(output_list)//8)
    j = 0
    #print(len(output_list))
    for i in range(0, len(output_list)):
        if ((i+1)%8 != 0):
            output_list2[i-j] = output_list[i]
        else:
            j += 1
 
    # print(output_list2)
    # return output_list

    # for i in range(0, len(output_list)):
    #     if (i+1)%8 == 0:
    #         output_list[i] = 'a'
    # output_list = [i for i in output_list if i != 'a']

    # new_output_list = []

    # for i in range(1, len(output_list)):
    #     if i % 8 != 0:

    return output_list

#Takes input of array of bytes, returns array of ascii chars.
def binary_to_ascii(input):
    output = []
    count = 0
    total = 0
    for i in input:
        total += int(i)*pow(2, 7-count)
        count+=1
        output.append(chr(total))
        count = 0
        total = 0
    print(output)

#GPIO.input(channel)    #Return 0 or 1 (High or Low)
#GPIO.output(channel, state)    #Set channel to state.





#yee
def ptSensorInit():
    logging.info("ptSensorInit: Sensor Initialized.")
     
    bits_total = 0
    count_int = 0 #number of interrupts received
    timestamps = [0]*(200) #timestamps
    period = 1/bitrate #length of one pulse in seconds
    bit_stream = [0]*(800) #recorded bits

    def receive_interrupt(sensor):
        print("Function triggered")
        n_pulses=0
        #check state of the sensor
        if not GPIO.input(sensor):
            state = 1
        else:
            state = 0

        nonlocal count_int, bits_total, timestamps, period, bit_stream
        #calculate time difference since last interrupt and approximate how many pulses passed
        timestamps[count_int] = time.perf_counter() #units = seconds
        if count_int != 0:
            time_diff = timestamps[count_int] - timestamps[count_int-1]
            n_pulses = round(time_diff/period)  #make sure units match
            bits_total = bits_total + n_pulses
            print(f'state= {state}, time_diff= {time_diff}, count_int= {count_int}, n_pulses= {n_pulses}, bits_total= {bits_total}')

        #print message if seen a postamble
        if (n_pulses>=9 and state==1):
            print('bit_stream: ', bit_stream)
            bits_decode = bit_stream[1:n_pulses]
            #print('timestamps: ', timestamps)

        #store bits in the bit_stream
        for i in range(n_pulses):
            bit_stream[bits_total-i] = state

        #update 
        count_int = count_int+1


    GPIO.add_event_detect(sensor, GPIO.BOTH, callback=receive_interrupt, bouncetime=1)
    # while True:
    #     t1 = time.perf_counter()
    #     sigValue = GPIO.input(3)
    #     t2 = time.perf_counter()
    #     print("Time to poll:\t" + str(t2-t1))
    #     #TODO: Add long ass array to catch all input. Need to make it fill and then start pruning end of array as the max size is reached.
    #     time.sleep(1/bitrate)



#The sensor is initiated above and will constantly take polls at the predefined bitrate that the sending function also uses. This should catch everything (fingers crossed)
#TODO: Identify start/stop bits and catch those.
#Pseudo Code follows:
""" From buffer, if start symbol detected:
    Create second buffer and append data following the start symbol
    Keep appending until -> stop symbol is detected:
        Once stop symbol detected, send captured 2nd buffer to be processed and clear main buffer """


        

initializeSensor = Thread(target= ptSensorInit)

#TODO: Add 4B5B Functionality shit
def sendData(str_message):
    print("Sending the following message: ", str_message)
    logging.info("sendData: message to be transmitted is:\t" + str(str_message))

    binaryOfMessage = ""
    for letter in str_message:
        binaryOfMessage += toBinary(letter)

    print("Binary of message:\t" + str(binaryOfMessage))
    encodedMessage = encode(binaryOfMessage)
    
    #Add preamble and postamble
    encodedArray = np.array(encodedMessage)
    preamble = np.array([1])
    postamble = np.array([1,1,1,1,1,1,1,1,1,1])

    withPre = np.append(preamble, encodedArray)
    payload = np.append(withPre, postamble)
    # print("Encoded message:\t"+ str(payload))

    print("Buffed payload:\t" + str(payload))
    for i in range(len(payload)):
        GPIO.output(laser, int(payload[i]))
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
