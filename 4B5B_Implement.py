#Takes input as string and returns array of binary bytes equiv to each char
# I was very tired when writing this...
def toBinary(textArr):
    binaryArray = []
    binaryArray = "".join(format(ord(c), "b") for c in textArr)
    binaryArray = int(binaryArray)
    # logging.info("From toBinary: Binary of payload is:\t" + str(binaryArray))
    binaryArray = [int(x) for x in str(binaryArray)]
    return binaryArray #Returns array of single bit elements.

def encode(binaryArray):   #Takes in array of single bit elements of type int
    changeMe = []
    #Aishik does his cool stuff here
    return changeMe   #Returns array of single bit elements of type int, but 4B5B style

testInput = "Hello World!"
print("Message being converted:\t" + testInput)

binaryOfMessage = toBinary(testInput)
print("Binary of input:\t " + str(binaryOfMessage))

afterEncoding = encode(binaryOfMessage)
print("Encoded message:\t" + str(afterEncoding))