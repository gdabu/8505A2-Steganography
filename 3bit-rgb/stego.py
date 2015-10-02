
from PIL import Image, ImageDraw, ImageFont, ImageEnhance
import sys
import os 

byte_string = ""
NULL = "00000000"

# prepare the secret file

# get the file name
file_name = os.path.splitext(os.path.basename("hide.txt"))

# open the file and store bytes into data_byte_array
with open(file_name[0] + file_name[1], 'rb') as f:
	data_byte_array = bytearray(f.read())

# store the each bit in data_byte_array into byte_string

for byte in data_byte_array:
	byte_string += bin(byte)[2:].zfill(8)

print byte_string
print len(byte_string)


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
						# byte_array_index += 1
					print pixels[x, y]
					pixels[x,y] = (rgba_decimal_array[0],rgba_decimal_array[1],rgba_decimal_array[2])
					# print pixels[x, y]
					# print "byte_array_index: " + `byte_array_index`
					# print "total bits: " + str(len(byte_string))
					return;

stego()

rgba_cover.save("germany.bmp")


