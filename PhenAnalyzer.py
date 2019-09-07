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
	strLength=16
	lyapExp=np.zeros(8, dtype=np.float)
	dens=np.zeros(8, dtype=np.uint)
	dmgRad=np.zeros(2, dtype=np.uint)
	strProb=np.zeros((2 ** strLength), dtype=float)
	sim=Simulation()
	damSim=Simulation()

	def __init__(self, dfctPos=0, strLength=16):
		self.dfctPos=dfctPos
		self.strLength=strLength

	def setSimulation(self, sim=Simulation()):
		self.sim=copy.deepcopy(sim)
		self.damSim=copy.deepcopy(sim)
		self.sim.tn=copy.deepcopy(self.sim.eca.initConf)
		self.damSim.tn=copy.deepcopy(self.sim.eca.initConf)
		length=self.sim.eca.initConf.length
		self.lyapExp=np.zeros(length, dtype=np.float)
		self.dens=np.zeros(self.sim.steps, dtype=np.uint)
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
			for x in range(int(self.dmgRad[0]), int(self.dmgRad[1] + 1)):
				self.lyapExp[x] += 1.0

	def getTrinomialRow(self, kn, prev=np.ones(1, dtype=np.uint)):
		if(len(prev) == 1):
			return np.ones(3, dtype=np.uint)
		else:
			current=np.ones((len(prev) + 2), dtype=np.uint)
			currentmid=len(current) // 2
			prevmid=len(prev) // 2
			for i in range(kn):
				pointer1=prevmid - i
				pointer2=prevmid + i
				if(pointer1 == pointer2):
					current[currentmid]=prev[prevmid - 1] + prev[prevmid] + prev[prevmid + 1]
				else:
					if((pointer1 - 1) >= 0):
						current[currentmid - i]=prev[prevmid - i - 1] + prev[prevmid - i] + prev[prevmid - i + 1]
						current[currentmid + i]=current[currentmid - i]
					else:
						current[currentmid - i]=prev[prevmid - i] + prev[prevmid - i + 1]
						current[currentmid + i]=current[currentmid - i]
			return current

	def getLyapunovExp(self, t):
		for i in range(len(self.lyapExp)):
			if(self.lyapExp[i] > 0):
				self.lyapExp[i]=(1 / t) * (math.log(self.lyapExp[i]))

	def getLyapunovExpNorm(self, t, tRow):
		for i in range(self.dmgRad[0], self.dmgRad[1] + 1):
			self.lyapExpNorm[i]=(1 / t) * (math.log(tRow[i]))


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
		ttRow=np.ones(1, dtype=np.uint)
		totalStr=self.sim.tn.length - self.strLength
		entropy=np.zeros(self.sim.steps, dtype=np.float32)
		sScreen=SimScreen(self.damSim.tn.length, self.sim.steps)

		for i in range(self.sim.steps):
			self.strProb=np.zeros((2 ** self.strLength), dtype=float)
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
			#tRow=self.getTrinomialRow((i + 1), tRow)
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