import numpy as np, matplotlib.pyplot as plt, copy, math, threading
from Bitstring import *
from Simulation import *
from Plotter import *

class Analysis:

	eca = ECA()
	ttrow = [1]
	dfctPos = 0
	strLength = 16
	analysisOp = [1, 0, 0]
	dens = np.zeros(8, dtype=np.uint)
	dmgRad = np.zeros(2, dtype=np.uint)
	defects = np.zeros(8, dtype=np.uint)
	entropy = np.zeros(8, dtype=np.double)
	lyapExp = np.zeros(8, dtype=np.double)
	lyapExpNorm = np.zeros(8, dtype=np.double)


	def __init__(self, dfctPos=0, strLength=16, eca=ECA(), analysisOp=[1, 0, 0]):
		self.dfctPos = dfctPos
		self.strLength = strLength
		self.eca = copy.deepcopy(eca)
		self.analysisOp = copy.deepcopy(analysisOp)
		self.defects = np.zeros(eca.x.length, dtype=np.uint)
		self.lyapExp = np.zeros(eca.x.length, dtype=np.double)
		self.lyapExpNorm = np.zeros(eca.x.length, dtype=np.double)

	def simAnalysis(self, sim1=Simulation(), sim2=Simulation()):
		threads = []
		totalStr = sim1.xn.length - self.strLength
		self.dens = np.zeros(sim1.steps, dtype=np.uint)
		self.entropy = np.zeros(sim1.steps, dtype=np.double)

		for i in range(sim1.steps):
			if(self.analysisOp[0]):
				x = threading.Thread(target=self.getDensity, args=(i, sim1.xn))
				threads.append(x)
				x.start()
			if(self.analysisOp[1]):
				x = threading.Thread(target=self.getEntropy, args=(i, totalStr, sim1.xn))
				threads.append(x)
				x.start()
			if(self.analysisOp[2]):
				x = threading.Thread(target=self.getTrinomialRow, args=(self.ttrow, ))
				threads.append(x)
				x.start()
				x = threading.Thread(target=self.getConeRadius, args=(i, sim1.xn, sim2.xn))
				threads.append(x)
				x.start()

			for x in threads:
				x.join()
			
			self.countDefects(sim1.xn, sim2.xn)
			sim2.stepForward(i, sim1.xn)
			sim1.stepForward(i)
		
		sim1.saveToPNG(fileName="SimAnalysis.png")
		sim2.saveToPNG(fileName="SimDefects.png")
		threads = []
		if(self.analysisOp[2]):
			x = threading.Thread(target=self.getLyapExp, args=(self.ttrow, len(self.defects), sim1.steps))
			threads.append(x)
			x.start()
			x = threading.Thread(target=self.getLyapExp, args=(self.defects, len(self.defects), sim1.steps))
			threads.append(x)
			x.start()

		for x in threads:
			x.join()

		if(self.analysisOp[0]):
			plotDensity(self.dens, sim1.xn.length)
		if(self.analysisOp[1]):
			plotEntropy(self.entropy)
		if(self.analysisOp[2]):
			plt.figure("Lyapunov exponents")
			plt.plot(self.lyapExp, "m,-")
			plt.savefig("../sim/LyapunovExp.png")
			plt.clf()
			plt.figure("Lyapunov exponents Norm")
			plt.plot(self.lyapExpNorm, "m,-")
			plt.savefig("../sim/LyapunovExpNorm.png")
			plt.clf()

	def ruleAnalysis(self):
		print("Rule analysis")

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

	def getDensity(self, step, xn):
		n = 0
		for i in range(xn.length):
			if(xn.bits[i]):
				n += 1
		
		n *= 100
		n = int(n // xn.length)

		#return n
		self.dens[step] = n

	def countDefects(self, t, tp):
		if(self.dmgRad[0] == self.dmgRad[1]):
			self.defects[self.dfctPos] += 1.0
		else:
			for x in range(self.dmgRad[0], int(self.dmgRad[1] + 1)):
				if(t.bits[x] ^ tp.bits[x]):
					self.defects[x] += 1.0

	def getEntropy(self, step, totalStr, xn):
		strProb = np.zeros((2 ** self.strLength), dtype=np.double)
		string = Bitstring(self.strLength)
		theta = 0.0
		entropy = 0.0
		for i in range(totalStr):
			k = i
			for j in range(self.strLength):
				string.bits[j] = xn.bits[k]
				k += 1
			n = string.binToInt()
			strProb[n] += 1.0
		
		for i in range(len(strProb)):
			if(strProb[i]):
				theta += 1.0
			
		if(theta):
			entropy=((1.0 / self.strLength) * math.log(theta, 2))
		
		#return entropy
		self.entropy[step] = entropy

	def getTrinomialRow(self, n):
		if(len(n) == 1):
			n.append(1)
			
			return n
		else:
			nt = []
			nt.append((n[0] +  (n[1] * 2)))
			for i in range(1, (len(n))):
				if(i != (len(n) - 1)):
					k = n[i - 1] + n[i] + n[i + 1]
				else:
					k = n[i - 1] + n[i]	
				nt.append(k)
			nt.append(1)

			#return nt
			self.ttrow = copy.deepcopy(nt)

	def getLyapExp(self, epsilon, n, t):
		if(len(epsilon) < n):
			i = len(epsilon) - 1
			j = 0
			while(i):
				print("j=" + str(j) + "i=" + str(i))
				self.lyapExpNorm[j] = (1 / t) * (math.log(epsilon[i]))
				j += 1
				i -= 1
			print("------------")
			while(i < len(epsilon) - 1):
				print("j=" + str(j) + "i=" + str(i))
				self.lyapExpNorm[j] = (1 / t) * (math.log(epsilon[i]))
				j += 1
				i += 1
		else:
			for i in range(n):
				if(epsilon[i] > 0):
					self.lyapExp[i] = (1 / t) * (math.log(epsilon[i]))