import numpy as np, copy, sys, pygame, subprocess, os
from pygame.locals import *
from Bitstring import Bitstring

class SimScreen:

	"""
	SimScreen object contains the representation of a screen where the simulations are drawn.
	
	Parameters
	----------
		width : int
			Width value for the simulation screen.
		height : int
			Height value for the simultion screen.
	Attributes
	----------
		width : int
			Width value for the simulation screen.
		height : int
			Height value for the simultion screen.
		cell1Clr : tuple
			RGB value of the cells with value 1.
		cell0Clr : tuple
			RGB value of the cells with value 0.
		bckgClr : tuple
			RGB value of the background.
		dfctClr : tuple
			RGB value of the cells with defect.
		screen : Surface
			Surface object to draw the simulations.
	"""
	width=0
	height=0
	cell1Clr=(0, 0, 0)
	cell0Clr=(255, 255, 255)
	bckgClr=(160, 160, 160)
	dfctClr=(255, 0, 0)
	screen=pygame.Surface((0, 0))

	def __init__(self, width=0, height=0):
		self.width=width * 2
		self.height=height * 2
		self.screen=pygame.Surface((self.width, self.height))
		self.screen.fill(self.bckgClr)

	def drawConfiguration(self, y, xL=None, xR=None, bitStr=None, dmgBitstr=None):
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
			bitStr : Bitstring
				Configuration to draw.
			dmgBitstr : Bitstring
				Configuration to compare and draw the defects.
		"""
		if(xL == None and xR == None):
			xL=0
			xR=self.width // 2

		y *= 2
		x=xL * 2

		for i in range(int(xL), int(xR)):
			if (dmgBitstr == None):
				if bitStr.bits[i]:
					self.screen.fill(self.cell1Clr, (x, y, 2, 2))
				else:
					self.screen.fill(self.cell0Clr, (x, y, 2, 2))
			else:
				if (bitStr.bits[i] ^ dmgBitstr.bits[i]):
					self.screen.fill(self.dfctClr, (x, y, 2, 2))
				else:
					if dmgBitstr.bits[i]:
						self.screen.fill(self.cell1Clr, (x, y, 2, 2))
					else:
						self.screen.fill(self.cell0Clr, (x, y, 2, 2))
			x += 2

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