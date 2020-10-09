import sys
import wave
import zwsp_steg
import cv2
import numpy as np
from PIL import Image, ImageDraw 
from random import randint
from re import findall


def encode_wav():
    audiofile = input("Please enter the path to wav file: ")
    string = input("Please enter a message to hide: ")
    song = wave.open(audiofile, mode='rb')
    # Read frames and convert to byte array
    frame_bytes = bytearray(list(song.readframes(song.getnframes())))
    # Append data to fill out rest of the bytes. Receiver shall detect and remove these characters.
    string = string + int((len(frame_bytes)-(len(string)*8*8))/8) *'#'
    # Convert text to bit array
    bits = list(map(int, ''.join([bin(ord(i)).lstrip('0b').rjust(8,'0') for i in string])))
    # Replace LSB of each byte of the audio data by one bit from the text bit array
    for i, bit in enumerate(bits):
        frame_bytes[i] = (frame_bytes[i] & 254) | bit
    # Get the modified bytes
    frame_modified = bytes(frame_bytes)
    outputname = audiofile[:-4] + '_encoded.wav'
    # Write bytes to a new wave audio file
    with wave.open(outputname, 'wb') as fd:
        fd.setparams(song.getparams())
        fd.writeframes(frame_modified)
    song.close()

def decode_wav():
    audiofile = input("Please enter the wav file with a supposed hidden message: ")
    song = wave.open(audiofile, mode='rb')
    # Convert audio to byte array
    frame_bytes = bytearray(list(song.readframes(song.getnframes())))

    # Extract the LSB of each byte
    extracted = [frame_bytes[i] & 1 for i in range(len(frame_bytes))]
    # Convert byte array back to string
    string = "".join(chr(int("".join(map(str,extracted[i:i+8])),2)) for i in range(0,len(extracted),8))
    # Cut off at the filler characters
    decoded = string.split("###")[0]

    # Print the extracted text
    print("Sucessfully decoded: "+decoded)
    song.close()

def to_bin(data):
    """Convert `data` to binary format as string"""
    if isinstance(data, str):
        return ''.join([format(ord(i), "08b") for i in data])
    elif isinstance(data, bytes) or isinstance(data, np.ndarray):
        return [format(i, "08b") for i in data]
    elif isinstance(data, int) or isinstance(data, np.uint8):
        return format(data, "08b")
    else:
        raise TypeError("Type not supported.")

def encode():
    image_name = input("Please enter the path of a png image, where you would like to hide a message: ")
    secret_data = input("Please write a message to hide into png file: ")
    # read the image
    image = cv2.imread(image_name)
    # maximum bytes to encode
    n_bytes = image.shape[0] * image.shape[1] * 3 // 8
    print("[*] Maximum bytes to encode:", n_bytes)
    if len(secret_data) > n_bytes:
        raise ValueError("[!] Insufficient bytes, need bigger image or less data.")
    print("[*] Encoding data...")
    # add stopping criteria
    secret_data += "====="
    data_index = 0
    # convert data to binary
    binary_secret_data = to_bin(secret_data)
    # size of data to hide
    data_len = len(binary_secret_data)
    for row in image:
        for pixel in row:
            # convert RGB values to binary format
            r, g, b = to_bin(pixel)
            # modify the least significant bit only if there is still data to store
            if data_index < data_len:
                # least significant red pixel bit
                pixel[0] = int(r[:-1] + binary_secret_data[data_index], 2)
                data_index += 1
            if data_index < data_len:
                # least significant green pixel bit
                pixel[1] = int(g[:-1] + binary_secret_data[data_index], 2)
                data_index += 1
            if data_index < data_len:
                # least significant blue pixel bit
                pixel[2] = int(b[:-1] + binary_secret_data[data_index], 2)
                data_index += 1
            # if data is encoded, just break out of the loop
            if data_index >= data_len:
                break
    cv2.imwrite(image_name[:-4] + '_encoded.png', image)
    print ("image with secret data is saved as '" + image_name[:-4] +"_encoded.png'")

def decode():
    image_name = input("Please enter the path to png file with a supposed hidden message: ")
    print("[+] Decoding...")
    # read the image
    image = cv2.imread(image_name)
    binary_data = ""
    for row in image:
        for pixel in row:
            r, g, b = to_bin(pixel)
            binary_data += r[-1]
            binary_data += g[-1]
            binary_data += b[-1]
    # split by 8-bits
    all_bytes = [ binary_data[i: i+8] for i in range(0, len(binary_data), 8) ]
    # convert from bits to characters
    decoded_data = ""
    for byte in all_bytes:
        decoded_data += chr(int(byte, 2))
        if decoded_data[-5:] == "=====":
            break
    print ('decoded data: ' + decoded_data[:-5])

	


def stega_encrypt():	
	input_image = input("Enter the path to a png file, where you wnat to hide a message: ")
	secret_data = input("Enter a message to hide: ")
	keys = [] 					#keys
	img = Image.open(input_image) 	#image object
	draw = ImageDraw.Draw(img)	   		#draw ogject
	width = img.size[0]  		   		#width
	height = img.size[1]		   		#height	
	pix = img.load()				#pix
	f = open('keys.txt','w')			#text file for keys

	for elem in ([ord(elem) for elem in secret_data]):
		key = (randint(1,width-10),randint(1,height-10))		
		g, b = pix[key][1:3]
		draw.point(key, (elem,g , b))														
		f.write(str(key)+'\n')								
	
	print('keys were written to the keys.txt file')
	img.save(input_image[:-4]+'_encoded.png')
	f.close()

def stega_decrypt():
	output_image = input('Enter the path to a png file with a supposed message: ')
	our_keys = input('Enter the path to a txt file with keys: ')
	a = []						    
	keys = []
	img = Image.open(output_image)				
	pix = img.load()
	f = open(our_keys,'r')
	y = str([line.strip() for line in f])				
															
	for i in range(len(findall(r'\((\d+)\,',y))):
		keys.append((int(findall(r'\((\d+)\,',y)[i]),int(findall(r'\,\s(\d+)\)',y)[i]))) 	
	for key in keys:
		a.append(pix[tuple(key)][0])							
	print (''.join([chr(elem) for elem in a]))

def ZWC():
	text_to_encode = input("Please type the text to encode into zwc: ")
	where_to_hide = input("Please give the path to txt file where you want to hide a message: ")
	text = open(where_to_hide, 'r').read()
	encoded = zwsp_steg.encode(text_to_encode)
	print ("Encoded string:" + encoded)
	text_file = open("Output.txt", "w")
	text_file.write("Encoded string: " + encoded + text)
	text_file.close()
	print ("file saved as output.txt")


def decode_zwc():
	input_file = input("Please give the path to txt file with supposed hidden messages: ")


	try:
		with open(input_file, 'r') as file:
			filedata = file.read()
	except:
		print("Error: Message is not found.")
	decoded = zwsp_steg.decode(filedata)
	print (decoded)
        




	

def menu():
	version = "v1.0.0 release"
	print("    ███████╗████████╗███████╗ ██████╗   ██████╗ ██╗   ██╗")
	print("    ██╔════╝╚══██╔══╝██╔════╝██╔════╝   ██╔══██╗╚██╗ ██╔╝")
	print("    ███████╗   ██║   █████╗  ██║  ███╗  ██████╔╝ ╚████╔╝ ")
	print("    ╚════██║   ██║   ██╔══╝  ██║   ██║  ██╔═══╝   ╚██╔╝  ")
	print("    ███████║   ██║   ███████╗╚██████╔╝  ██║        ██║   ")
	print("    ╚══════╝   ╚═╝   ╚══════╝ ╚═════╝   ╚═╝        ╚═╝   ")
	print("                         github.com/mars1198/StegPy " + version)
	print("1) To hide a message into ZWC print 1")
	print("2) To decode a ZWC message print 2")
	print("3) To hide a message into a png without a key print 3")
	print("4) To decode a message from png without a key print 4")
	print("5) To hide a message into png with a key print 5")
	print("6) To decode a message from png with a key print 6")
	print("7) To hide a message into wav file print 7")
	print("8) To decode a message from a wav file print 8")
	print("9) To exit print x")
	userInput = input("Please Enter an option: ")

	if userInput == "1":
		ZWC()# function to encode text into zwc
	elif userInput == "2":
		decode_zwc() # decode text with zwc
	elif userInput == "3":
		encode() # hide message into png without a key
	elif userInput == "4":
		decode() # decode a message from png file
	elif userInput == "5":
		stega_encrypt() # encode message into png file with a key
	elif userInput == "6":
		stega_decrypt() # decode message from png file with a key
	elif userInput == "7":
		encode_wav()
	elif userInput == "8":
		decode_wav()
	elif userInput == "x":
		print("Goodbye!")
		sys.exit()
	else:
		print("Please enter a valid option: ")
		menu()

menu()
