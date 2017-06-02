from PIL import Image
import sys

def encode(filename, text):
	print text
	count1 = 15
	count2 = 7
	count3 = 0
	text_length = len(text)
	print text_length
	text = list(text)
	for i in range(0, text_length):
		text[i] = ord(text[i])
	im = Image.open(filename)
	width = im.size[0]
	height = im.size[1]
	print "/* width:%d */"%(width)
	print "/* height:%d */"%(height)
	for h in range(0, height):
		if count3 >= text_length:
			break
		for w in range(0, width):
			if count3 >= text_length:
				break
			pixel = im.getpixel((w, h))
			pixel = list(pixel)
			if count1 >= 0:
				digit = (text_length >> count1) & 1
				pixel[2] = (pixel[2] >> 1 << 1) | digit
				count1 -= 1
			else:
				digit = (text[count3] >> count2) & 1
				pixel[2] = (pixel[2] >> 1 << 1) | digit
				count2 -= 1
				if count2 < 0:
					count2 = 7
					count3 += 1
			pixel = tuple(pixel)
			im.putpixel((w, h), pixel)
	im.save(filename, "png")

def decode(filename):
	count1 = 15
	count2 = 0
	text_length = 0
	im = Image.open(filename)
	width = im.size[0]
	height = im.size[1]
	print "/* width:%d */"%(width)
	print "/* height:%d */"%(height)
	count = 0
	result = 0
	result_string = []
	for h in range(0, height):
		if count1 < 0 and count2 >= text_length:
			break
		for w in range(0, width):
			if count1 < 0 and count2 >= text_length:
				break
			pixel = im.getpixel((w, h))
			result_bit = pixel[2] & 1
			if count1 >= 0:
				text_length = (text_length << 1) | result_bit
				count1 -= 1
			else:
				result = (result << 1) | result_bit
				count += 1
				if count >= 8:
					result_string.append(chr(result))
					count = 0
					result = 0
					count2 += 1
	print ''.join(result_string)

encode(sys.argv[1], sys.argv[2])
decode(sys.argv[1])