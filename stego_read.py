import array
import binascii
import sys
from PIL import Image

# saveSecretFile
#
# @args secretFileName: path of the secret file 
# @args secretFileBitString: string of bits to save
# 
# saves the secretFileBitString with file th name passed in through secretFileName
# 
# @return the new saved cover image.
# 
def saveSecretFile(secretFileName, secretFileBitString):
	secretByteStrings = []

	# convert bit string into array of bytes in decimal format. 
	for i in range (0, len(secretFileBitString)/8):
		secretByteStrings.append(int(secretFileBitString[i*8:(i+1) * 8], 2))

	secretByteString = array.array('B', secretByteStrings).tostring()
	secrets = bytearray(secretByteString)

	secretFile = open("s_" + secretFileName, 'w')
	secretFile.write(secrets)

# stegoRead
#
# @args coverImagePath: path of the cover image
# 
# Reads a cover image and decodes the bits to retrieve the secret file. 
# 
# @return the saved secret image.
# 
def stegoRead(coverImagePath):
	bitBuffer = ""
	byteBuffer = []
	nullCounter = 0

	secretFileBitString = ""
	secretFileName = ""
	secretBitStringLength = 0
	secretBitStringIndex = 0

	cover = Image.open(coverImagePath)
	pixels = cover.load()
	coverWidth, coverHeight = cover.size

	# iterate through each pixel of the cover
	for x in range(coverWidth):
		for y in range(coverHeight):

			# get pixel values
			r, g, b = pixels[x, y]
			rgbSecretBits = [str(bin(r)[2:].zfill(8))[7], str(bin(g)[2:].zfill(8))[7], str(bin(b)[2:].zfill(8))[7]]

			# grab each pixel value
			for i in range(len(rgbSecretBits)):
				
				# get file name and file size
				if nullCounter < 2:

					bitBuffer += rgbSecretBits[i]

					if len(bitBuffer) == 8:
						byteBuffer.append(bitBuffer)

						if bitBuffer == "00000000":
							if nullCounter == 0:
								secretFileName = ''.join(binascii.unhexlify('%x' % int(b,2)) for b in byteBuffer[0:len(byteBuffer) - 1])
								
							elif nullCounter == 1:
								secretBitStringLength = ''.join(binascii.unhexlify('%x' % int(b,2)) for b in byteBuffer[0:len(byteBuffer) - 1])
							nullCounter += 1
							byteBuffer = []

						bitBuffer = ""

				# if file name and size have been parsed, retrieve data.
				else:

					if int(secretBitStringIndex) < int(secretBitStringLength):
						secretFileBitString += rgbSecretBits[i]
						secretBitStringIndex += 1
						continue;
					else:
						return saveSecretFile(secretFileName, secretFileBitString)

	return saveSecretFile(secretFileName, secretFileBitString)

							
			