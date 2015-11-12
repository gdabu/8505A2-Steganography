Readme

There are three file included in this submission:

	stego_main.py - is the main file to be executed. Parses command line arguments, and runs either stego_read or stego_write
	stego_read.py - contains the library functions that are used to decode a cover image.
	stego_write.py - contains the libary functions that are used to encode secret files into cover images.


Setup: 

	1. install python
	2. install the pillow library
		run the command: pip install pillow

Usage: 

	python steg_main -o <read|write> -c <cover-image-path> -s <secret-image-path>

	-o : you may only set this argument to read or write [REQUIRED]
	-c : set it to the path of your cover image [REQUIRED]
	-s : set it to the path of your secret image [not REQUIRED if option is set to read]

	example:

		python steg_main -o read -c cover.bmp

		python steg_main -o write -c cover.bmp -s secret.txt
