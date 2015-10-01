# def bits(f):
#     bytes = (ord(b) for b in f.read())
#     for b in bytes:
#         for i in xrange(8):
#             yield (b >> i) & 1

# string = ""
# for b in bits(open('abc.png', 'r')):
#     string += str(b)

# print string


import os 

file_name = os.path.splitext(os.path.basename("test.txt"))


with open('test.txt', 'rb') as f:
	bytes = bytearray(f.read())

for bits in bytes:
	print bits

with open('test1.txt', 'wb') as w:
    w.write(bytes)

# with open("abc.png", "rb") as imageFile:
#   f = imageFile.read()
#   b = bytearray(f)

# for bit in b:
# 	print bit