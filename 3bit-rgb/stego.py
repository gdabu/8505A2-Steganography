
from PIL import Image, ImageDraw, ImageFont, ImageEnhance
import sys
import os 
import argparse



NULL = "00000000"

# gets the file name, file size, and file data of a file and converts them into bits.
def setupSecretDataBits(file_name):

	file_name_binary = ""
	file_data_binary = ""

	# the bits that are stored into the pixels of the cover. 
	# will include the file name, file size, and file data. 
	secret_binary_string = "" 

	# 1. Convert the file name into bits and add it to secret_binary_string

	for c in file_name:
		file_name_binary += format(ord(c), 'b').zfill(8)

	secret_binary_string += file_name_binary + NULL

	# 2. Read the secret file and convert it to bytes.
	
	with open(file_name, 'rb') as f:
		data_byte_array = bytearray(f.read())

	# 3. Convert the bytes into bits and store the bits into file_data_binary

	for byte in data_byte_array:
		file_data_binary += bin(byte)[2:].zfill(8)

	# 4. Determine the size of file_data_binary and convert the length into bits. Store bits into file_size_binary

	file_size = list(str(len(file_data_binary)))
	file_size_binary = ''.join(format(ord(x), 'b').zfill(8) for x in file_size)
	file_size_binary += NULL

	# 5. Add file_size_binary and file_data_binary into the secret_binary_string

	secret_binary_string += file_size_binary + file_data_binary

	return secret_binary_string

# stores the bits of a file into the pixels of a cover image
def stego(secret_binary_string, cover_name):

	cover = Image.open(cover_name)

	newCover = cover.convert('RGB')
	pixels = newCover.load()
	cover_width, cover_height = cover.size

	byte_array_index = 0;
	final_pixel_flag = 0;

	# iterate through each pixel of the cover
	for x in range(cover_width):
		for y in range(cover_height):

			# 1. gather rgba values of the pixel located on x, y.
			r, g, b = pixels[x, y]

			# 2. convert the rgba values into binary
			listr = list(bin(r)[2:].zfill(8))
			listg = list(bin(g)[2:].zfill(8))
			listb = list(bin(b)[2:].zfill(8))
			
			rgba_array = [listr, listg, listb]
			rgba_decimal_array = []

			# 3. check to see if this is the final pixel to be stored. If not (or final_pixel_flag == 0)
			#  then write the bits to all three rgb values.
			if final_pixel_flag == 0:

				# for every rgba value
				for colour_value in rgba_array:

					# use lsb encoding to modify the final bit in the specified rgba value.
					colour_value[7] = secret_binary_string[byte_array_index]
					byte_array_index += 1

					# convert the byte back into decimal
					rgba_decimal_array.append(int(''.join(str(e) for e in colour_value), 2))
					# # print pixels[x, y]

				pixels[x,y] = (rgba_decimal_array[0],rgba_decimal_array[1],rgba_decimal_array[2])
				

			# 4a. If there are less than 3 bits to store into a pixel
			if len(secret_binary_string) - byte_array_index < 3:
				

				if final_pixel_flag == 0:
					# 4b. set final_pixel_flag to 1 which mean we will be manipulating the last pixel.	
					final_pixel_flag = 1
					# 4c. continue to the next iteration of the loop. This will give us the last pixel to manipulate.
					continue;
				
				# 5a. This condition will be met after the second iteration of there being less than 3 bits to store.
				# when this is true we are now manipulating the last pixel.
				else:

					# 5b. grab the rgb values of the last pixel
					rgba_decimal_array = [r,g,b]

					# 5c. store the remaining bits into the final pixel.
					for i in range(len(secret_binary_string) - byte_array_index):
						rgba_array[i][7] = secret_binary_string[byte_array_index]
						rgba_decimal_array[i] = (int(''.join(str(e) for e in rgba_array[i]), 2))
						byte_array_index += 1
					
					pixels[x,y] = (rgba_decimal_array[0],rgba_decimal_array[1],rgba_decimal_array[2])
					return newCover;

if __name__ == '__main__':

	#set command line arguments
	cmdParser = argparse.ArgumentParser(description="8505A2 Stego Write")
	cmdParser.add_argument('-c','--cover',dest='cover', help='Path of the cover image', required=True)
	cmdParser.add_argument('-s','--secret',dest='secret', help='Path of the secret file', required=True)
	args = cmdParser.parse_args();

	secret_binary_string = ""

	# 1. get file name
	file_name = os.path.basename(args.secret)
	
	# 2. get bits to be stored in cover image
	secret_binary_string = setupSecretDataBits(file_name)

	# 3. store bits into cover image
	newCoverImage = stego(secret_binary_string, args.cover)
	
	# 4. save cover image
	newCoverImage.save("cover.bmp")
