# StegPy.py

Python terminal tool for steganography. Works propperly only with png files. Works in two modes: without a key and with a key. A key is an .txt that will be saved in scripts folder after encoding.




# How to use
-n -e - to encode without a key
-n -d - to decode without a key
-k -e - to encode with a key
-k -d - to decode with a key

Example of commands

Encoding without a key -  python3 stega.py -n -e [path_to_image] [path_to_save_encoded_image] your_message
Decoding without a key -  python3 stega.py -n -d [path_to_encoded_image]
Encoding with a key - python3 stega.py -k -e [path_to_image] [path_to_save_encoded_image] your_message
Decoding with a key - python3 stega.py -k -d [path_to_encoded_image] [path_to_keys]
