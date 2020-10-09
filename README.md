# StegPy.py

Python3 terminal tool for steganography. Works propperly only with png files, txt-files and wav files. Nothing really original, just compilation of tools.
With PNG files it works in two modes: without a key and with a key. A key is an .txt file that will be saved in folder after encoding.

Types of used steganography: ZWC for text (https://en.wikipedia.org/wiki/Zero-width_space), LSB for evrything else (https://www.computerhope.com/jargon/l/leastsb.htm)

# Install

git clone https://github.com/mars1198/StegPy.git

cd StegPy

pip3 install -r requirements.txt

Ok, ready to use



# How to use

Just follow the menu of a script

1) To hide a message into ZWC print 1"
2) To decode a ZWC in message print 2"
3) To hide a message into a png without a key print 3"
4) To decode a message from png without a key print 4"
5) To hide a message into png with a key print 5"
6) To decode a message from png with a key print 6"
7) To hide a message into wav file print 7"
8) To decode a message from a wav file print 8"
9) To exit print x"
