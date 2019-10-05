import cairo, copy
from Simulation import ECA
from Bitstring import *

eca = ECA(30, 31)
eca.setConf("1", 0)
steps = 32
cellSize = 1
surface = cairo.ImageSurface(cairo.FORMAT_RGB24, (eca.x.length * cellSize), (steps * cellSize))
ctx = cairo.Context(surface)
ctx.set_source_rgb(0, 0, 0)
ctx.rectangle(0, 0, (eca.x.length * cellSize), (steps * cellSize))


xn = copy.deepcopy(eca.x)
y = 0
for i in range(steps):
	print(xn.bits)
	x = 0
	for j in range(xn.length):
		if(xn.bits[j]):
			ctx.set_source_rgb(0, 0, 0)
			ctx.rectangle(x, y, cellSize, cellSize)
			ctx.fill_preserve()
			ctx.set_line_width(0.05)
			ctx.stroke()
		else:
			ctx.set_source_rgb(1, 1, 1)
			ctx.rectangle(x, y, cellSize, cellSize)
			ctx.fill_preserve()
			ctx.set_source_rgb(0, 0, 0)
			ctx.set_line_width(0.05)
			ctx.stroke()
		
		x += cellSize
	
	xn = copy.deepcopy(eca.evolve(xn))

	y += cellSize

surface.write_to_png("test.png")