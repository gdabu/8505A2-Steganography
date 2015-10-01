
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

string = "Hell"
byte_string = ""

for ch in string:
	byte_string += bin(ord(ch))[2:].zfill(8)

print byte_string

cover = Image.open("abc.bmp")


rgba_cover = cover.convert('RGBA')
pixels = rgba_cover.load()
cover_width, cover_height = cover.size

def stego():
	byte_array_index = 0;

	# iterate through each pixel of the cover
	for x in range(cover_width):
		for y in range(cover_height):
			# gather rgba values of the pixel located on x, y.
			r, g, b, a = pixels[x, y]

			# convert the rgba values into binary
			listr = list(bin(r)[2:].zfill(8))
			listg = list(bin(g)[2:].zfill(8))
			listb = list(bin(b)[2:].zfill(8))
			lista = list(bin(a)[2:].zfill(8))
			rgba_array = [listr, listg, listb, lista]
			rgba_decimal_array = []
			# print rgba_array

			# for every rgba value
			for colour_value in rgba_array:

				# use lsb encoding to modify the final bit in the specified rgba value.
				colour_value[7] = byte_string[byte_array_index]
				byte_array_index += 1

				# convert the byte back into decimal
				rgba_decimal_array.append(int(''.join(str(e) for e in colour_value), 2))

				# 
				if byte_array_index >= len(byte_string):
					print rgba_decimal_array
					pixels[x,y] = (rgba_decimal_array[0],rgba_decimal_array[1],rgba_decimal_array[2],rgba_decimal_array[3])
					print rgba_array
					return

			print rgba_decimal_array
			pixels[x,y] = (rgba_decimal_array[0],rgba_decimal_array[1],rgba_decimal_array[2],rgba_decimal_array[3])

			print rgba_array

stego()

rgba_cover.save("cover.bmp")


