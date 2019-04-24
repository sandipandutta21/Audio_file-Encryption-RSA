import scipy.io.wavfile
import numpy
from tqdm import tqdm
import time
import matplotlib.pyplot as plt
import sys
import wave
from tkinter.filedialog import askopenfilename
from tkinter.ttk import *
from tkinter import *
from tkinter import filedialog
import random 


#TODO random.randint() from Enaudio.py 

audio_window = Tk()
audio_window.geometry ( '360x200' )
audio_window.title ('Audio Cryptography')

def goback():
	exit()

def powmod(b, e, m):
	b2 = b                         
	res = 1                        
	while e:                       
		if e & 1:                  
			res = (res * b2) % m   
		b2 = (b2*b2) % m        
		e >>= 1                 
	return res

def filenameerror():
	messagebox.showinfo('Error Occured!', 'Please select a 8bit/16bit mono or stereo audio file')

def enfinish16():
	messagebox.showinfo('Done!', 'Encryption is Finished and saved as NEG.wav and POS.wav ')

def enfinish8():
	messagebox.showinfo('Done!', 'Encryption is Finished and saved as EN.wav')

def definish():
	messagebox.showinfo('Done!', 'Decryption is finished and saved as DE.wav')
	

def sixteen_encrypt():
	
	try:
			start = time.time()
			filename = askopenfilename()
			foo = wave.open(filename, 'rb')
			channels = foo.getnchannels()
			FS = foo.getframerate()
			#print(channels)

			if(channels == 2): #stereo

				#Encryption


				fs, data = scipy.io.wavfile.read(filename)
				print('The original data: \n',+data)
				print('The frame rate: ',+fs)
				#print(type(data))
				a, b = data.shape
				tup = (a, b)
				data = data.astype(numpy.int16)#16
				#data = numpy.asarray(data, dtype=numpy.int16)
				#print(data.flags)
				data.setflags(write=1)
				#print(data.flags)
				#print((a,b))
				Time= numpy.linspace(0, len(data)/fs, num=len(data))
				print(type(Time))
				plt.figure(1)
				plt.title('Original Signal Wave')
				plt.plot(Time, data) 
				plt.savefig('Original.png')

				posdata = []
				negdata = []
				data_list = data.tolist()
				posdata = data_list
				negdata = data_list
				posdata = numpy.array(posdata).astype(numpy.int16)
				negdata = numpy.array(negdata).astype(numpy.int16)

				#for posdata:
				for z in range(len(data)):
					for q in range(len(data[z])):
						if(data[z][q]<0):
							posdata[z][q] = random.randint(-30000, -20000)
						elif(data[z][q]>0):
							posdata[z][q] = data[z][q]
						else:
							posdata[z][q] = 0
					
				#for negdata:
				for m in range(len(data)):
					for r in range(len(data[r])):
						if(data[m][r]>0):
							negdata[m][r] = random.randint(20000, 30000)
						elif(data[m][r]<0):
							negdata[m][r] = data[m][r]
						else:
							negdata[m][r] = 0

				#posdata = numpy.where(data >= 0, data, -1) #-25777 -(n)
				#negdata = numpy.where(data <= 0, data, 1) #25777 (n)
				print('The array made from the possitive datas: \n',+posdata)
				print('The array made from the negativetive datas: \n',+negdata)

				for i in range(0, tup[0]):
					for j in range(0, tup[1]):
						if(posdata[i][j]<0 or negdata[i][j] < 0):
							x = negdata[i][j] 
							x = ((pow(x,3)) % 25777)
							negdata[i][j] = x
						elif(posdata[i][j]>0 or negdata[i][j]>0):
							x = posdata[i][j] 
							x = ((pow(x,3)) % 25777)
							posdata[i][j] = x
						else:
							posdata[i][j] = 0
							negdata[i][j] = posdata[i][j]
						

				print('\n Encrypted positive array:')
				print(posdata)
				print('\n Encrypted positive array:')
				print(negdata)
				print('\n')
				scipy.io.wavfile.write('Pos.wav', fs, posdata)
				scipy.io.wavfile.write('Neg.wav', fs, negdata)
				
				Time= numpy.linspace(0, len(posdata)/fs, num=len(posdata))
				plt.figure(2)
				plt.title('Encrypted Signal Wave')
				plt.plot(Time, posdata) 
				plt.savefig('posdata.png')
				
				Time= numpy.linspace(0, len(negdata)/fs, num=len(negdata))
				plt.figure(3)
				plt.title('Encrypted Signal Wave')
				plt.plot(Time, negdata) 
				plt.savefig('negdata.png')
				
				end = time.time()
				ElspTime = (end-start)
				print('\n Sorry for taking', +ElspTime, 'sec from your life!')

			else: #mono

				binarySound = {}
				binaryHeader = {}

				song = {}

				#dt = numpy.dtype(int)
				#dt = dt.newbyteorder('>')
				#numpy.frombuffer(buffer, dtype=dt)

				with open(filename,'rb') as f:
					dt = numpy.dtype(int)
					dt = dt.newbyteorder('>')
					buffer = f.read(44)
					#print(type(buffer))
					binaryHeader = numpy.frombuffer(buffer,dtype=numpy.int16) #TODO remove the file header 
					buffer = f.read()
					binarySound = numpy.frombuffer(buffer,dtype=numpy.int16)	
				#Encryption

				fs = FS
				data = binarySound
				print('The original data: \n',+data)
				print('The frame rate: ',+fs)

				Time= numpy.linspace(0, len(data)/fs, num=len(data))
				plt.figure(1)
				plt.title('Original Signal Wave')
				plt.plot(Time, data) 
				plt.savefig('Original.png')
				
				posdata = []
				negdata = []
				data_list = data.tolist()
				posdata = data_list
				negdata = data_list
				posdata = numpy.array(posdata).astype(numpy.int16)
				negdata = numpy.array(negdata).astype(numpy.int16)
				
				#for posdata:
				for z in range(len(data)):
					if(data[z]<0):
						posdata[z] = random.randint(-30000, -20000)
					elif(data[z]>0):
						posdata[z] = data[z]
					else:
						posdata[z] = 0
				
				#for negdata:
				for m in range(len(data)):
					if(data[m]>0):
						negdata[m] = random.randint(20000, 30000)
					elif(data[m]<0):
						negdata[m] = data[m]
					else:
						negdata[m] = 0

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
				print('\n Encrypted positive array:')
				print(posdata)
				print('\n Encrypted positive array:')
				print(negdata)
				print('\n')

				scipy.io.wavfile.write('Pos.wav', fs, posdata)
				scipy.io.wavfile.write('Neg.wav', fs, negdata)

				Time= numpy.linspace(0, len(posdata)/fs, num=len(posdata))
				plt.figure(2)
				plt.title('Posdata Wave')
				plt.plot(Time, posdata) 
				#plt.show()
				plt.savefig('posdata.png')

				Time= numpy.linspace(0, len(negdata)/fs, num=len(negdata))
				plt.figure(3)
				plt.title('Negdata Wave')
				plt.plot(Time, negdata) 
				#plt.show()
				plt.savefig('negdata.png')
				
				end = time.time()
				ElspTime = (end-start)
				print('\n Sorry for taking', +ElspTime, 'sec from your life!')
			
			enfinish16()
	except TypeError:
		filenameerror()

	except AttributeError:
		filenameerror()

def eight_encrypt():

	try:

			start = time.time()

			filename = askopenfilename() 
			foo = wave.open(filename, 'rb')
			channels = foo.getnchannels()
			FS = foo.getframerate()

			if(channels == 2):

				#Encryption

				fs, data = scipy.io.wavfile.read(filename)
				print(data)
				print(fs)
				dataarray = data
				a, b = dataarray.shape
				tup = (a, b)
				data = data.astype(numpy.int16)
				#data = numpy.asarray(data, dtype=numpy.int16)
				#print(data.flags)
				data.setflags(write=1)
				#print(data.flags)
				print((a,b))

				Time= numpy.linspace(0, len(data)/fs, num=len(data))
				plt.figure(1)
				plt.title('Original Signal Wave')
				plt.plot(Time, data) 
				#plt.show()
				plt.savefig('Original.png')

				for i in range(0, tup[0]):
					for j in range(0, tup[1]):
						x = data[i][j] 
						x = ((pow(x,3)) % 25777)
						data[i][j] = x

				print(data)
				data = data.astype(numpy.int16)
				scipy.io.wavfile.write('EN.wav', fs, data)

				Time= numpy.linspace(0, len(data)/fs, num=len(data))
				plt.figure(2)
				plt.title('Encrypted Signal Wave')
				plt.plot(Time, data) 
				#plt.show()
				plt.savefig('Encrypted.png')

				end = time.time()
				ElspTime = (end-start)
				print('\n Sorry for taking', +ElspTime, 'sec from your life!')

			else:
				binarySound = {}
				binaryHeader = {}

				song = {}

				#dt = numpy.dtype(int)
				#dt = dt.newbyteorder('>')
				#numpy.frombuffer(buffer, dtype=dt)

				with open(filename,'rb') as f:
					dt = numpy.dtype(int)
					dt = dt.newbyteorder('>')
					buffer = f.read(44)
					#print(type(buffer))
					binaryHeader = numpy.frombuffer(buffer,dtype=numpy.uint8)
					buffer = f.read()
					binarySound = numpy.frombuffer(buffer,dtype=numpy.uint8)
					print(type(binarySound))
				print(binarySound)

				start = time.time()

				#Encryption

				fs = 8000 #, data = scipy.io.wavfile.read(askopenfilename())
				data = binarySound
				print(data)
				print(fs)
				#print(type(data))
				dataarray = data
				#print(type(dataarray))
				#a, b = dataarray.shape
				#tup = (a, b)
				data = data.astype(numpy.int16)
				#data = numpy.asarray(data, dtype=numpy.int16)
				#print(data.flags)
				#data.setflags(write=1)
				#print(data.flags)
				#print((a,b))

				Time= numpy.linspace(0, len(data)/fs, num=len(data))
				plt.figure(1)
				plt.title('Original Signal Wave')
				plt.plot(Time, data) 
				#plt.show()
				plt.savefig('Original.png')

				for i in range(len(data)):
					#for j in range(0, tup[1]):
					x = data[i] 
					x = ((pow(x,3)) % 25777)
					data[i] = x

				print(data)
				data = data.astype(numpy.int16)
				scipy.io.wavfile.write('EN.wav', fs, data)

				Time= numpy.linspace(0, len(data)/fs, num=len(data))
				plt.figure(2)
				plt.title('Encrypted Signal Wave')
				plt.plot(Time, data) 
				#plt.show()
				plt.savefig('Encrypted.png')

				end = time.time()
				ElspTime = (end-start)
				print('\n Sorry for taking', +ElspTime, 'sec from your life!')
			enfinish8()

	except TypeError:
		filenameerror()

	except AttributeError:
		filenameerror()


def sixteen_decrypt():

	try:
 
			file11 = askopenfilename()
			file22 = askopenfilename()
			file1 = wave.open(file11, 'rb')
			file2 = wave.open(file22, 'rb')
			channel1 = file1.getnchannels()
			FS1 = file1.getframerate()
			channel2 = file2.getnchannels()
			FS2 = file2.getframerate()
			#print(channels)
			start = time.time()

			#TODO if() exception handling of another file format 

			if(channel1 == 2): #stereo #TODO check if channel1==channel2 #TODO exception handling of selecting 2 diff file

				#Decryption
					
				fs, data = scipy.io.wavfile.read(file11)
				fs1, data1 = scipy.io.wavfile.read(file22)
				print('The first file:\n', +data)
				print('The second file:\n', +data1)
				#print(type(data))
				#print(type(dataarray))
				a1, b1 = data.shape
				tup1 = (a1, b1)
				data = data.astype(numpy.int16)#16
				data1 = data1.astype(numpy.int16)
				#print(data.flags)
				data.setflags(write=1)
				data1.setflags(write=1)
				#print(data.flags)
				#print((a1,b1))
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
				data = numpy.array(data).astype(numpy.int16)
				#data = data.astype(numpy.int16)
				print('The original data: \n',+data)
				scipy.io.wavfile.write('DE.wav', fs, data)

				end = time.time()
				ElspTime = (end-start)
				print('\n Sorry for taking ', +ElspTime, 'sec from your life!')

			else:

				#decryption	
					
				binarySound = {}
				binaryHeader = {}
				
				#song = {}
				
				#dt = numpy.dtype(int)
				#dt = dt.newbyteorder('>')
				#numpy.frombuffer(buffer, dtype=dt)
				
				with open(file11,'rb') as f:
					dt = numpy.dtype(int)
					dt = dt.newbyteorder('>')
					buffer = f.read(44)
					#print(type(buffer))
					binaryHeader = numpy.frombuffer(buffer,dtype=numpy.int16) #TODO remove the file header 
					buffer = f.read()
					binarySound = numpy.frombuffer(buffer,dtype=numpy.int16)
				data = binarySound
				#fs, data = scipy.io.wavfile.read(askopenfilename())
				print('The first file:\n', +data)
				#print(fs)
				
				with open(file22,'rb') as f:
					dt = numpy.dtype(int)
					dt = dt.newbyteorder('>')
					buffer = f.read(44)
					#print(type(buffer))
					binaryHeader = numpy.frombuffer(buffer,dtype=numpy.int16) #TODO remove the file header 
					buffer = f.read()
					binarySound = numpy.frombuffer(buffer,dtype=numpy.int16)
				data1 = binarySound
				print('The second file:\n', +data1)

				data= data.tolist()
				data1 = data1.tolist()
		
				for i1 in tqdm(range(len(data))):
					if(data[i1]==-1 or data1[i1] < 0):
						x1 = data1[i1] 
						x1 = powmod(x1, 16971, 25777)   #= ((pow(x1,16971)) % 25777)
						x1 = x1 - 25777
						data[i1] = x1
					elif(data[i1]>0 or data1[i1] == 1):
						x1 = data[i1]
						x1 = powmod(x1, 16971, 25777)   #= ((pow(x1,16971)) % 25777)
						data[i1] = x1
					else:
						data[i1] = 0
				
				data = numpy.array(data)
				data = data.astype(numpy.int16)
				print('The original data: \n', +data)
				scipy.io.wavfile.write('DE.wav', FS1, data)
				
				end = time.time()
				ElspTime = (end-start)
				print('\n Sorry for taking', +ElspTime, 'sec from your life!')
				############ finish of decryption ##############
			definish()
	except TypeError:
		filenameerror()

	except AttributeError:
		filenameerror()

def eight_decrypt():

	try:

			filename = askopenfilename()
			foo = wave.open(filename, 'rb')
			channels = foo.getnchannels()
			FS = foo.getframerate()
			start = time.time()

			if(channels == 2):


				#Decryption
				fs, data = scipy.io.wavfile.read(filename)
				print(data)
				print(fs)
				#print(type(data))
				dataarray = data
				#print(type(dataarray))
				a1, b1 = dataarray.shape
				tup1 = (a1, b1)
				data = data.astype(numpy.int16)
				#print(data.flags)
				data.setflags(write=1)
				#print(data.flags)
				print((a1,b1))
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
				print('\n Sorry for taking', +ElspTime, 'sec from your life!')

			else:				
				binarySound = {}
				binaryHeader = {}

				song = {}

				#dt = numpy.dtype(int)
				#dt = dt.newbyteorder('>')
				#numpy.frombuffer(buffer, dtype=dt)

				with open(filename,'rb') as f:
					dt = numpy.dtype(int)
					dt = dt.newbyteorder('>')
					buffer = f.read(44)
					#print(type(buffer))
					binaryHeader = numpy.frombuffer(buffer,dtype=numpy.uint8)
					buffer = f.read()
					binarySound = numpy.frombuffer(buffer,dtype=numpy.uint8)
					print(type(binarySound))
				print(binarySound)
				print(data)
				print(fs)
				dataarray = data
				data = data.astype(numpy.int16)
				data= data.tolist()
			
				for i1 in tqdm(range(len(data))):
					#for j1 in (range(len(data[i1]))):
					x1 = data[i1] 
					x1 = (pow(x1, 16971)%25777)
					data[i1] = x1

				data = numpy.array(data)
				data = data.astype(numpy.uint8)
				print(data)
				scipy.io.wavfile.write('DE.wav', fs, data)

				end = time.time()
				ElspTime = (end-start)
				print('\n Sorry for taking', +ElspTime, 'sec from your life!')

			definish()

	except TypeError:
		filenameerror()

	except AttributeError:
		filenameerror()

btn_16_decrypt = Button( audio_window, text = "16bit Audio Decryption", command = sixteen_decrypt)
btn_16_decrypt.place( x=10, y=100 )
btn_8_decrypt = Button( audio_window, text = "8bit Audio Decryption", command = eight_decrypt)
btn_8_decrypt.place( x=180, y=100 )
btn_8_encrypt = Button( audio_window, text = "8bit Audio Decryption", command = eight_encrypt)
btn_8_encrypt.place( x=180, y=50 )
btn_16_encrypt = Button( audio_window, text = "16bit Audio Encryption", command = sixteen_encrypt)
btn_16_encrypt.place( x=10, y=50 )
btn_exit = Button( audio_window, text = "Go Back" , command = goback).place( x=140, y=150 )

audio_window.mainloop()



