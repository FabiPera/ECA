import numpy as np, copy, sys, pygame, subprocess, os
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

	def drawConfiguration(self, y, xL=None, xR=None, bitStr=None, dmgBitstr=None):
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
		if(xL == None and xR == None):
			xL=0
			xR=self.width // 2

		y *= 2
		x=xL * 2

		for i in range(xL, xR):
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