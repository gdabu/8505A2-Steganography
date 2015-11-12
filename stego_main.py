from stego_read import *
from stego_write import *
import argparse
import sys

if __name__ == '__main__':

	#set command line arguments
	argumentParser = argparse.ArgumentParser(description="8505A2 Stego Write")
	argumentParser.add_argument('-o','--option',dest='option', help='stego option: \'read\' or \'write\'', required=True)
	argumentParser.add_argument('-c','--cover',dest='cover', help='Path of the cover image', required=True)
	argumentParser.add_argument('-s','--secret',dest='secret', help='Path of the secret file')
	command = argumentParser.parse_args();


	if command.option == "read":
		stegoRead(command.cover)

	elif command.option == "write":
	
		if command.secret == None:
			print "No Secret File Selected"
			
		else:
			stegoWrite(command.secret, command.cover)
			
	else:
		print "Illegal Option"
		print "Usage: python steg_main -o <read|write> -c <cover-image-path> -s <secret-image-path>"
	
	sys.exit()