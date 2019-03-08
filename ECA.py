import numpy as np, copy, math, sys, pygame
from numba import jit, int32
from pygame.locals import *
from BitString import BitString

class ECA:

	"""
	ECA object contains the representation of a Elementary Cellular Automata.

	Parameters
	----------
		r : int
			Value of the rule.
		s : int
			Number of steps for the evolution.
		l : int
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
		seedConfig : BitString 
			Global configuration of the ECA.
		t0 : BitString
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
	steps=0
	denPer=0
	dmgPos=0
	hX=0.0
	entStringLen=3
	rule=BitString(8)
	seedConfig=BitString(21)
	t0=BitString(21)
	tDam=BitString(21)
	damageFreq=np.zeros(21, dtype=int)
	strProb=np.zeros(2 ** entStringLen, dtype=float)
	dmgR=np.zeros(2, dtype=int)
	lyapExp=np.zeros(21, dtype=float)

	def __init__(self, r=94, s=512, l=1024):
		self.rule.bsFromInt(r)
		self.steps=s
		self.seedConfig=BitString(l)
		self.t0=BitString(l)
		self.tDam=BitString(l)
		self.damageFreq=np.zeros(l)

	def setT0(self, str0, oz):
		"""
		Initialize the seed configuration from a string.

		Parameters
		----------
			str0 : string
				Seed string to initalize the configuration.
			oz : int
				Value for fill the seed configuration (0 or 1).
		"""
		if (oz):
			self.seedConfig.bits=np.ones(self.seedConfig.length, dtype=int)

		self.seedConfig.bsFromString(str0)
		self.t0=copy.deepcopy(self.seedConfig)

	def setRandomT0(self):
		"""
		Initialize a random seed configuration.
		"""
		dens=((self.denPer * self.t0.length) // 100)
		self.seedConfig.bsFromRandomVal(dens)
		self.t0=copy.deepcopy(self.seedConfig)

	
	def evolve(self, t0):
		"""
		Evolve a configuration with the ECA rule.
		
		Parameters
		----------
			t0 : BitString
				Configuration to evolve.

		Returns
		-------
			t1 : BitString
				Configuration evolved.
		"""
		t1=BitString(t0.length)
		n=0
		neighb=BitString(3)
		for i in range(t0.length):
			neighb.bits[2]=t0.getValue(i - 1)
			neighb.bits[1]=t0.getValue(i)
			neighb.bits[0]=t0.getValue(i + 1)
			n=neighb.binToInt()
			if (self.rule.bits[n]):
				t1.bits[i]=1
			else:
				t1.bits[i]=0

		return t1
	
	def setDamage(self):
		self.lyapExp=np.zeros(self.t0.length, dtype=float)
		self.t0=copy.deepcopy(self.seedConfig)
		self.tDam=copy.deepcopy(self.seedConfig)
		self.tDam.bits[self.dmgPos]=not(self.tDam.bits[self.dmgPos])

	def getConeRatio(self, t, y):
		self.dmgR[0]=self.dmgPos
		self.dmgR[1]=self.dmgPos
		if(y > 0):
			i=0
			while(i < self.dmgPos):
				if (self.t0.bits[i] ^ t.bits[i]):
					self.dmgR[0]=i
					break
				else:
					i += 1
			i=self.t0.length - 1
			while(i > self.dmgPos):
				if (self.t0.bits[i] ^ t.bits[i]):
					self.dmgR[1]=i
					break
				else:
					i -= 1
			if ((self.dmgR[1] - self.dmgR[0]) > (2 * y)):
				self.dmgR[0]=self.dmgPos
		
	def countDefects(self):
		if (self.dmgR[0] == self.dmgR[1]):
			self.damageFreq[self.dmgPos] += 1
		else:
			for x in range(self.dmgR[0], self.dmgR[1] + 1):
				self.damageFreq[x] += 1

	def getLyapunovExp(self, t):
		for i in range(len(self.lyapExp)):
			if(self.damageFreq[i] > 0):
				self.lyapExp[i]=(1 / t) * (math.log(self.damageFreq[i]))

	def getTopEntropy(self):
		str=BitString(self.entStringLen)
		entStringLen=self.entStringLen
		strProb=np.zeros(2 ** entStringLen, dtype=float)
		theta=0.0
		for i in range(self.t0.length - entStringLen):
			k=i
			for j in range(self.entStringLen):
				str.bits[j]=self.t0.bits[k]
				k += 1
			n=str.binToInt()
			strProb[n] += 1.0
		
		for i in range(2 ** entStringLen):
			if (strProb[i]):
				strProb[i]=strProb[i] / (2 ** entStringLen)
				theta += 1
			
		self.hX=((1.0 / self.entStringLen) * math.log(theta, 2))
