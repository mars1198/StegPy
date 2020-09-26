import cv2
import numpy as np
import sys
from PIL import Image, ImageDraw 
from random import randint
from re import findall
from colorama import Fore, Style

def to_bin(data):
    """Convert `data` to binary format as string"""
    if isinstance(data, str):
        return ''.join([ format(ord(i), "08b") for i in data ])
    elif isinstance(data, bytes) or isinstance(data, np.ndarray):
        return [ format(i, "08b") for i in data ]
    elif isinstance(data, int) or isinstance(data, np.uint8):
        return format(data, "08b")
    else:
        raise TypeError("Type not supported.")

def encode(image_name, secret_data):
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
    return image

def decode(image_name):
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
    return decoded_data[:-5]

	


def stega_encrypt(input_image, secret_data, output_image):	
	
	keys = [] 					#сюда будут помещены ключи
	img = Image.open(input_image) 	#создаём объект изображения
	draw = ImageDraw.Draw(img)	   		#объект рисования
	width = img.size[0]  		   		#ширина
	height = img.size[1]		   		#высота	
	pix = img.load()				#все пиксели тут
	f = open('keys.txt','w')			#текстовый файл для ключей

	for elem in ([ord(elem) for elem in secret_data]):
		key = (randint(1,width-10),randint(1,height-10))		
		g, b = pix[key][1:3]
		draw.point(key, (elem,g , b))														
		f.write(str(key)+'\n')								
	
	print('keys were written to the keys.txt file')
	img.save(output_image)
	f.close()

def stega_decrypt(output_image, our_keys):
	
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
	return ''.join([chr(elem) for elem in a])

if __name__ == "__main__":
    version = "v0.0.1release"
    print("    ███████╗████████╗███████╗ ██████╗   ██████╗ ██╗   ██╗")
    print("    ██╔════╝╚══██╔══╝██╔════╝██╔════╝   ██╔══██╗╚██╗ ██╔╝")
    print("    ███████╗   ██║   █████╗  ██║  ███╗  ██████╔╝ ╚████╔╝ ")
    print("    ╚════██║   ██║   ██╔══╝  ██║   ██║  ██╔═══╝   ╚██╔╝  ")
    print("    ███████║   ██║   ███████╗╚██████╔╝  ██║        ██║   ")
    print("    ╚══════╝   ╚═╝   ╚══════╝ ╚═════╝   ╚═╝        ╚═╝   ")
    print("                         github.com/mars1198/StegPy " + version)

    try:
        KEYS = sys.argv[1]
        DATA = sys.argv[2]

        if DATA == '-e' and KEYS == '-n':
            input_image = sys.argv[3]
            output_image = sys.argv[4]
            secret_data = sys.argv[5]
            encoded_image = encode(input_image, secret_data)
            cv2.imwrite(output_image, encoded_image)
        elif DATA == '-d' and KEYS =='-n':
            output_image = sys.argv[3]
            decoded_data = decode(output_image)
            print("[+] Decoded data:", decoded_data)
        elif DATA == '-e' and KEYS == '-k':
            input_image = sys.argv[3]
            output_image = sys.argv[4]
            secret_data = sys.argv[5]
            encoded_image = stega_encrypt(input_image, secret_data, output_image)            
        elif DATA == '-d' and KEYS == '-k':
            output_image = sys.argv[3]
            our_keys = sys.argv[4]
            decoded_data = stega_decrypt(output_image, our_keys)
            print("you message: ", decoded_data)
        else:
            print("Input for encoding data without keys: python3 stega.py -n -e [path_to_image] [path_to_save_encoded_image] your_message")
            print("Input for decoding data without keys: python3 stega.py -n -d [path_to_encoded_image]")
            print("Input for encoding data with keys: python3 stega.py -k -e [path_to_image] [path_to_save_encoded_image] your_message")
            print("Input for decoding data with keys: python3 stega.py -k -d [path_to_encoded_image] [path_to_keys]")
    except IndexError:
        print("Input for encoding data without keys: python3 stega.py -n -e [path_to_image] [path_to_save_encoded_image] your_message")
        print("Input for decoding data without keys: python3 stega.py -n -d [path_to_encoded_image]")
        print("Input for encoding data with keys: python3 stega.py -k -e [path_to_image] [path_to_save_encoded_image] your_message")
        print("Input for decoding data with keys: python3 stega.py -k -d [path_to_encoded_image] [path_to_keys]")

