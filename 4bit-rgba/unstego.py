from PIL import Image, ImageDraw, ImageFont, ImageEnhance
import sys



cover = Image.open("cover.bmp")


rgba_cover = cover.convert('RGBA')
pixels = rgba_cover.load()
cover_width, cover_height = cover.size

def stego():
	bit_array_string = ""
	# iterate through each pixel of the cover
	for x in range(1):
		for y in range(10):

			# gather rgba values of the pixel located on x, y.
			r, g, b, a = pixels[x, y]

			print pixels[x,y]

			bit_array_string += list(bin(r)[2:].zfill(8))[7]
			bit_array_string += list(bin(g)[2:].zfill(8))[7]
			bit_array_string += list(bin(b)[2:].zfill(8))[7]
			bit_array_string += list(bin(a)[2:].zfill(8))[7] + " "
	
	# print bit_array_string

stego()



