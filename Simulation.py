import numpy as np, copy, math, sys, pygame, subprocess, os
from pygame.locals import *
from BitString import BitString
from ECA import ECA
from SimScreen import SimScreen

class Simulation:

	steps=0
	eca=ECA()
	
	def __init__(self, eca=ECA(), steps=0):
		self.steps=steps
		self.eca=eca
	
	def run(self):
		sScreen=SimScreen(self.eca.currentConf.length, self.steps)

		for i in range(self.steps):
			sScreen.drawConfiguration(y=i, bitStr=self.eca.currentConf, dmgBitstr=None)
			self.eca.currentConf=copy.deepcopy(self.eca.evolve(self.eca.currentConf))
		
		sScreen.saveToPNG(sScreen.screen, "Simulation.png")
		sScreen.openImage("Simulation.png")