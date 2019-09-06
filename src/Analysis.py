import numpy as np, matplotlib.pyplot as plt, copy, math
from Bitstring import *
from Simulation import *

class Analysis:

	eca = ECA()
	dfctPos = 0
	strLength = 16
	dens = np.zeros(8, dtype=np.uint)
	dmgRad = np.zeros(2, dtype=np.uint)
	ttrow = np.zeros(1, dtype=np.double)
	lyapExp = np.zeros(8, dtype=np.double)
	strProb = np.zeros((2 ** strLength), dtype=float)

	def __init__(self, dfctPos=0, strLength=16, eca=ECA()):
		self.dfctPos = dfctPos
		self.strLength = strLength
		self.eca = copy.deepcopy(eca)

	def simAnalysis(self, sim1=Simulation(), sim2=Simulation()):
		print("Simulation analysis starting...")

	def ruleAnalysis(self):
		pass

	def setDefect(self):
		x = copy.deepcopy(self.eca.x)
		x.bits[self.dfctPos] = not(self.eca.x.bits[self.dfctPos])
		
		return x

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

	def getTrinomialRow(self, kn, prev=np.ones(1, dtype=np.uint)):
		if(len(prev) == 1):
			return np.ones(3, dtype=np.uint)
		else:
			current = np.ones((len(prev) + 2), dtype=np.uint)
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

	def getLyapunovExp(self, t):
		for i in range(len(self.lyapExp)):
			if(self.lyapExp[i] > 0):
				self.lyapExp[i] = (1 / t) * (math.log(self.lyapExp[i]))

	