import numpy as np, copy, math
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
		self.sim.tn=copy.deepcopy(self.sim.eca.initConf)
		self.damSim.tn=copy.deepcopy(self.sim.eca.initConf)
		length=self.sim.eca.initConf.length
		self.lyapExp=np.zeros(length, dtype=np.float32)
		self.damSim.tn.bits[self.dfctPos]=not(self.damSim.tn.bits[self.dfctPos])

	def getConeRatio(self, y):
		self.dmgRad[0]=self.dfctPos
		self.dmgRad[1]=self.dfctPos
		if(y > 0):
			i=0
			while(i < self.dfctPos):
				if(self.sim.tn.bits[i] ^ self.damSim.tn.bits[i]):
					self.dmgRad[0]=i
					break
				else:
					i += 1
			i=self.sim.tn.length - 1
			while(i > self.dfctPos):
				if (self.sim.tn.bits[i] ^ self.damSim.tn.bits[i]):
					self.dmgRad[1]=i
					break
				else:
					i -= 1
			if ((self.dmgRad[1] - self.dmgRad[0]) > (2 * y)):
				self.dmgRad[0]=self.dfctPos
		
	def countDefects(self):
		if (self.dmgRad[0] == self.dmgRad[1]):
			self.lyapExp[self.dfctPos] += 1.0
		else:
			for x in range(self.dmgRad[0], self.dmgRad[1] + 1):
				self.lyapExp[x] += 1.0

	def getLyapunovExp(self, t):
		for i in range(len(self.lyapExp)):
			if(self.lyapExp[i] > 0):
				self.lyapExp[i]=(1 / t) * (math.log(self.lyapExp[i]))

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
			self.sim.stepForward()
			self.damSim.stepForward()

		sScreen.saveToPNG(sScreen.screen, "DamageSimulation.png")
		sScreen.openImage("DamageSimulation.png")
		
		sScreen=SimScreen(self.damSim.tn.length, self.sim.steps)
		self.sim.tn=copy.deepcopy(self.sim.eca.initConf)
		self.damSim.tn=copy.deepcopy(self.sim.eca.initConf)
		self.damSim.currentStep=0
		self.sim.currentStep=0
		self.damSim.tn.bits[self.dfctPos]=not(self.damSim.tn.bits[self.dfctPos])

		for i in range(self.sim.steps):
			self.getConeRatio(i)
			sScreen.drawConfiguration(y=i, xL=(self.dmgRad[0]), xR=(self.dmgRad[1] + 1), bitStr=self.damSim.tn)
			self.damSim.stepForward()
			self.sim.stepForward()
			self.countDefects()

		print(self.lyapExp)
		self.getLyapunovExp(self.sim.steps)
		print(self.lyapExp)
		sScreen.saveToPNG(sScreen.screen, "DamageCone.png")
		sScreen.openImage("DamageCone.png")