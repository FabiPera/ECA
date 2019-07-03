import numpy as np, copy, sys, pygame, subprocess, os
from pygame.locals import *
from BitString import BitString

class Plotter:

	cellSize=1
	cell1=(0, 0, 0)
	cell0=(255, 255, 255)
	bckg=(160, 160, 160)
	dfct=(255, 0, 0)
	screen=pygame.Surface((0, 0))

	def __init__(self, cellSize=1):
		self.cellSize=cellSize

	def createSurface(self, width=0, height=0):
		width *= self.cellSize
		height *= self.cellSize
		screen = pygame.Surface((width, height))
		screen.fill(self.bckg)
		return screen

	def drawStep(self, screen, width=1024, height=512, y=0, xL=None, xR=None, config=None, dmgConfig=None):
		"""
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
		"""
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
		"""
			Saves the evolution simulation into a .png file.

			Parameters
			----------
				filePath : string
					Path of the file to save the simulation.
		"""
		pygame.image.save(screen, filePath)
		print("Simulation saved")