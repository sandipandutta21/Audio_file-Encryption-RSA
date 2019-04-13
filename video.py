import cv2
import numpy
import os
#import moviepy.editor as mp
import imageio 
import time
from tkinter.filedialog import askopenfilename
from tkinter.ttk import *
from tkinter import *
from tkinter import filedialog
from tqdm import tqdm 
from tkinter import messagebox
import subprocess

video_window = Tk()
video_window.geometry ( '350x200' )
video_window.title ('Video Encryption')

start = time.time()

endata = './data'
dedata = './Endata'
dedata2 = './Dedata'

def encrypt():
	load_image_encrypt(endata)

def decrypt():
	load_image_decrypt(endata)

#try:
#	if not os.path.exists('Endata'):
#		os.makedirs('Endata')
#except OSError:
#    	messagebox.showinfo('Error Occured', 'Error: Creating directory of encrypted data')

def load_image_encrypt(folder):
	
	videofile = askopenfilename()
	
	try:
		if not os.path.exists('Endata'):
			os.makedirs('Endata')
	except OSError:
		messagebox.showinfo('Error Occured', 'Error: Creating directory of encrypted data')

	name = './data/frame'
	vid_to_image(name,videofile)

	for filename1 in tqdm(os.listdir(folder)):
		imgV = cv2.imread(os.path.join(folder, filename1))
		if imgV is not None:
			RGBencryption(imgV, filename1)
		else:
			break
	vidname = 'envid.avi'
	image_to_vid(dedata, vidname)

	messagebox.showinfo('Finish!', 'Encryption Done succesfully!')

def load_image_decrypt(folder):

	videofile = askopenfilename()

	try:
		if not os.path.exists('Dedata'):
			os.makedirs('Dedata')
	except OSError:
		messagebox.showinfo('Error Occured', 'Error: Creating directory of decrypted data')
	
	try:
		if not os.path.exists('Dedata1'):
			os.makedirs('Dedata1')
	except OSError:
		messagebox.showinfo('Error Occured', 'Error: Creating directory of decrypted data')

	name = './data/frame'
	vid_to_image(name, videofile)

	for filename1 in tqdm(os.listdir(folder)):
		imgV = imageio.imread(os.path.join(folder, filename1))
		if imgV is not None:
			RGBdecryption(imgV, filename1)
		else:
			break
	
	vidname = 'devid.avi'
	image_to_vid(dedata2, vidname)

	messagebox.showinfo('Finish!', 'Decryption Done succesfully!')

def RGBencryption(img, filename):
	
	img = img.astype(numpy.uint16)
	a = img.shape
	img= img.tolist()

	for i in (range(len(img))):
		for j in (range(len(img[i]))):
			for k in (range(len(img[i][j]))):
				x = img[i][j][k] 
				x = (pow(x,3)%25777)
				img[i][j][k] = x
	img = numpy.array(img).astype(numpy.uint16)
	name = './Endata/'+str(filename)
	imageio.imwrite(name, img, format='PNG-FI')


def powmod(b, e, m):

	b2 = b
	res = 1
	while e:
		if e & 1:
			res = (res * b2) % m
		b2 = (b2*b2) % m
		e >>= 1
	return res

def RGBdecryption(img, filename):

	#print('\n\nReading Encrypted Image again:\n\n')
	#print(img1)
	img1 = img
	img = img.astype(numpy.uint16)
	img1= img1.tolist()
	#print('Decrypting....')

	for i1 in tqdm(range(len(img1))):
		for j1 in (range(len(img1[i1]))):
			for k1 in (range(len(img1[i1][j1]))):
				x1 = img1[i1][j1][k1] 
				x1 = powmod(x1,16971,25777)
				img1[i1][j1][k1] = x1

	img1 = numpy.array(img1).astype(numpy.uint16)#.reshape(184,275)
	#print('\n\nDecrypted Image:\n\n')
	#print(img1)
	name = './Dedata1/'+str(filename)
	imageio.imwrite(name, img1, format='PNG-FI')
	#cv2.imwrite(name, img1)


#clip = mp.VideoFileClip("video.mp4")
#clip.audio.write_audiofile("theaudio.wav")


def vid_to_image(foldername ,filename):
	# Playing video from file:
	cap = cv2.VideoCapture(filename)

	try:
		if not os.path.exists('data'):
			os.makedirs('data')
		messagebox.showinfo('Info!', 'Data directory is created where the frames are stored')
	
	except OSError:
	    	print ('Error: Creating directory of data')

	currentFrame = 0
	while(True):
	    # Capture frame-by-frame
		ret, frame = cap.read()
		if not ret: 
			break

	    # Saves image of the current frame in jpg file
		name = foldername + str(currentFrame) + '.png'
		print ('Creating...' + name)
		imageio.imwrite(name, frame,format='PNG-FI')

	    # To stop duplicate images
		currentFrame += 1
	    	
	# When everything done, release the capture
	cap.release()
	cv2.destroyAllWindows()

def get_frame_rate(filename):

	cap = cv2.VideoCapture(filename)
	fps = cap.get(cv2.CAP_PROP_FPS)
	return fps

def image_to_vid(folder, vidname):  
	
	image_folder = folder
	video_name = vidname
	sort_image = []
	images = [img for img in os.listdir(image_folder) if img.endswith(".png")]
	print(images)
	print('\n\n')

	for i in range(0,1000):
		for j in range(len(images)):
			name = 'frame' + str(i) + '.png' 
			if ((str(images[j])) == str(name)):
				sort_image.append(images[j])
				
	print(sort_image)
	frame = cv2.imread(os.path.join(image_folder, sort_image[0]))
	height, width, layers = frame.shape

	video = cv2.VideoWriter(video_name, 0, 29, (width,height))

	for image in sort_image:
	    video.write(cv2.imread(os.path.join(image_folder, image)))

	cv2.destroyAllWindows()
	video.release() 

		
def goback():
	exit()

btn_select_img = Button( video_window, text = "Go Back" , command = goback)
btn_select_img.place( x=140, y=150 )

btn_encrypt = Button( video_window, text = "Encrypt Video" , command = encrypt)
btn_encrypt.place( x=20, y=100 )

btn_decrypt = Button( video_window, text = "Decrypt Video" , command = decrypt)
btn_decrypt.place( x=200, y=100 )

video_window.mainloop()

#end = time.time()
#eTime = end - start
#print(eTime)

