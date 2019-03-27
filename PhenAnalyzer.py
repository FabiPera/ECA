import numpy as np, copy
from pygame.locals import *
from BitString import BitString
from ECA import ECA
from Simulation import Simulation
from SimScreen import SimScreen

class PhenAnalyzer:

	dfctPos=0
	strLength=3
	lyapExp=np.zeros(8, dtype=np.float32)
	dmgRad=np.zeros(2, dtype=np.uint8)
	strProb=np.zeros(2 ** strLength, dtype=float)
	sim=Simulation()
	damSim=Simulation()

	def __init__(self, dfctPos=0, strLength=3):
		self.dfctPos=dfctPos
		self.strLength=strLength

	def setSimulation(self, sim=Simulation()):
		self.sim=copy.deepcopy(sim)
		self.damSim=copy.deepcopy(sim)
		length=self.sim.eca.initConf.length
		self.lyapExp=np.zeros(length, dtype=np.float32)
		self.damSim.tn.bits[self.dfctPos]=not(self.damSim.tn.bits[self.dfctPos])

	def getConeRatio(self, t, y):
		self.dmgRad[0]=self.dfctPos
		self.dmgRad[1]=self.dfctPos
		if(y > 0):
			i=0
			while(i < self.dfctPos):
				if(self.sim.eca.currentConf.bits[i] ^ t.bits[i]):
					self.dmgRad[0]=i
					break
				else:
					i += 1
			i=self.sim.eca.currentConf.length - 1
			while(i > self.dfctPos):
				if (self.sim.eca.currentConf.bits[i] ^ t.bits[i]):
					self.dmgRad[1]=i
					break
				else:
					i -= 1
			if ((self.dmgRad[1] - self.dmgRad[0]) > (2 * y)):
				self.dmgRad[0]=self.dfctPos
    else:
      
		
	def countDefects(self):
		if (self.dmgRad[0] == self.dmgRad[1]):
			self.damageFreq[self.dfctPos] += 1
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

	def runAnalysis(self):
		sScreen=SimScreen(self.damSim.tn.length, self.sim.steps)

		for i in range(self.sim.steps):
			sScreen.drawConfiguration(y=i, bitStr=self.sim.tn, dmgBitstr=self.damSim.tn)
			self.sim.eca.currentConf=copy.deepcopy(self.sim.eca.evolve(self.sim.eca.currentConf))
			self.tn=copy.deepcopy(self.sim.eca.evolve(self.tn))

		sScreen.saveToPNG(sScreen.screen, "DamageSimulation.png")
		sScreen.openImage("DamageSimulation.png")

		sScreen=SimScreen(self.tn.length, self.sim.steps)
		self.sim.eca.currentConf=copy.deepcopy(self.sim.eca.initConf)
		self.tn=copy.deepcopy(self.sim.eca.initConf)
		self.tn.bits[self.dfctPos]=not(self.tn.bits[self.dfctPos])

		for i in range(self.eca.steps):
			self.getConeRatio(self.tn, i)
			self.drawCone(self.eca.tDam, i)
			self.eca.countDefects()
			self.eca.t0=copy.deepcopy(self.eca.evolve(self.eca.t0))
			self.eca.tDam=copy.deepcopy(self.eca.evolve(self.eca.tDam))

		print(self.eca.damageFreq)
		self.eca.getLyapunovExp(self.eca.steps)
		print(self.eca.lyapExp)
		self.saveToPNG(self.screen, "DamageCone.png")
		self.openImage("DamageCone.png")

	