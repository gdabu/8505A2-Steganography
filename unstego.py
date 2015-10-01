
from PIL import Image, ImageDraw, ImageFont, ImageEnhance
import sys



cover = Image.open("abc.png")


rgba_cover = cover.convert('RGBA')
pixels = rgba_cover.load()
cover_width, cover_height = cover.size

def stego():
	byte_array_index = 0;
	bit_array = ""
	# iterate through each pixel of the cover
	for x in range(1):
		for y in range(1):

			# gather rgba values of the pixel located on x, y.
			r, g, b, a = pixels[x, y]
			r_str = str(bin(r)[2:].zfill(8)) 
			g_str = str(bin(g)[2:].zfill(8)) 
			b_str = str(bin(b)[2:].zfill(8)) 
			a_str = str(bin(a)[2:].zfill(8)) 
			print r_str + g_str + b_str + a_str

stego()

rgba_cover.save("cover.png")


