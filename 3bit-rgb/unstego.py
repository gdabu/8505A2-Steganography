
from PIL import Image, ImageDraw, ImageFont, ImageEnhance
import sys



cover = Image.open("cover.png")
rgba_cover = cover.convert('RGB')
pixels = rgba_cover.load()
cover_width, cover_height = cover.size

def stego():
	byte_array_index = 0;
	bit_array = ""
	# iterate through each pixel of the cover
	for x in range(1):
		for y in range(11):
			# gather rgba values of the pixel located on x, y.
			r, g, b = pixels[x, y]
			print pixels[x, y]
			r_str = str(bin(r)[2:].zfill(8))[7]
			g_str = str(bin(g)[2:].zfill(8))[7]
			b_str = str(bin(b)[2:].zfill(8))[7]
			bit_array +=  r_str + g_str + b_str
	print bit_array
stego()



