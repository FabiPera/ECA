import numpy as np, copy, math, sys, pygame
from pygame.locals import *
from BitString import BitString

class ECA:

	"""
	ECA object contains the representation of a Elementary Cellular Automata.

	Parameters
	----------
		rule : int
			Value of the rule.
		length : int
			Number of cells in the configuration.

	Attributes
	----------
		rule : BitString
			Base 2 representation of the rule.
		neighb : BitString
			BitString to compute the neighborhood of the current cell.
		initConf : BitString 
			Initial configuration of the ECA.
	"""
	rule=BitString(8)
	neighb=BitString(3)
	initConf=BitString()

	def __init__(self, rule=0, length=8):
		self.rule.bsFromInt(rule)
		self.initConf=BitString(length)

	def setInitConf(self, seed, oz):
		"""
		Initialize the configuration from a string.

		Parameters
		----------
			seed : string
				Seed string to initalize the configuration.
			oz : int
				Value for fill the initial configuration (0 or 1).
		"""
		if (oz):
			self.initConf.bits=np.ones(self.initConf.length, dtype=int)

		self.initConf.bsFromString(seed)

	def setRandInitConf(self, denPer=50):
		"""
		Initialize a random configuration.
		"""
		dens=((denPer * self.initConf.length) // 100)
		self.initConf.bsFromRandomVal(dens)
	
	def evolve(self, t):
		"""
		Evolve a configuration with the ECA rule.
		
		Parameters
		----------
			t : BitString
				Configuration to evolve.

		Returns
		-------
			tn : BitString
				Configuration evolved.
		"""
		tn=BitString(t.length)
		n=0
		for i in range(t.length):
			self.neighb.bits[2]=t.getValue(i - 1)
			self.neighb.bits[1]=t.getValue(i)
			self.neighb.bits[0]=t.getValue(i + 1)
			n=self.neighb.binToInt()
			if (self.rule.bits[n]):
				tn.bits[i]=1
			else:
				tn.bits[i]=0

		return tn