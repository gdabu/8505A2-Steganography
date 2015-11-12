import os
import sys
from PIL import Image

# stringToBinary
# 
# @args string : a string
#
# converts a string into a string of bits
# 
# @return binaryString : string of bits
#
def stringToBinary(string):
	binaryString = ""

	for c in string:
		binaryString += format(ord(c), 'b').zfill(8)

	return binaryString

# fileToBinary
# 
# @args fileName: a string of the file path 
# 
# opens a file and converts it into a string of bits.
# the string of data bits is preceded by file information including the file
#  name and the number of bits in the data. 
# 
# Bit String Structure: 
# 				| file_size | nullchar | file_name | nullchar | file_data
# 
# @return binaryString : string of bits
#
def fileToBinary(fileName):

	header_FileName = ""
	header_FileSize = ""
	payload_FileData = ""

	# 1. Get the file name in binary
	header_FileName = stringToBinary(fileName)

	# 2a. Get the file data in binary
	secretFile = open(fileName, 'rb')
	data_byte_array = bytearray(secretFile.read())

	# 2b. Convert the array of bytes into a bit string
	payload_FileData = ''.join(bin(byte)[2:].zfill(8) for byte in data_byte_array)

	# 3a. Get the number of bits of the file in binary (ASCII) 
	header_FileSizeList = list(str(len(payload_FileData)))
	
	# 3b. Convert the array of decimal numbers into a bit string (ASCII)
	header_FileSize = ''.join(format(ord(i), 'b').zfill(8) for i in header_FileSizeList)


	# Return the Bit String
	# Bit String structure:
	# 			| file_size | file_name | file_data
	return header_FileName + "00000000" + header_FileSize + "00000000" + payload_FileData

# loadNewCoverImage
# 
# @args fileName: a string of the file path 
# 
# Opens a file and initializes it so that the pixels can be manipulated.
# 
# @return new cover image, array of pixels, cover image width, cover image height
#
def loadNewCoverImage(coverImagePath):

	newCover = Image.open(coverImagePath).convert('RGB')
	pixels = newCover.load()
	width, height = newCover.size

	return [newCover, pixels, width, height]

# getDecimalPixelRGB
#
# @args rgb: an array of decimal values, which represent the rgb values of a pixel in binary format
# 
# Converts the binary values for rgb into decimal .
# 
# @return the rgb values of the pixel in decimal
# 
def getDecimalPixelRGB(rgb):
	rgba_decimal_array = []
	
	for colour_value in rgb:
		rgba_decimal_array.append(int(''.join(str(b) for b in colour_value), 2))

	return (rgba_decimal_array[0], rgba_decimal_array[1], rgba_decimal_array[2])

# checkFileSizeLimit
#
# @args coverImageArea: total area of an image, in pixels.
# @args bitString: string of bits
# 
# Checks to see that coverImageArea is large enough to store all the bits in bitString
# 
# @return true if coverImageArea is large enough to store the bitString
# 
def checkFileSizeLimit(coverImageArea, bitString):
	print coverImageArea * 3
	print len(bitString)
	if coverImageArea * 3 <= len(bitString):
		return 0
	else:
		return 1

# stegoWrite
#
# @args secretFilePath: path of the secret file 
# @args coverImagePath: path of the cover image
# 
# Utilizes LSB to encode bits from a secret file into a cover image, and saves the new cover image.
# 
# @return the new saved cover image.
# 
def stegoWrite(secretFilePath, coverImagePath):

	secretFile_BitString = fileToBinary(secretFilePath)
	newCover, pixels, coverWidth, coverHeight = loadNewCoverImage(coverImagePath)

	if checkFileSizeLimit(coverWidth * coverHeight, secretFile_BitString) == 0:
		print "Cover Image Is Too Small."
		return

	secretFile_BitIndex = 0;

	# loop through each pixel
	for x in range(coverWidth):
		for y in range(coverHeight):

			r, g, b = pixels[x, y]
			rgba_array = [list(bin(r)[2:].zfill(8)), list(bin(g)[2:].zfill(8)), list(bin(b)[2:].zfill(8))]
			rgba_decimal_array = []

			for i in range(len(rgba_array)):
				
				# if there are no more bits to be stored 
				if secretFile_BitIndex >= len(secretFile_BitString):
					
					pixels[x, y] = getDecimalPixelRGB(rgba_array)
					return newCover.save("cover.bmp")
				# if there are more bits to be stored.
				else:
					rgba_array[i][7] = secretFile_BitString[secretFile_BitIndex]
					secretFile_BitIndex += 1
			
			pixels[x, y] = getDecimalPixelRGB(rgba_array)

	return newCover.save("cover.bmp")