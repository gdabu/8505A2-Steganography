from PIL import Image, ImageDraw, ImageFont, ImageEnhance
import sys
import array
import binascii
import argparse

#set command line arguments
cmdParser = argparse.ArgumentParser(description="8505A2 Stego Read")
cmdParser.add_argument('-c','--cover',dest='cover', help='Path of the cover image', required=True)
args = cmdParser.parse_args();


# save the bits of the secret file.
def saveSecretDataFile(file_name, secret_message):
	write_byte_arrray = []

	# convert bit string into array of bytes in decimal format. 
	for i in range (0, len(secret_message)/8):
		write_byte_arrray.append(int(secret_message[i*8:(i+1) * 8], 2))

	bytes_array = array.array('B', write_byte_arrray).tostring()
	secrets = bytearray(bytes_array)
	w = open("secret-" + file_name, 'w')
	w.write(secrets)

# gets the secret bits of a file from a cover image.
def unstego(cover_name):
	secret_message = ""
	file_name = ""

	byte_array_index = 0;
	byte = ""
	bytez = []
	secret_message_size = 0
	secret_message_index = 0
	nullcount = 0

	cover = Image.open(cover_name)
	rgba_cover = cover.convert('RGB')
	pixels = cover.load()
	coverWidth, coverHeight = cover.size

	# iterate through each pixel of the cover
	for x in range(coverWidth):
		for y in range(coverHeight):

			# 1. gather rgba values of the pixel located on x, y.
			r, g, b = pixels[x, y]

			# 2. convert the rgba values into binary

			rgbSecretBits = [str(bin(r)[2:].zfill(8))[7], str(bin(g)[2:].zfill(8))[7], str(bin(b)[2:].zfill(8))[7]]

			for i in range(len(rgbSecretBits)):
				
				# 3. nullcount will equal 2 when we are done reading the header, 
				#  and are ready to reading the secret data.
				if nullcount == 2:
					# if there are more bits from the secret to read
					# makes sure you only read the bits you need and not all the bits 
					#  of the cover image.
					if int(secret_message_index) < int(secret_message_size):
						secret_message += rgbSecretBits[i]
						secret_message_index += 1
						continue;
					else:
						return saveSecretDataFile(file_name, secret_message)
				
				# 4. if we are not reading the secret data, then parse for the header data.
				else:
					byte += rgbSecretBits[i]

					# 5a. If we have read 8 bytes
					if len(byte) == 8:
						bytez.append(byte)
						# 5b. check to see if its a null char. The first null terminates the file bytes. The second terminates the file size.
						if byte == "00000000" and nullcount == 0:
							file_name = ''.join(binascii.unhexlify('%x' % int(b,2)) for b in bytez[0:len(bytez) - 1])
							bytez = []
							nullcount += 1
						elif byte == "00000000" and nullcount == 1:
							secret_message_size = ''.join(binascii.unhexlify('%x' % int(b,2)) for b in bytez[0:len(bytez) - 1])
							bytez = []
							nullcount += 1
						byte = ""





if __name__ == '__main__':
	# get file name and data
	unstego("cover.bmp")
	