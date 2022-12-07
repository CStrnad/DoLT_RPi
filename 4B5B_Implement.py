#Takes input as string and returns array of binary bytes equiv to each char
# I was very tired when writing this...
def toBinary(textArr):
    binaryArray = []
    binaryArray = "".join(format(ord(c), "b") for c in textArr)
    binaryArray = int(binaryArray)
    # logging.info("From toBinary: Binary of payload is:\t" + str(binaryArray))
    binaryArray = [int(x) for x in str(binaryArray)]
    return binaryArray #Returns array of single bit elements.


#input needs to be multiple of 4 in length
def encode(binaryArray):   #Takes in array of single bit elements of type int
    chunk = ''
    chunk_list = []
    count = 0

    for i in binaryArray:
        if (count+1)%7 is 0:
            binaryArray.insert(count+1, 0)
        count += 1

    count = 0

    for i in binaryArray:
        chunk += str(i)
        if (count+1)%4 is 0:
            chunk_list.append(chunk)
            chunk = ''
        count += 1

    dictionary = {'0000' : '11110', '0001' : '01001', '0010' : '10100', '0011' : '10101', '0100' : '01010',\
                '0101' : '01011', '0110' : '01110', '0111' : '01111', '1000' : '10010', '1001' : '10011',\
                '1010' : '10110', '1011' : '10111', '1100' : '11010', '1101' : '11011', '1110' : '11100',\
                '1111' : '11101'}

    output_list = []
    for j in chunk_list:
        five_b = dictionary[j]
        for k in five_b:
            output_list.append(int(k))

    return output_list #Returns array of single bit elements of type int, but 4B5B style

#output must be multiple of 5
def decode(binaryArray):
    dictionary = {'0000' : '11110', '0001' : '01001', '0010' : '10100', '0011' : '10101', '0100' : '01010',\
                '0101' : '01011', '0110' : '01110', '0111' : '01111', '1000' : '10010', '1001' : '10011',\
                '1010' : '10110', '1011' : '10111', '1100' : '11010', '1101' : '11011', '1110' : '11100',\
                '1111' : '11101'}
    dictionary_correct = {v: k for k, v in dictionary.items()}

    chunk = ''
    chunk_list = []
    count = 0
    for i in binaryArray:
        chunk += str(i)
        if (count+1)%5 is 0:
            chunk_list.append(chunk)
            chunk = ''
        count += 1
    
    output_list = []
    for j in chunk_list:
        four_b = dictionary_correct[j]
        for k in four_b:
            output_list.append(int(k))

    for i in range(0, len(output_list)):
        if (i+1)%7 is 0:
            output_list.pop(i)
    return output_list


testInput = "Hello World!"
print("Message being converted:\t" + testInput)

binaryOfMessage = toBinary(testInput)
print("Binary of input:\t " + str(binaryOfMessage))

afterEncoding = encode(binaryOfMessage)
print("Encoded message:\t" + str(afterEncoding))

afterDecoding = decode(afterEncoding)
print("Decoded binary:\t" + str(afterDecoding))
