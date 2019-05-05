import numpy as np, copy, math, matplotlib.pyplot as plt
from pygame.locals import *
from BitString import BitString
from ECA import ECA
from Simulation import Simulation
from SimScreen import SimScreen

class PhenAnalyzer:

	"""
	PhenAnalyzer object contains the representation of a phenotipic analyzer.

	Parameters
	----------
		dfctPos : int
			Position in which a defect was introduce.
		strLength : int
			Lenght of the strings to analyze.
	Attributes
	----------
		dfctPos : int
			Position in which a defect was introduce.
		strLength : int
			Lenght of the strings to analyze.
		lyapExp : float32 array
			Lyapunov exponent of every cell in the configuration.
		dmgRad : unsigned int32 array
			Radius of the damage cone.
		sim : Simulation
			Original evolution simulation.
		damSim : Simulation
			Evolution simulation with a defect introduced.
	"""
	dfctPos=0
	strLength=10
	lyapExp=np.zeros(8, dtype=np.float32)
	dens=np.zeros(8, dtype=np.uint32)
	dmgRad=np.zeros(2, dtype=np.uint32)
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
		self.dens=np.zeros(self.sim.steps, dtype=np.uint32)
		self.damSim.tn.bits[self.dfctPos]=not(self.damSim.tn.bits[self.dfctPos])

	def getConeRadius(self, y):
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

	def getStrProb(self, strl):
		numOfStr=2 ** strl
		self.strProb=np.zeros(numOfStr, dtype=float)
		bs=BitString(strl)
		for i in range(numOfStr):
			bs.bsFromInt(i)
			bs=self.sim.eca.evolve(bs)
			nextState=bs.binToInt()
			self.strProb[nextState] += 1.0

		print(self.strProb)

	def getEntropy(self, totalStr):
		string=BitString(self.strLength)
		theta=0.0
		entropy=0.0
		for i in range(totalStr):
			k=i
			for j in range(self.strLength):
				string.bits[j]=self.sim.tn.bits[k]
				k += 1
			n=string.binToInt()
			self.strProb[n] += 1.0
		
		for i in range(len(self.strProb)):
			if(self.strProb[i]):
				theta += 1.0
			
		if(theta):
			entropy=((1.0 / self.strLength) * math.log(theta, 2))
		return entropy

	def runAnalysis(self):
		totalStr=self.sim.tn.length - self.strLength
		entropy=np.zeros(self.sim.steps, dtype=np.float32)
		sScreen=SimScreen(self.damSim.tn.length, self.sim.steps)

		for i in range(self.sim.steps):
			self.strProb=np.zeros(2 ** self.strLength, dtype=float)
			sScreen.drawConfiguration(y=i, bitStr=self.sim.tn, dmgBitstr=self.damSim.tn)
			entropy[i]=self.getEntropy(totalStr)
			for j in range(self.sim.tn.length):
				if(self.sim.tn.bits[j]):
					self.dens[i] += 1
			self.sim.stepForward()
			self.damSim.stepForward()

		sScreen.saveToPNG(sScreen.screen, "DamageSimulation.png")
		
		sScreen=SimScreen(self.damSim.tn.length, self.sim.steps)
		self.sim.tn=copy.deepcopy(self.sim.eca.initConf)
		self.damSim.tn=copy.deepcopy(self.sim.eca.initConf)
		self.damSim.currentStep=0
		self.sim.currentStep=0
		self.damSim.tn.bits[self.dfctPos]=not(self.damSim.tn.bits[self.dfctPos])

		for i in range(self.sim.steps):
			self.getConeRadius(i)
			sScreen.drawConfiguration(y=i, xL=(self.dmgRad[0]), xR=(self.dmgRad[1] + 1), bitStr=self.damSim.tn)
			self.damSim.stepForward()
			self.sim.stepForward()
			self.countDefects()

		self.getLyapunovExp(self.sim.steps)
		sScreen.saveToPNG(sScreen.screen, "DamageCone.png")
		plt.figure("Density")
		plt.plot(self.dens, "m,-")
		plt.savefig("Density.png")
		plt.clf()
		plt.figure("Lyapunov exponents")
		plt.plot(self.lyapExp, "m,-")
		plt.savefig("LyapunovExp.png")
		plt.clf()
		plt.figure("Entropy")
		plt.plot(entropy, "m,-")
		plt.savefig("Entropy.png")
		plt.clf()
		#plt.show()