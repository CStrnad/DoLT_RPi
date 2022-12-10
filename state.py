import numpy as np
import time

#Both represent "Hello World!"
binaryArray = '010010000110010101101100011011000110111100100000011101110110111101110010011011000110010000100001' #binary of above.
encodedArray = [0, 1, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 1, 0, 1, 1, 1, 0, 1, 1, 0, 1, 0, 0, 1, 1, 1, 0, 1, 1, 0, 1, 0, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 0, 1, 0, 0, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 1, 1, 1, 0, 1, 1, 0, 1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 1]
insert = np.array([0,0,0,0,1,1,1,0,0,0,0,0,0])

#4B/5B start stop symbols per wikipedia
symbols = {'stop' : '11000', 'stop' : '01101', 'reset':'00111'}


new = np.array(encodedArray)
print(new)

updated = np.append(insert, encodedArray)
print(updated)

# for 

#Imitate signal coming in...
# buffer = np.empty((100,0), int)
buffer = []
print(buffer)
for i in updated:
    # np.append(buffer, updated[i], axis = 0)
    buffer.append(updated[i])
    #print("Buffer first 10 elements:\t" + str(buffer[i-5, i]))

    time.sleep(1)



# rows = int(new.size/5)
# print(rows)

# stupid = np.reshape(new, (rows, 7))
# print(stupid)
