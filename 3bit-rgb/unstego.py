
from PIL import Image, ImageDraw, ImageFont, ImageEnhance
import sys
import array
import binascii






cover = Image.open("germany.bmp")
rgba_cover = cover.convert('RGB')
pixels = rgba_cover.load()
cover_width, cover_height = cover.size
bit_array = ""
secret_message_size = 0

def stego():
	global bit_array
	global secret_message_size
	byte_array_index = 0;
	byte = ""
	bytez = []
	secret_message_size = 208
	secret_message_index = 0
	nullcount = 0
	file_size = ""

	# iterate through each pixel of the cover
	for x in range(cover_width):
		for y in range(cover_height):
			r, g, b = pixels[x, y]
			# ----------------------------------------------------
			r_str = str(bin(r)[2:].zfill(8))[7]
			g_str = str(bin(g)[2:].zfill(8))[7]
			b_str = str(bin(b)[2:].zfill(8))[7]

			rgb_bit_array = [r_str, g_str, b_str]

			for i in range(len(rgb_bit_array)):
				
				
				byte += rgb_bit_array[i]

				if len(byte) == 8:
					bytez.append(byte)
					if byte == "00000000" and nullcount == 0:
						print bytez[0:len(bytez) - 1]
						bytez = []
						nullcount += 1
					elif byte == "00000000" and nullcount == 1:
						print bytez[0:len(bytez) - 1]
						secret_message_size = ''.join(binascii.unhexlify('%x' % int(b,2)) for b in bytez[0:len(bytez) - 1])
						print secret_message_size
						bytez = []
						nullcount += 1
						continue;
					byte = ""

				if nullcount == 2:
					if secret_message_index < int(secret_message_size):
						bit_array += rgb_bit_array[i]
						secret_message_index += 1
					else:
						return

stego()

secret_message = ""

byte_array = []

for i in range(int(secret_message_size)):
	secret_message += bit_array[i]

# print(len(secret_message))
print secret_message
write_byte_arrray = []

# convert bit string into array of bytes in decimal format. 
for i in range (0, len(secret_message)/8):
	write_byte_arrray.append(int(secret_message[i*8:(i+1) * 8], 2))

bytes_array = array.array('B', write_byte_arrray).tostring()
secrets = bytearray(bytes_array)

w = open('secret.txt', 'w')
w.write(secrets)






