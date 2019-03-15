import numpy as np, copy, math, sys, pygame, subprocess, os
from pygame.locals import *
from BitString import BitString

class SimScreen:
	
	width=0
	height=0
	cellColor=(0, 0, 0)
	bckgColor=(255, 255, 255)
	bckgGColor=(160, 160, 160)
	defectColor=(255, 0, 0)
	screen=pygame.Surface((0, 0))

	def __init__(self, width=0, height=0):
		self.width=width * 2
		self.height=height * 2
		self.screen=pygame.Surface((self.width, self.height))
		self.screen.fill(self.bckgGColor)

	def drawConfiguration(self, y, bitStr=None, dmgBitstr=None):
		"""
		Draw the next step of the evolution in the simulation screen.

		Parameters
		----------
			y : int
				Step of the evolution.
			bitStr : BitString
				Configuration to draw.
			dmgBitstr : BitString
		"""
		y *= 2
		x=0
		for i in range(bitStr.length):
			if (dmgBitstr == None):
				if bitStr.bits[i]:
					self.screen.fill(self.cellColor, (x, y, 2, 2))
				else:
					self.screen.fill(self.bckgColor, (x, y, 2, 2))
			else:
				if (bitStr.bits[i] ^ dmgBitstr.bits[i]):
					self.screen.fill(self.defectColor, (x, y, 2, 2))
				else:
					if dmgBitstr.bits[i]:
						self.screen.fill(self.cellColor, (x, y, 2, 2))
					else:
						self.screen.fill(self.bckgColor, (x, y, 2, 2))
			x += 2

	def drawCone(self, dmgBitstr, y):
		if (y == 0):
			if dmgBitstr.bits[self.eca.dmgPos]:
				self.screen.fill(self.cellColor, (self.eca.dmgPos * 2, 0, 2, 2))
			else:
				self.screen.fill(self.bckgColor, (self.eca.dmgPos * 2, 0, 2, 2))
		else:
			y *= 2
			x=self.eca.dmgR[0]
			for i in range(self.eca.dmgR[0], self.eca.dmgR[1] + 1):
				if dmgBitstr.bits[i]:
					self.screen.fill(self.cellColor, (x * 2, y, 2, 2))
				else:
					self.screen.fill(self.bckgColor, (x * 2, y, 2, 2))
				x += 1

	def saveToPNG(self, screen, path):
		pygame.image.save(screen, path)
		print("Simulation saved")

	def openImage(self, filePath):
		if sys.platform.startswith("darwin"):
			subprocess.call(("open", filePath))
		elif os.name == "nt":
			os.startfile(filePath)
		elif os.name == "posix":
			subprocess.call(("xdg-open", filePath))