import numpy as np
import Image
import sys

name = sys.argv[1]
out = sys.argv[2]

im = Image.open(name)

width, height = im.size

t = im.load()

for i in range(width):
	im.putpixel((0, i), (255, 255, 255, 255))

for i in range(height):
	im.putpixel((i, 0), (255, 255, 255, 255))

color1 = t[0, 0]
color2 = (255, 50, 50, 255)

for i in range(width):
	for j in range(height):
		if t[i, j][0] == color1[0] or t[i, j][1] == color1[1] and t[i, j][2] == color1[2]:
			print("bla")
			im.putpixel((i, j), color2)
		else:
			im.putpixel((i, j), (0, 0, 0, 255))

im.save(out)
