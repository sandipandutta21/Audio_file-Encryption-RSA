import scipy.io.wavfile
import numpy
from tqdm import tqdm
import time
import matplotlib.pyplot as plt
import sys

start = time.time()

#Decryption

fs, data = scipy.io.wavfile.read('EN.wav')
print(data)
print(fs)
print(type(data))
dataarray = data
print(type(dataarray))
a1, b1 = dataarray.shape
tup1 = (a1, b1)
data = data.astype(numpy.int16)
#print(data.flags)
data.setflags(write=1)
#print(data.flags)
print((a1,b1))
numpy.savetxt('txtaudio.txt', data)
data= data.tolist()

for i1 in tqdm(range(len(data))):
	for j1 in (range(len(data[i1]))):
		x1 = data[i1][j1] 
		x1 = (pow(x1, 16971)%25777)
		data[i1][j1] = x1

data = numpy.array(data)
data = data.astype(numpy.uint8)
print(data)
scipy.io.wavfile.write('DE.wav', fs, data)

end = time.time()
ElspTime = (end-start)
print('\n Sorry for taking %f sec from your life!', +ElspTime)
