import numpy as np, copy
from pygame.locals import *
from BitString import BitString
from ECA import ECA
from SimScreen import SimScreen

class Simulation:

	"""
	Simulation object contains the representation of a ECA evolution simulation.

	Parameters
	----------
		steps : int
			Value of steps in the evolution.
		eca : ECA
			ECA used in the evolution simulation.

	Attributes
	----------
		steps : int
			Value of steps in the evolution.
		currentStep : int
			Value of the current step (step by step evolution).
		eca : ECA
			ECA used in the evolution simulation.
		tn : BitString
			Current configuration in the evolution.
	"""
	steps=0
	currentStep=0
	eca=ECA()
	tn=BitString()
	
	def __init__(self, steps=0, eca=ECA()):
		self.steps=steps
		self.eca=copy.deepcopy(eca)
		self.tn=copy.deepcopy(self.eca.initConf)
	
	def run(self, fileName="Simulation.png"):
		"""
		Runs the evolution simulation.

		Parameters
		----------
		filename : string
			Name of the file to save the simulation.
		"""
		self.tn=copy.deepcopy(self.eca.initConf)
		sScreen=SimScreen(self.tn.length, self.steps)

		for i in range(self.steps):
			sScreen.drawConfiguration(y=i, bitStr=self.tn)
			self.tn=copy.deepcopy(self.eca.evolve(self.tn))
		
		sScreen.saveToPNG(sScreen.screen, fileName)
		#sScreen.openImage(fileName)

	def stepForward(self):
		"""
		Advances one step in the evolution simulation.
		"""
		if(self.currentStep < self.steps):
			self.tn=copy.deepcopy(self.eca.evolve(self.tn))
			self.currentStep += 1