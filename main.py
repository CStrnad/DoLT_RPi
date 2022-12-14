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
from time import perf_counter
import os
import matplotlib.pyplot as plt

global bitrate
bitrate = 4000 #bits per second or laser switches per second


def clear_console():
    try: os.system('clear')
    except: os.system('cls')

#Initiate logging
logging.basicConfig(
    filename='RPiLog.log',
    level=logging.DEBUG,
    format='%(asctime)s.%(msecs)03d %(levelname)s %(module)s - %(funcName)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
)
logging.info("Program initiating.")

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
    return output_list

def binary_to_ascii(binaryArray):
    binaryArray = ''.join(binaryArray)
    return binascii.unhexlify('%x' % int('0b' + binaryArray, 2)).decode("utf-8") 

def ptSensorInit():
    logging.info("ptSensorInit: Sensor Initialized.")

    expectedCharCount = 10000 
    expectedBitCount = expectedCharCount * 10
    bitStreamDesignator = expectedBitCount * 16
    phaseShift = 25

    bits_total = 0 #total received bits counter
    count_int = 0 #number of interrupts received
    period = 1/(bitrate-phaseShift) #length of one pulse in seconds
    timestamps = [0]*(expectedBitCount) #timestamps
    timing_error = [0]*(expectedBitCount) #pulse averaged bit time difference (from calculated with bitrate), synched with timestamps, used for timing stats analysis
    bit_stream = [0]*(bitStreamDesignator) #recorded bits
    done = 0

    def receive_interrupt(sensor):
        nonlocal count_int, bits_total, timestamps, period, bit_stream, done
        n_pulses = 0

        #check state of the sensor
        if not GPIO.input(sensor):
            state = 1
        else:
            state = 0
        
        #calculate time difference since last interrupt and approximate how many pulses passed
        timestamps[count_int] = time.perf_counter() #units = seconds
        if count_int != 0:
            time_diff = timestamps[count_int] - timestamps[count_int-1]
            n_pulses = round(time_diff/period)  #make sure units match
            bits_total = bits_total + n_pulses
            timing_error[count_int] = time_diff/n_pulses - 1/bitrate

        #process and display the message
        if done:
            GPIO.remove_event_detect(sensor) #stop interrupts
            bits_to_decode = bit_stream[2:(bits_total-10)] #remove pre- and postamble
            try: 
                decodedArray = decode(bits_to_decode)
                textArray = binary_to_ascii(decodedArray)
                clear_console()
                print("\nMessage Received:\n"+str(textArray))
            except: 
                clear_console()
                print("Error in decoding. Likely due to phasic latency.")
                pass
            
            plt.plot([(x-timestamps[2]) for x in timestamps[2:count_int]], timing_error[2:count_int])
            plt.xlabel('time /s')
            plt.ylabel('bit time inconsistency /us')
            plt.title(f'Bit time error (bitrate={bitrate})')
            plt.show(block=True)
            plt.draw()
            plt.savefig('time_stats')

            done = 0
            ptSensorInit()

        #print message if seen a postamble
        if (n_pulses>=9 and state==1):
            done = 1

        #store bits in the bit_stream
        for i in range(n_pulses):
            bit_stream[bits_total-i] = state

        #update interrupt counter
        count_int = count_int+1      

    try: GPIO.add_event_detect(sensor, GPIO.BOTH, callback=receive_interrupt) #bouncetime = 1 worked for bitrate of 50
    except: print("Ignore if working from PC. The detection function is not supported by the emulator.")

def sendData(str_message):
    print("Sending the following message: ", str_message)
    print("Pausing before sending. Length of message is " + str(len(str_message)) + " chars.")
    time.sleep(0.5)
    logging.info("sendData: message to be transmitted is:\t" + str(str_message))

    binaryOfMessage = ""
    for letter in str_message:
        binaryOfMessage += toBinary(letter)

    #print("Binary of message:\t" + str(binaryOfMessage))
    encodedMessage = encode(binaryOfMessage)
    
    #Add preamble and postamble
    encodedArray = np.array(encodedMessage)
    preamble = np.array([1])
    # postamble = np.array([1,1,1,1,1,1,1,1,1,1,0,1])
    postamble = np.array([1,1,1,1,1,1,1,1,1,1,0,1])

    withPre = np.append(preamble, encodedArray)
    payload = np.append(withPre, postamble)
    bitSizePayload = len(payload)
    # print("Encoded message:\t"+ str(payload))

    # print("Buffed payload:\t" + str(payload))
    sendTimeStart = time.perf_counter()
    for i in range(len(payload)):
        GPIO.output(laser, int(payload[i]))
        # print("State should be:\t" + str(payload[i]))
        sleep_time = 1/bitrate

        start_t = perf_counter()
        while (perf_counter()-start_t<sleep_time):
            continue


        #time.sleep(1/bitrate)
    GPIO.output(laser, 0) #Return transmitter to 0 at end.
    logging.info("sendData: Transmission complete. Killing thread.") 
    timeToSend = time.perf_counter() - sendTimeStart
    print("Send complete. Total time to send: " + str(timeToSend) + " at " + str(bitrate) + " bits per second. The payload is " + str(bitSizePayload) + " bits.")

#Main
setupHardware()

initializeSensor = Thread(target= ptSensorInit)


testMessage = "Hello World!"
testMessage2 = "If you're visiting this page, you're likely here because you're searching for a random sentence."
testMessage3 = "The unanimous Declaration of the thirteen united States of America, When in the Course of human events, it becomes necessary for one people to dissolve the political bands which have connected them with another, and to assume among the powers of the earth, the separate and equal station to which the Laws of Nature and of Nature's God entitle them, a decent respect to the opinions of mankind requires that they should declare the causes which impel them to the separation."
#testMessage3 is 474 chars
testMessage4 = """We hold these truths to be self-evident, that all men are created equal, that they are endowed by their Creator with certain unalienable Rights, that among these are Life, Liberty and the pursuit of Happiness.--That to secure these rights, Governments are instituted among Men, deriving their just powers from the consent of the governed, --That whenever any Form of Government becomes destructive of these ends, it is the Right of the People to alter or to abolish it, and to institute new Government, laying its foundation on such principles and organizing its powers in such form, as to them shall seem most likely to effect their Safety and Happiness. Prudence, indeed, will dictate that Governments long established should not be changed for light and transient causes; and accordingly all experience hath shewn, that mankind are more disposed to suffer, while evils are sufferable, than to right themselves by abolishing the forms to which they are accustomed. But when a long train of abuses and usurpations, pursuing invariably the same Object evinces a design to reduce them under absolute Despotism, it is their right, it is their duty, to throw off such Government, and to provide new Guards for their future security.--Such has been the patient sufferance of these Colonies; and such is now the necessity which constrains them to alter their former Systems of Government. The history of the present King of Great Britain is a history of repeated injuries and usurpations, all having in direct object the establishment of an absolute Tyranny over these States. To prove this, let Facts be submitted to a candid world."""
#testMessage4 is 2104 chars w/ whitespaces
testMessage5 = """It is a period of civil wars in the galaxy. A brave alliance of underground freedom fighters has challenged the tyranny and oppression of the awesome GALACTIC EMPIRE.

Striking from a fortress hidden among the billion stars of the galaxy, rebel spaceships have won their first victory in a battle with the powerful Imperial Starfleet. The EMPIRE fears that another defeat could bring a thousand more solar systems into the rebellion, and Imperial control over the galaxy would be lost forever.

To crush the rebellion once and for all, the EMPIRE is constructing a sinister new battle station. Powerful enough to destroy an entire planet, its completion spells certain doom for the champions of freedom.
"""
#testMessage5 is star wars intro crawl

transmissionMode = str(input("Choose from the following options:\n1) Transmit Mode\n2) Receive Mode\n3) Exit Program.\n"))
if(transmissionMode == "1"):
    functionality = "transmit"
    print("Entering Transmit Mode...")
elif(transmissionMode == "2"):
    functionality = "receive"
    print("Entering Receive Mode...")
    initializeSensor.start()
else:
    GPIO.cleanup()
    exit()

operate = True
while operate == True:
    clear_console()
    if(functionality == 'transmit'):
        print(
            "There are four preset options of text to be sent:\n" + 
            "1) Short message \"Hello World!\"\n" + 
            "2) Medium-Length Sentence\n" + 
            "3) Long message: Beginning of Declaration of Independance\n" + 
            "4) Long message: Star wars intro craw\n"
        )

        userInput = str(input("Choose from the following:\n1) Short Message\n2) Sentence\n3) Long Message\n4) Star Wars Intro Crawl\n5) Custom message\n6)Quit.\n"))
        if(userInput == '1'):
            trSend = Thread(target = sendData, args=[testMessage])
            trSend.start()
        elif(userInput == '2'):
            trSend = Thread(target = sendData, args=[testMessage2])
            trSend.start()
        elif(userInput == '3'):
            trSend = Thread(target = sendData, args=[testMessage3])
            trSend.start()
        elif(userInput == '4'):
            trSend = Thread(target = sendData, args=[testMessage5])
            trSend.start()
        elif(userInput == '5'):
            customString = input("\nEnter custom text:\n")
            trSend = Thread(target = sendData, args=[customString])
            trSend.start()
        else:
            print("Quitting...")
            operate = False
            GPIO.cleanup()  #Free up GPIO resources, return channels back to default.
            exit()

        while(trSend.is_alive()):
            time.sleep(0.1)
        input("Press any key to continue...")

    elif(functionality == 'receive'):
        clear_console()
        print("Ready to receive data.")
        input("Press any key to quit...")
        GPIO.cleanup()
        exit()