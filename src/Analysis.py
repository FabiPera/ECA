import numpy as np, matplotlib.pyplot as plt, copy, math, threading
from Bitstring import Bitstring
from Simulation import ECA, Simulation
from Plotter import *

class Analysis:

	eca = ECA()
	#ttrow = [1]
	dfctPos = 0
	strLength = 16
	analysisOp = [1, 0, 0]
	dens = np.zeros(8, dtype=np.uint)
	dmgRad = np.zeros(2, dtype=np.uint)
	defects = np.zeros(8, dtype=np.double)
	defectsn = np.zeros(8, dtype=np.double)
	entropy = np.zeros(8, dtype=np.double)

	def __init__(self, dfctPos=0, strLength=16, eca=ECA(), analysisOp=[1, 0, 0]):
		self.dfctPos = dfctPos
		self.dmgRad[0] = dfctPos
		self.dmgRad[1] = dfctPos
		self.strLength = strLength
		self.eca = copy.deepcopy(eca)
		self.analysisOp = copy.deepcopy(analysisOp)
		self.defects = np.zeros(eca.x.length, dtype=np.double)
		self.defectsn = np.zeros(eca.x.length, dtype=np.double)

	def simAnalysis(self, sim1, sim2, path):
		threads = []
		simComparison1 = Simulation(sim1.steps, sim1.cellSize, sim1.s0Color, sim1.s1Color, sim1.bColor, sim1.dColor, sim1.eca)
		simComparison2 = Simulation(sim2.steps, sim2.cellSize, sim2.s0Color, sim2.s1Color, sim2.bColor, sim2.dColor, sim2.eca)
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

			# if(self.analysisOp[2]):
				# x = threading.Thread(target=self.getTrinomialRow, args=(self.ttrow, ))
				# threads.append(x)
				# x.start()
				# x = threading.Thread(target=self.getDefectSpreading, args=(i, sim1.xn, sim2.xn))
				# threads.append(x)
				# x.start()

			for x in threads:
				x.join()

			simComparison1.draw(i, int(self.dmgRad[0]), int(self.dmgRad[1] + 1), simComparison1.xn)
			simComparison1.xn = copy.deepcopy(simComparison1.eca.evolve(simComparison1.xn))
			simComparison2.draw(i, int(self.dmgRad[0]), int(self.dmgRad[1] + 1), simComparison2.xn)
			simComparison2.xn = copy.deepcopy(simComparison2.eca.evolve(simComparison2.xn))

			sim2.stepForward(i, sim1.xn)
			sim1.stepForward(i)

			if(self.analysisOp[2]):
				self.getDefectSpreading((i + 1), sim1.xn, sim2.xn)

		# print(self.defects[self.dfctPos])
		
		sim1.saveToPNG(path, "SimAnalysis.png")
		sim2.saveToPNG(path, "SimDefects.png")
		simComparison1.saveToPNG(path, "SimOriginal.png")
		simComparison2.saveToPNG(path, "SimAlter.png")

		self.getLyapExp(sim1.steps)
		print(self.defects[self.dfctPos])
		
		# threads = []
		# if(self.analysisOp[2]):
		# 	x = threading.Thread(target=self.getLyapExp, args=(self.defectsn, len(self.defectsn), sim1.steps))
		# 	threads.append(x)
		# 	x.start()
		# 	x = threading.Thread(target=self.getLyapExp, args=(self.defects, len(self.defects), sim1.steps))
		# 	threads.append(x)
		# 	x.start()

		# for x in threads:
		# 	x.join()

		if(self.analysisOp[0]):
			plotDensity(self.dens, sim1.xn.length, path)

		if(self.analysisOp[1]):
			plotEntropy(self.entropy, path)

		if(self.analysisOp[2]):
			plt.figure("Lyapunov exponents")
			plt.plot(self.defects, "m,-")
			plt.savefig(path + "SimLyapunovExp.png")
			plt.clf()
			plt.figure("Lyapunov exponents Norm")
			plt.plot(self.defectsn, "m,-")
			plt.savefig(path + "SimLyapunovExpNorm.png")
			plt.clf()

	def ruleAnalysis(self):
		print("Rule analysis")

	def setDefect(self):
		x = copy.deepcopy(self.eca.x)
		x.bits[self.dfctPos] = not(self.eca.x.bits[self.dfctPos])
		
		return x

	def getDefectSpreading(self, step, t, tp):
		self.dmgRad[0] = self.dfctPos
		self.dmgRad[1] = self.dfctPos

		if(step > 0):
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

			if((self.dmgRad[1] - self.dmgRad[0]) > (2 * step)):
				self.dmgRad[0] = self.dfctPos

		self.countDefects(t, tp)
	
	def countDefects(self, t, tp):
		for c in range(self.dmgRad[0], int(self.dmgRad[1] + 1)):
			self.defectsn[c] += 1

			if(t.bits[c] ^ tp.bits[c]):
				self.defects[c] += 1

	def getDensity(self, step, xn):
		n = 0
		for i in range(xn.length):
			if(xn.bits[i]):
				n += 1
		
		n *= 100
		n = int(n // xn.length)

		self.dens[step] = n

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

		self.entropy[step] = entropy

	# def getTrinomialRow(self, n):
	# 	if(len(n) == 1):
	# 		n.append(1)
			
	# 		return n
	# 	else:
	# 		nt = []
	# 		nt.append((n[0] +  (n[1] * 2)))
	# 		for i in range(1, (len(n))):
	# 			if(i != (len(n) - 1)):
	# 				k = n[i - 1] + n[i] + n[i + 1]
	# 			else:
	# 				k = n[i - 1] + n[i]	
	# 			nt.append(k)
	# 		nt.append(1)

	# 		#return nt
	# 		self.ttrow = copy.deepcopy(nt)

	def getLyapExp(self, t):
		for i in range(len(self.defects)):
			if(self.defects[i] > 0):
				self.defects[i] = (math.log(self.defects[i])) / t 

		for i in range(len(self.defectsn)):
			if(self.defectsn[i] > 0):
				self.defectsn[i] = (math.log(self.defectsn[i])) / t 
