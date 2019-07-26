import gi, cairo, copy, pygame, numpy as np
gi.require_version('Gtk', '3.0')
from gi.repository import Gdk
from Bitstring import Bitstring

class SimSettings():

	cellSize = 1
	state0Color = Gdk.RGBA(1, 1, 1, 1)
	state1Color = Gdk.RGBA(0, 0, 0, 1)
	bckgColor = Gdk.RGBA(0.62, 0.62, 0.62, 1)
	dfctColor = Gdk.RGBA(1, 0, 0, 1)

	def __init__(self, cellSize=1, state0Color=Gdk.RGBA(1, 1, 1, 1), state1Color=Gdk.RGBA(0, 0, 0, 1), bckgColor=Gdk.RGBA(0.62, 0.62, 0.62, 1), dfctColor=Gdk.RGBA(1, 0, 0, 1)):
		self.cellSize = cellSize
		self.state0Color = state0Color
		self.state1Color = state1Color
		self.bckgColor = bckgColor
		self.dfctColor = dfctColor

	def setCellSize(self, cellSize=1):
		self.cellSize = cellSize

	def setState0Color(self, state0Color=Gdk.RGBA(1, 1, 1, 1)):
		self.state0Color = state0Color

	def setState1Color(self, state1Color=Gdk.RGBA(0, 0, 0, 1)):
		self.state1Color = state1Color

	def setBckgColor(self, bckgColor=Gdk.RGBA(0.62, 0.62, 0.62, 1)):
		self.bckgColor = bckgColor

	def setDfctColor(self, dfctColor=Gdk.RGBA(1, 0, 0, 1)):
		self.dfctColor = dfctColor


def createSurface(cells, steps, cellSize):
	width = cells * cellSize
	heigth = steps * cellSize
	surface = cairo.ImageSurface(cairo.FORMAT_RGB24, width, heigth)
	return surface

def drawSimStep(surface, settings=SimSettings(), y=0, xL=None, xR=None, t=None, tp=None):
	context = cairo.Context(surface)
	context.rectangle(0, 0, surface.get_width, surface.get_heigth)
	context.set_source_rgb(settings.bckgColor.red, settings.bckgColor.green, settings.bckgColor.blue)
	context.fill()
	
	if(xL == None and xR == None):
		xL = 0
		xR = t.length

	y *= settings.cellSize
	x = xL * settings.cellSize

	for i in range(xL, xR):
		if(tp == None):
			if(t.bits[i]):
				context.rectangle(x, y, settings.cellSize, settings.cellSize)
				context.set_source_rgb(settings.state1Color.red, settings.state1Color.green, settings.state1Color.blue)
				context.fill()
			else:
				context.rectangle(x, y, settings.cellSize, settings.cellSize)
				context.set_source_rgb(settings.state0Color.red, settings.state0Color.green, settings.state0Color.blue)
				context.fill()
		else:
			if(t.bits[i] ^ tp.bits[i]):
				context.rectangle(x, y, settings.cellSize, settings.cellSize)
				context.set_source_rgb(settings.dfctColor.red, settings.dfctColor.green, settings.dfctColor.blue)
				context.fill()
			else:
				if(tp.bits[i]):
					context.rectangle(x, y, settings.cellSize, settings.cellSize)
					context.set_source_rgb(settings.state1Color.red, settings.state1Color.green, settings.state1Color.blue)
					context.fill()
				else:
					context.rectangle(x, y, settings.cellSize, settings.cellSize)
					context.set_source_rgb(settings.state0Color.red, settings.state0Color.green, settings.state0Color.blue)
					context.fill()
		x += self.cellSize


"""
class Plotter:

	cellSize=1
	cell1=(0, 0, 0)
	cell0=(255, 255, 255)
	bckg=(160, 160, 160)
	dfct=(255, 0, 0)
	screen=pygame.Surface((0, 0))

	def __init__(self, cellSize=1):
		self.cellSize=cellSize

	def createSurface(self, width=0, heigth=0):
		width *= self.cellSize
		heigth *= self.cellSize
		screen = pygame.Surface((width, heigth))
		screen.fill(self.bckg)
		return screen

	def drawStep(self, screen, width=1024, heigth=512, y=0, xL=None, xR=None, config=None, dmgConfig=None):

		Draws the given configuration on the simulation screen.

		Parameters
		----------
			y : int
				Step of the evolution.
			xL : int
				Position from which will began to draw.
			xR : int
				Position until which will ends to draw.
			bitStr : BitString
				Configuration to draw.
			dmgConfig : BitString
				Configuration to compare and draw the defects.

		if(xL == None and xR == None):
			xL = 0
			xR = width // self.cellSize

		y *= self.cellSize
		x = xL * self.cellSize

		for i in range(xL, xR):
			if (dmgConfig == None):
				if config.bits[i]:
					self.screen.fill(self.cell1, (x, y, self.cellSize, self.cellSize))
				else:
					self.screen.fill(self.cell0, (x, y, self.cellSize, self.cellSize))
			else:
				if (config.bits[i] ^ dmgConfig.bits[i]):
					self.screen.fill(self.dfct, (x, y, self.cellSize, self.cellSize))
				else:
					if dmgConfig.bits[i]:
						self.screen.fill(self.cell1, (x, y, self.cellSize, self.cellSize))
					else:
						self.screen.fill(self.cell0, (x, y, self.cellSize, self.cellSize))
			x += self.cellSize

	def saveToPNG(self, screen, filePath):
			Saves the evolution simulation into a .png file.

			Parameters
			----------
				filePath : string
					Path of the file to save the simulation.
		pygame.image.save(screen, filePath)
		print("Simulation saved")
"""