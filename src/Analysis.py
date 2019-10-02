import numpy as np, matplotlib.pyplot as plt, copy, math
from Bitstring import *
from Simulation import *

class Analysis:

	dfctPos = 0
	strLength = 16
	sim = Simulation()
	dens = np.zeros(8, dtype=np.uint)
	dmgRad = np.zeros(2, dtype=np.uint)
	ttrow = np.zeros(1, dtype=np.double)
	lyapExp = np.zeros(8, dtype=np.ulonglong)
	strProb = np.zeros((2 ** strLength), dtype=np.double)

	def __init__(self, dfctPos=0, strLength=16, sim=Simulation()):
		self.dfctPos = dfctPos
		self.strLength = strLength
		self.dens = np.zeros(self.sim.steps, dtype=np.uint)
		self.lyapExp = np.zeros(self.sim.steps, dtype=np.double)
		self.strProb = np.zeros(int((2 ** self.strLength)), dtype=np.double)
		self.sim = Simulation(sim.eca, sim.steps)
		self.sim.setSettings(sim.cellSize, sim.state0Color, sim.state1Color, sim.bckgColor, sim.dfctColor)

	def getDensity(self, xn):
		for i in range(xn.length):
			if(xn.bits[i]):
				self.dens[i] += 1
	
	def getConeRadius(self, y, t, tp):
		self.dmgRad[0] = self.dfctPos
		self.dmgRad[1] = self.dfctPos
		if(y > 0):
			i = 0
			while(i < self.dfctPos):
				if(t.bits[i] ^ tp.bits[i]):
					self.dmgRad[0] = i
					break
				else:
					i += 1
			i = t.length - 1
			while(i > self.dfctPos):
				if(t.bits[i] ^ tp.bits[i]):
					self.dmgRad[1] = i
					break
				else:
					i -= 1
			if((self.dmgRad[1] - self.dmgRad[0]) > (2 * y)):
				self.dmgRad[0] = self.dfctPos

	def countDefects(self, t, tp):
		if (self.dmgRad[0] == self.dmgRad[1]):
			self.lyapExp[self.dfctPos] += 1.0
		else:
			for x in range(self.dmgRad[0], int(self.dmgRad[1] + 1)):
				if(t.bits[x] ^ tp.bits[x]):
					self.lyapExp[x] += 1.0

	def getTrinomialRow(self, kn, prev=np.ones(1, dtype=np.ulonglong)):
		if(len(prev) == 1):
			return np.ones(3, dtype=np.ulonglong)
		else:
			current = np.ones((len(prev) + 2), dtype=np.ulonglong)
			currentmid = len(current) // 2
			prevmid=len(prev) // 2
			for i in range(kn):
				pointer1 = prevmid - i
				pointer2 = prevmid + i
				if(pointer1 == pointer2):
					current[currentmid] = prev[prevmid - 1] + prev[prevmid] + prev[prevmid + 1]
				else:
					if((pointer1 - 1) >= 0):
						current[currentmid - i] = prev[prevmid - i - 1] + prev[prevmid - i] + prev[prevmid - i + 1]
						current[currentmid + i] = current[currentmid - i]
					else:
						current[currentmid - i] = prev[prevmid - i] + prev[prevmid - i + 1]
						current[currentmid + i] = current[currentmid - i]
			return current

	def getTrinomialRow(self,)

	def getLyapunovExp(self, t):
		for i in range(len(self.lyapExp)):
			if(self.lyapExp[i] > 0):
				self.lyapExp[i] = (1 / t) * (math.log(self.lyapExp[i]))

	def getLyapunovExpTT(self, t):
		for i in range(int(self.dmgRad[0]), int(self.dmgRad[1] + 1)):
			if(self.ttrow[i] > 0):
				self.ttrow[i] = (1 / t) * (math.log(self.ttrow[i]))

	def getEntropy(self, totalStr):
		string = Bitstring(self.strLength)
		theta = 0.0
		entropy = 0.0
		for i in range(totalStr):
			k = i
			for j in range(self.strLength):
				string.bits[j] = self.sim.xn.bits[k]
				k += 1
			n = string.binToInt()
			self.strProb[n] += 1.0
		
		for i in range(len(self.strProb)):
			if(self.strProb[i]):
				theta += 1.0
			
		if(theta):
			entropy = ((1.0 / self.strLength) * math.log(theta, 2))
		return entropy

	def simAnalysis(self):
		asim = Simulation(self.sim.eca, self.sim.steps)
		asim.setSettings(self.sim.cellSize, self.sim.state0Color, self.sim.state1Color, self.sim.bckgColor, self.sim.dfctColor)
		asim.xn.bits[self.dfctPos] = not(asim.xn.bits[self.dfctPos])
		totalStr = self.sim.xn.length - self.strLength
		entropy = np.zeros(self.sim.steps, dtype=np.double)

		for i in range(self.sim.steps):
			self.strProb = np.zeros(int((2 ** self.strLength)), dtype=np.double)
			self.getDensity(self.sim.xn)
			self.getConeRadius(i, asim.xn, self.sim.xn)
			self.countDefects(asim.xn, self.sim.xn)
			self.ttrow = copy.deepcopy(self.getTrinomialRow((i + 1), self.ttrow))
			asim.stepForward(i, self.sim.xn)
			self.sim.stepForward(i)
			entropy[i] = self.getEntropy(totalStr)
		
		self.getLyapunovExp(self.sim.steps)
		for h in range(int(len(self.ttrow) // 2)):
			print(self.ttrow[h])
		#self.getLyapunovExpTT(self.sim.steps)
		plt.figure("Density")
		plt.plot(self.dens, "m,-")
		plt.savefig("../img/Density.png")
		plt.clf()
		plt.figure("Lyapunov exponents")
		plt.plot(self.lyapExp, "m,-")
		plt.savefig("../img/LyapunovExp.png")
		plt.clf()
		#plt.figure("Lyapunov exponents TT")
		#plt.plot(self.ttrow, "m,-")
		#plt.savefig("../img/LyapunovExpTT.png")
		#plt.clf()
		plt.figure("Entropy")
		plt.plot(entropy, "m,-")
		plt.savefig("../img/Entropy.png")
		plt.clf()
		asim.saveToPNG(fileName="dsimulation.png")
		self.sim.saveToPNG()

	def ruleAnalysis(self):
		pass