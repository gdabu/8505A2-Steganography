
from PIL import Image, ImageDraw, ImageFont, ImageEnhance
import sys
import os 
import binascii

byte_string = ""
NULL = "00000000"

# prepare the secret file

# get the file name
file_name = os.path.basename("text.txt")

file_name_binary = ""

# ------------------------------------------------------

for c in file_name:
	file_name_binary += format(ord(c), 'b').zfill(8)

print file_name_binary
print len(file_name_binary)

byte_string += file_name_binary + NULL

# ------------------------------------------------------

# open the file and store bytes into data_byte_array
with open(file_name, 'rb') as f:
	data_byte_array = bytearray(f.read())

file_data_binary = ""

# store the each bit in data_byte_array into byte_string
for byte in data_byte_array:
	file_data_binary += bin(byte)[2:].zfill(8)

print file_data_binary

file_size = list(str(len(file_data_binary)))
file_size_binary = ''.join(format(ord(x), 'b').zfill(8) for x in file_size)
file_size_binary += NULL

# print "file_size: " + `len(file_data_binary)`
# print "file_size_binary: " + file_size_binary

byte_string += file_size_binary + file_data_binary
# print byte_string
# print len(byte_string)

# ------------------------------------------------------

# prepare the cover image

# load the cover image
cover = Image.open("tux.bmp")
# 
rgba_cover = cover.convert('RGB')
# load pixels of rgba_cover
pixels = rgba_cover.load()
cover_width, cover_height = cover.size

def stego():
	byte_array_index = 0;
	final_pixel_flag = 0;

	# iterate through each pixel of the cover
	for x in range(cover_width):
		for y in range(cover_height):

			# gather rgba values of the pixel located on x, y.
			r, g, b = pixels[x, y]

			# convert the rgba values into binary
			listr = list(bin(r)[2:].zfill(8))
			listg = list(bin(g)[2:].zfill(8))
			listb = list(bin(b)[2:].zfill(8))
			
			rgba_array = [listr, listg, listb]
			rgba_decimal_array = []
			# print rgba_array

			if final_pixel_flag == 0:
				# for every rgba value
				for colour_value in rgba_array:

					# use lsb encoding to modify the final bit in the specified rgba value.
					colour_value[7] = byte_string[byte_array_index]
					byte_array_index += 1

					# convert the byte back into decimal
					rgba_decimal_array.append(int(''.join(str(e) for e in colour_value), 2))
					# print pixels[x, y]
					

				pixels[x,y] = (rgba_decimal_array[0],rgba_decimal_array[1],rgba_decimal_array[2])
				# print pixels[x, y]


			# if there are less than 3 bits left to store, take the next pixel and store the bits into it. 
			if len(byte_string) - byte_array_index < 3:
				if final_pixel_flag == 0:
					final_pixel_flag = 1
					continue;
				else:
					rgba_decimal_array = [r,g,b]
					for i in range(len(byte_string) - byte_array_index):
						rgba_array[i][7] = byte_string[byte_array_index]
						rgba_decimal_array[i] = (int(''.join(str(e) for e in rgba_array[i]), 2))
						byte_array_index += 1
					print pixels[x, y]
					pixels[x,y] = (rgba_decimal_array[0],rgba_decimal_array[1],rgba_decimal_array[2])
					# print pixels[x, y]
					# print "byte_array_index: " + `byte_array_index`
					# print "total bits: " + str(len(byte_string))
					return;

stego()

rgba_cover.save("germany.bmp")


