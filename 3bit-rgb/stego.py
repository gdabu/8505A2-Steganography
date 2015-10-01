
from PIL import Image, ImageDraw, ImageFont, ImageEnhance
import sys
# def bits(f):
#     bytes = (ord(b) for b in f.read())
#     for b in bytes:
#         for i in xrange(8):
#             yield (b >> i) & 1

# string = ""
# for b in bits(open('test.txt', 'r')):
#     string += str(b)

# string = string[::-1]

string = "helo"
byte_string = ""

for ch in string:
	byte_string += bin(ord(ch))[2:].zfill(8)

print byte_string

cover = Image.open("original.png")
rgba_cover = cover.convert('RGB')
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
			# lista = list(bin(a)[2:].zfill(8))
			
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
				print pixels[x, y]



			if len(byte_string) - byte_array_index < 3:
				if final_pixel_flag == 0:
					final_pixel_flag = 1
					continue;
				else:
					rgba_decimal_array = [r,g,b]
					for i in range(len(byte_string) - byte_array_index):
						rgba_array[i][7] = byte_string[byte_array_index]
						rgba_decimal_array[i] = (int(''.join(str(e) for e in rgba_array[i]), 2))

					pixels[x,y] = (rgba_decimal_array[0],rgba_decimal_array[1],rgba_decimal_array[2])
					print pixels[x, y]
					# print "byte_array_index: " + `byte_array_index`
					# print "total bits: " + str(len(byte_string))
					return;

stego()

rgba_cover.save("cover.png")


