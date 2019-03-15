import numpy as np, copy, math, sys, pygame, subprocess, os
from pygame.locals import *
from BitString import BitString
from ECA import ECA
from Simulation import Simulation

class phenAnalyzer:

	dfctPos=0
	strLength=3
	tn=BitString()
	dmgFreq=np.zeros(8, dtype=np.uint8)
	lyapExp=np.zeros(8, dtype=float)
	dmgRad=np.zeros(2, dtype=np.uint8)
	strProb=np.zeros(2 ** strLength, dtype=float)
	sim=Simulation()

	def __init__(self, dfctPos=0, strLength=3, sim=Simulation()):
		self.dfctPos=dfctPos
		self.strLength=strLength
		self.sim=sim
		length=sim.eca.initConf.length
		self.tn=BitString(length)
		self.dmgFreq=np.zeros(length, dtype=np.uint8)
		self.lyapExp=np.zeros(length, dtype=float)
		self.sim.eca.currentConf=copy.deepcopy(self.sim.eca.initConf)
		self.tn=copy.deepcopy(self.sim.eca.initConf)
		self.tn.bits[self.dfctPos]=not(self.tn.bits[self.dfctPos])

	def getConeRatio(self, t, y):
		self.dmgRad[0]=self.dmgPos
		self.dmgRad[1]=self.dmgPos
		if(y > 0):
			i=0
			while(i < self.dmgPos):
				if (self.currentConf.bits[i] ^ t.bits[i]):
					self.dmgRad[0]=i
					break
				else:
					i += 1
			i=self.currentConf.length - 1
			while(i > self.dmgPos):
				if (self.currentConf.bits[i] ^ t.bits[i]):
					self.dmgRad[1]=i
					break
				else:
					i -= 1
			if ((self.dmgRad[1] - self.dmgRad[0]) > (2 * y)):
				self.dmgRad[0]=self.dmgPos
		
	def countDefects(self):
		if (self.dmgRad[0] == self.dmgRad[1]):
			self.damageFreq[self.dmgPos] += 1
		else:
			for x in range(self.dmgRad[0], self.dmgRad[1] + 1):
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
		for i in range(self.currentConf.length - entStringLen):
			k=i
			for j in range(self.entStringLen):
				str.bits[j]=self.currentConf.bits[k]
				k += 1
			n=str.binToInt()
			strProb[n] += 1.0
		
		for i in range(2 ** entStringLen):
			if (strProb[i]):
				strProb[i]=strProb[i] / (2 ** entStringLen)
				theta += 1
			
		self.hX=((1.0 / self.entStringLen) * math.log(theta, 2))

	def run(self):
		self.sim.createSimScreen()

		for i in range(self.sim.steps):
			self.sim.drawConfiguration(y=i, bitStr=self.sim.eca.currentConf, dmgBitstr=self.tn)
			self.sim.eca.currentConf=copy.deepcopy(self.sim.eca.evolve(self.sim.eca.currentConf))
			self.tn=copy.deepcopy(self.sim.eca.evolve(self.tn))

		self.sim.saveToPNG(self.sim.screen, "DamageSimulation.png")
		self.sim.openImage("DamageSimulation.png")
	