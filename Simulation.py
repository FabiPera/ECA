import numpy as np, copy, math, sys, pygame, subprocess, os
from pygame.locals import *
from BitString import BitString
from ECA import ECA
from SimScreen import SimScreen

class Simulation:

	steps=0
	eca=ECA()
	tn=BitString()
	
	def __init__(self, steps=0, eca=ECA()):
		self.steps=steps
		self.eca=eca
		self.tn=BitString(self.eca.initConf.length)
		self.tn=copy.copy(self.eca.initConf)
	
	def run(self, fileName="Simulation.png"):
		sScreen=SimScreen(self.tn.length, self.steps)

		for i in range(self.steps):
			sScreen.drawConfiguration(y=i, bitStr=self.tn, dmgBitstr=None)
			self.tn=copy.deepcopy(self.eca.evolve(self.tn))
		
		sScreen.saveToPNG(sScreen.screen, fileName)
		sScreen.openImage(fileName)