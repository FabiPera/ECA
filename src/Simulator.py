import numpy as np, copy
from Bitstring import Bitstring
from ECA import ECA
from dataclasses import dataclass

@dataclass
class Simulation:
	steps: int = 0

class Simulator:
	
	eca = ECA()

	def __init__(self, eca=ECA()):
		self.eca = copy.deepcopy(eca)

	def setSteps(self, steps=512):
		self.steps = steps

	def setECA(self, eca=ECA()):
		self.eca = copy.deepcopy(eca)
	
	def nextStep(self, x0, x1=None):
		if(x1 == None):
			xn = Bitstring(x0.length)
			xn = copy.deepcopy(self.eca.evolve(x0))
			steps -= 1
		else:
			x0n = Bitstring(x0.length)
			x1n = Bitstring(x1.length)
			x0n = copy.deepcopy(self.eca.evolve(x0))
			x1n = copy.deepcopy(self.eca.evolve(x1))
			steps -= 1	
