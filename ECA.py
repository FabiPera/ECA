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
		steps : int
			Number of steps for the evolution of the ECA.
		denPer : int
			Percentage of cells with value 1 in the global configuration.
		dmgPos : int
			Position of the introduced defect.
		hx : float
			Entropy value.
		entStringLen: int
			Length of the strings for entropy calculation.
		rule : BitString
			Base 2 representation of the rule.
		initConf : BitString 
			Global configuration of the ECA.
		currentConf : BitString
			Configuration to evolve.
		tDam : BitString
			Configuration to evolve with one defect introduced.
		damageFreq : numpy array
			Array to track the damage spreading along the time.
		strProb : numpy array
			Array to count the probability of strings.
		dmgR : numpy array
			Ratio of the damage cone in the current configuration.
		lyapExp : numpy array
			Values of the Lyapunov exponents of each cell.
	"""
	denPer=0
	dmgPos=0
	hX=0.0
	entStringLen=3
	rule=BitString()
	initConf=BitString()
	currentConf=BitString()

	def __init__(self, rule=0, length=8):
		self.rule.bsFromInt(rule)
		self.initConf=BitString(length)
		self.currentConf=BitString(length)
		self.tDam=BitString(length)
		self.damageFreq=np.zeros(length)

	def setInitConf(self, seed, oz):
		"""
		Initialize the seed configuration from a string.

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
		self.currentConf=copy.deepcopy(self.initConf)

	def setRandInitConf(self):
		"""
		Initialize a random seed configuration.
		"""
		dens=((self.denPer * self.currentConf.length) // 100)
		self.initConf.bsFromRandomVal(dens)
		self.currentConf=copy.deepcopy(self.initConf)

	
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
		neighb=BitString(3)
		for i in range(t.length):
			neighb.bits[2]=t.getValue(i - 1)
			neighb.bits[1]=t.getValue(i)
			neighb.bits[0]=t.getValue(i + 1)
			n=neighb.binToInt()
			if (self.rule.bits[n]):
				tn.bits[i]=1
			else:
				tn.bits[i]=0

		return tn

