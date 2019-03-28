import numpy as np, copy
from pygame.locals import *
from BitString import BitString
from ECA import ECA
from SimScreen import SimScreen

class Simulation:

	steps=0
	currentStep=0
	eca=ECA()
	tn=BitString()
	
	def __init__(self, steps=0, eca=ECA()):
		self.steps=steps
		self.eca=copy.deepcopy(eca)
		self.tn=copy.deepcopy(self.eca.initConf)
	
	def run(self, fileName="Simulation.png"):
		self.tn=copy.deepcopy(self.eca.initConf)
		sScreen=SimScreen(self.tn.length, self.steps)

		for i in range(self.steps):
			sScreen.drawConfiguration(y=i, bitStr=self.tn)
			self.tn=copy.deepcopy(self.eca.evolve(self.tn))
		
		sScreen.saveToPNG(sScreen.screen, fileName)
		sScreen.openImage(fileName)

	def stepForward(self):
		if(self.currentStep < self.steps):
			self.tn=copy.deepcopy(self.eca.evolve(self.tn))
			self.currentStep += 1