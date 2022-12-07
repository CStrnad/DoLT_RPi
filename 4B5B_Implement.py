#Takes input as string and returns array of binary bytes equiv to each char
# def toBinary(textArr):
#     binaryArray = []
#     print("".join(format(ord(c), "b") for c in textArr)) #print unpadded
#     print(len("".join(format(ord(c), "b") for c in textArr)))
#     binaryArray = "".join((format(ord(c), "b")+'0') for c in textArr)
#     binaryArray = int(binaryArray)
#     binaryArray = [int(x) for x in str(binaryArray)]
#     return binaryArray #Returns array of single bit elements.
import binascii

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


binaryOfMessage = ""

def binary_to_ascii(binaryArray):
    return binascii.unhexlify('%x' % int('0b' + binaryArray, 2)).decode("utf-8") 

testInput = "helloworld"
for letter in testInput:
    binaryOfMessage += toBinary(letter)

afterEncoding = encode(binaryOfMessage)

#print("Encoded message:\t" + str(afterEncoding))

afterDecoding = decode(afterEncoding)

print("Decoded binary:\t " + str(afterDecoding))



print("Ascii After Encode/Decode:\t " + binary_to_ascii(''.join(afterDecoding)))
