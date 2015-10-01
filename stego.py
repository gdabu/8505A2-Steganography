
from PIL import Image, ImageDraw, ImageFont, ImageEnhance
import sys
import os 


# prepare the secret file

# get the file name
file_name = os.path.splitext(os.path.basename("test.txt"))

# open the file and store bytes into data_byte_array
with open(file_name[0] + file_name[1], 'rb') as f:
	data_byte_array = bytearray(f.read())

# store the each bit in data_byte_array into byte_string
byte_string = ""
for byte in data_byte_array:
	byte_string += bin(byte)[2:].zfill(8)

print byte_string


# prepare the cover image

# load the cover image
cover = Image.open("tux.bmp")
# 
rgba_cover = cover.convert('RGBA')
# load pixels of rgba_cover
pixels = rgba_cover.load()
cover_width, cover_height = cover.size


def stego():
	byte_array_index = 0;

	# iterate through each pixel of the cover
	for x in range(cover_width):
		for y in range(cover_height):

			# gather rgba values of the pixel located on x, y.
			# pixels[x, y] will return the decimal values for the pixels rgba values.
			r, g, b, a = pixels[x, y]

			# convert the rgba values into binary and store them into rgba_binary_array
			rgba_binary_array = [list(bin(r)[2:].zfill(8)), list(bin(g)[2:].zfill(8)), list(bin(b)[2:].zfill(8)), list(bin(a)[2:].zfill(8))]
			rgba_decimal_array = [] # will hold the new decimal values for rgba
			# print rgba_binary_array

			# loop through the rgba values in rgba_binary_array
			for colour_value in rgba_binary_array:

				# use lsb encoding to modify the final bit in the specified rgba value.
				colour_value[7] = byte_string[byte_array_index]
				byte_array_index += 1

				# convert the byte back into decimal
				rgba_decimal_array.append(int(''.join(str(e) for e in colour_value), 2))

				# return once there are no more bytes to encode
				if byte_array_index >= len(byte_string):
					# set the pixel with the new rgba values
					pixels[x,y] = (rgba_decimal_array[0],rgba_decimal_array[1],rgba_decimal_array[2],rgba_decimal_array[3])
					# print rgba_binary_array
					# print pixels[x, y]
					return

			# set the pixel with the new rgba values
			pixels[x,y] = (rgba_decimal_array[0],rgba_decimal_array[1],rgba_decimal_array[2],rgba_decimal_array[3])
			print pixels[x, y]
			# print rgba_binary_array

stego()

rgba_cover.save("cover.bmp")


