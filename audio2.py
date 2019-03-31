import scipy.io.wavfile
import numpy
from tqdm import tqdm
import time
import matplotlib.pyplot as plt
import sys
import wave

start = time.time()

foo = wave.open('16bitaudiomono.wav', 'rb')
channels = foo.getnchannels()
FS = foo.getframerate()
#print(channels)

def powmod(b, e, m):
		b2 = b                         
		res = 1                        
		while e:                       
			if e & 1:                  
				res = (res * b2) % m   
			b2 = (b2*b2) % m        
			e >>= 1                 
		return res


if(channels == 2):

	#Encryption


	fs, data = scipy.io.wavfile.read('16bitaudio.wav')
	print(data)
	print(fs)
	print(type(data))
	dataarray = data
	print(type(dataarray))
	a, b = dataarray.shape
	tup = (a, b)
	data = data.astype(numpy.int16)#16
	#data = numpy.asarray(data, dtype=numpy.int16)
	#print(data.flags)
	data.setflags(write=1)
	#print(data.flags)
	print((a,b))
	data1 = data
	data1.setflags(write=1)
	Time= numpy.linspace(0, len(data)/fs, num=len(data))
	plt.figure(1)
	plt.title('Signal Wave')
	plt.plot(Time, data) 
	plt.show()
	print('\n\ndata: ')
	print(data)

	posdata = numpy.where(data >= 0, data, -1)
	negdata = numpy.where(data <= 0, data, 1)
	print('\n\n')
	print(posdata)
	print('\n\n')
	print(negdata)
	print('\n\n')

	for i in range(0, tup[0]):
		for j in range(0, tup[1]):
			if(posdata[i][j]== -1 or negdata[i][j] < 0):
				x = negdata[i][j] 
				x = ((pow(x,3)) % 25777)
				negdata[i][j] = x
			elif(posdata[i][j]>0 or negdata[i][j] == 1):
				x = posdata[i][j] 
				x = ((pow(x,3)) % 25777)
				posdata[i][j] = x
			else:
				posdata[i][j] = 0
				negdata[i][j] = posdata[i][j]
			

	print('\n\n')
	print(posdata)
	print('\n\n')
	print(negdata)
	print('\n\n')
	data = data.astype(numpy.int16)#16
	scipy.io.wavfile.write('EN.wav', fs, posdata)
	scipy.io.wavfile.write('EN1.wav', fs, negdata)
	
	Time= numpy.linspace(0, len(data)/fs, num=len(data))
	plt.figure(2)
	plt.title('Encrypted Signal Wave')
	plt.plot(Time, data) 
	plt.show()
	
	
	
	#Decryption
	
	fs, data = scipy.io.wavfile.read('EN.wav')
	fs1, data1 = scipy.io.wavfile.read('EN1.wav')
	print(data)
	print(data1)
	print(type(data))
	dataarray = data
	print(type(dataarray))
	a1, b1 = dataarray.shape
	tup1 = (a1, b1)
	data = data.astype(numpy.int16)#16
	data1 = data1.astype(numpy.int16)
	#print(data.flags)
	data.setflags(write=1)
	data1.setflags(write=1)
	#print(data.flags)
	print((a1,b1))
	data= data.tolist()
	data1 = data1.tolist()
	
	for i1 in tqdm(range(len(data))):
		for j1 in (range(len(data[i1]))):
			if(data[i1][j1]==-1 or data1[i1][j1] < 0):
				x1 = data1[i1][j1] 
				x1 = powmod(x1, 16971, 25777)   #= ((pow(x1,16971)) % 25777)
				x1 = x1 - 25777
				data[i1][j1] = x1
			elif(data[i1][j1]>0 or data[i1][j1] == 1):
				x1 = data[i1][j1] 
				x1 = powmod(x1, 16971, 25777)   #= ((pow(x1,16971)) % 25777)
				data[i1][j1] = x1
			else:
				data[i1][j1] = 0
	data = numpy.array(data)
	data = data.astype(numpy.int16)
	print(data)
	scipy.io.wavfile.write('DE.wav', fs, data)

	end = time.time()
	ElspTime = (end-start)
	print('\n Sorry for taking %f sec from your life!', ElspTime)



else:
	binarySound = {}
	binaryHeader = {}

	song = {}

	#dt = numpy.dtype(int)
	#dt = dt.newbyteorder('>')
	#numpy.frombuffer(buffer, dtype=dt)

	with open("pcm0808m.wav",'rb') as f:
        	dt = numpy.dtype(int)
        	dt = dt.newbyteorder('>')
        	buffer = f.read(44)
        	#print(type(buffer))
        	binaryHeader = numpy.frombuffer(buffer,dtype=numpy.int16)
        	buffer = f.read()
        	binarySound = numpy.frombuffer(buffer,dtype=numpy.int16)
        	print(type(binarySound))
	print(binarySound)	
	#Encryption

	fs = FS
	data = binarySound
	print(data)
	print(fs)
	dataarray = data
	data = data.astype(numpy.int16)
	Time= numpy.linspace(0, len(data)/fs, num=len(data))
	plt.figure(1)
	plt.title('Original Signal Wave')
	plt.plot(Time, data) 
	plt.savefig('Original.png')
	
	posdata = numpy.where(data >= 0, data, -1)
	negdata = numpy.where(data <= 0, data, 1)

	for i in range(len(data)):
		if(posdata[i]== -1 or negdata[i]< 0):
			x = negdata[i]
			x = ((pow(x,3)) % 25777)
			negdata[i] = x
		elif(posdata[i]>0 or negdata[i] == 1):
			x = posdata[i]
			x = ((pow(x,3)) % 25777)
			posdata[i]= x
		else:
			posdata[i] = 0
			negdata[i] = posdata[i]
	print(posdata)
	print(negdata)
	#data = data.astype(numpy.int16)
	scipy.io.wavfile.write('EN.wav', fs, posdata)
	scipy.io.wavfile.write('EN1.wav', fs, negdata)

	Time= numpy.linspace(0, len(data)/fs, num=len(data))
	plt.figure(2)
	plt.title('Encrypted Signal Wave')
	plt.plot(Time, data) 
	#plt.show()
	plt.savefig('Encrypted.png')
	
	end = time.time()
	ElspTime = (end-start)
	print('\n Sorry for taking', +ElspTime, 'sec from your life!')
	
	
	#decryption
	
	binarySound = {}
	binaryHeader = {}
	
	song = {}
	
	#dt = numpy.dtype(int)
	#dt = dt.newbyteorder('>')
	#numpy.frombuffer(buffer, dtype=dt)
	
	with open("EN.wav",'rb') as f:
	        dt = numpy.dtype(int)
	        dt = dt.newbyteorder('>')
	        buffer = f.read(44)
	        #print(type(buffer))
	        binaryHeader = numpy.frombuffer(buffer,dtype=numpy.int16)
	        buffer = f.read()
	        binarySound = numpy.frombuffer(buffer,dtype=numpy.int16)
	        print(type(binarySound))
	print(binarySound)
	data = binarySound
	#fs, data = scipy.io.wavfile.read(askopenfilename())
	print(data)
	print(fs)
	
	with open("EN.wav",'rb') as f:
	        dt = numpy.dtype(int)
	        dt = dt.newbyteorder('>')
	        buffer = f.read(44)
	        #print(type(buffer))
	        binaryHeader = numpy.frombuffer(buffer,dtype=numpy.int16)
	        buffer = f.read()
	        binarySound = numpy.frombuffer(buffer,dtype=numpy.int16)
	        print(type(binarySound))
	print(binarySound)
	data1 = binarySound

	dataarray = data
	data = data.astype(numpy.int16)
	data= data.tolist()
	data1 = data1.tolist()
	
	for i1 in tqdm(range(len(data))):
		if(data[i1]==-1 or data1[i1] < 0):
			x1 = data1[i1] 
			x1 = powmod(x1, 16971, 25777)   #= ((pow(x1,16971)) % 25777)
			x1 = x1 - 25777
			data[i1] = x1
		elif(data[i1]>0 or data[i1] == 1):
			x1 = data[i1]
			x1 = powmod(x1, 16971, 25777)   #= ((pow(x1,16971)) % 25777)
			data[i1] = x1
		else:
			data[i1] = 0
	
	data = numpy.array(data)
	data = data.astype(numpy.uint8)
	print(data)
	scipy.io.wavfile.write('DE.wav', fs, data)
	
	end = time.time()
	ElspTime = (end-start)
	print('\n Sorry for taking', +ElspTime, 'sec from your life!')
	
	
	
	
	

