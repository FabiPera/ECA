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
		denPer : int
			Percentage of cells with value 1 in the global configuration.
		rule : BitString
			Base 2 representation of the rule.
		initConf : BitString 
			Initial configuration of the ECA.
	"""
	denPer=0
	rule=BitString()
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
			self.initConf.bits=np.ones(len(self.initConf), dtype=int)

		self.initConf.bsFromString(seed)

	def setRandInitConf(self):
		"""
		Initialize a random configuration.
		"""
		dens=((self.denPer * len(self.initConf)) // 100)
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
		tn=BitString(len(t))
		n=0
		neighb=BitString(3)
		for i in range(len(t)):
			neighb.bits[2]=t.getValue(i - 1)
			neighb.bits[1]=t.getValue(i)
			neighb.bits[0]=t.getValue(i + 1)
			n=neighb.binToInt()
			if (self.rule.bits[n]):
				tn.bits[i]=1
			else:
				tn.bits[i]=0

		return tn