
from PIL import Image, ImageDraw, ImageFont, ImageEnhance
import sys
import array





cover = Image.open("test.bmp")
rgba_cover = cover.convert('RGB')
pixels = rgba_cover.load()
cover_width, cover_height = cover.size
bit_array = ""
secret_message_size = 0

def stego():
	global bit_array
	global secret_message_size
	byte_array_index = 0;
	

	secret_message_size = 40
	secret_message_index = 0

	# iterate through each pixel of the cover
	for x in range(cover_width):
		for y in range(cover_height):

			if secret_message_index < secret_message_size:
				# gather rgba values of the pixel located on x, y.
				r, g, b = pixels[x, y]
				# print pixels[x, y]
				r_str = str(bin(r)[2:].zfill(8))[7]
				g_str = str(bin(g)[2:].zfill(8))[7]
				b_str = str(bin(b)[2:].zfill(8))[7]
				bit_array +=  r_str + g_str + b_str
			
				secret_message_index += 3

			else:
				print bit_array
				return
stego()

secret_message = ""
# bit_counter = 0
# byte = ""

byte_array = []

for i in range(secret_message_size):
	secret_message += bit_array[i]


write_byte_arrray = []

# convert bit string into array of bytes in decimal format. 
for i in range (0, len(secret_message)/8):
	write_byte_arrray.append(int(secret_message[i*8:(i+1) * 8], 2))

bytes_array = array.array('B', write_byte_arrray).tostring()
secrets = bytearray(bytes_array)

w = open('elton.txt', 'w')
w.write(secrets)






