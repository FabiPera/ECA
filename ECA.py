import numpy as np, copy, math, sys, pygame
from pygame.locals import *
from BitString import BitString

class ECA:
	
	rule=BitString(8)
	seedConfig=BitString(21)
	t0=BitString(21)
	tDam=BitString(21)
	frequencies=np.zeros(50, dtype=int)
	damageFreq=np.zeros(21, dtype=int)
	steps=0
	denPer=0
	dmgPos=0
	entStringLen=3
	t0Freq=0
	damFreq=0
	strProb=np.zeros(2 ** entStringLen, dtype=float)
	hX=0.0
	hXMetric=0.0
	#Pygame variables
	cellColor=(0, 0, 0)
	bckgColor=(255, 255, 255)
	defectColor=(255, 0, 0)
	screen=pygame.display.set_mode((200, 200))

	def __init__(self, r, s, l):
		self.rule.bsFromInt(r)
		self.steps=s
		self.seedConfig=BitString(l)
		self.t0=BitString(l)
		self.tDam=BitString(l)
		self.frequencies=np.zeros(self.steps)
		self.damaFreq=np.zeros(l)

	def setT0(self, str0, oz):
		if (oz):
			self.seedConfig.bits=np.ones(self.seedConfig.length, dtype=int)

		self.seedConfig.setStringBits(str0)
		self.t0=copy.deepcopy(self.seedConfig)

	def setRandomT0(self):
		dens=((self.denPer * self.t0.length) // 100)
		self.seedConfig.setRandomBits(dens)
		self.t0=copy.deepcopy(self.seedConfig)

	def evolve(self, t0):
		t1=BitString(t0.length)
		n=0
		neighb=BitString(3)
		for i in range(t0.length):
			neighb.bits[2]=t0.getValue(i-1)
			neighb.bits[1]=t0.getValue(i)
			neighb.bits[0]=t0.getValue(i+1)
			n=neighb.binToInt()
			if (self.rule.bits[n]):
				t1.bits[i]=1
			else:
				t1.bits[i]=0

		return t1
	
	def createSimScreen(self, hStr, width, height):
		pygame.init()
		self.screen=pygame.display.set_mode((width, height))
		pygame.display.set_caption(hStr)
		self.screen.fill(self.bckgColor)

	def updateScreen(self, y, bitStr=None, dmgBitstr=None):
		y *= 2
		x=0
		for i in range(bitStr.length):
			if (dmgBitstr == None):
				if bitStr.bits[i]:
					self.screen.fill(self.cellColor, (x, y, 2, 2))
				else:
					self.screen.fill(self.bckgColor, (x, y, 2, 2))
			else:
				if (bitStr.bits[i] ^ dmgBitstr.bits[i]):
					self.screen.fill(self.defectColor, (x, y, 2, 2))
				else:
					if bitStr.bits[i]:
						self.screen.fill(self.cellColor, (x, y, 2, 2))
					else:
						self.screen.fill(self.bckgColor, (x, y, 2, 2))
			x += 2

	def saveToPNG(self, file):
		pygame.image.save(self.screen, file)
	
	def setDamage(self):
		self.damageFreq=np.zeros(self.t0.length)
		self.tDam=BitString(self.t0.length)
		self.t0=copy.deepcopy(self.seedConfig)
		self.tDam=copy.deepcopy(self.seedConfig)
		self.tDam.bits[self.dmgPos]=~(self.tDam.bits[self.dmgPos])

	def countDefects(self):
		defects=0
		for i in range(self.t0.length):
			defects += self.damageFreq[i]

		return defects

	def getLyapunovExp(self, a, b):
		lyapExp=((1.0 / self.steps) * math.log(b / a))
		return lyapExp

	def getTopEntropy(self, size):
		str=BitString(size)
		entStringLen=size
		strProb=np.zeros(2 ** entStringLen, dtype=float)
		theta=0.0
		for i in range(self.t0.length - entStringLen):
			k=i
			for j in range(size):
				str.bits[j]=self.t0.bits[k]
				k += 1
			n=str.binToInt()
			strProb[n] += 1.0
		
		for i in range(2 ** entStringLen):
			if (strProb[i]):
				theta += 1
			
		self.hX=((1.0 / size) * math.log(theta, 2))
			

print("Create ECA")
eca=ECA(30, 50, 50)
eca.setT0("000", 1)
print(eca.seedConfig)
eca.dmgPos=9
eca.setDamage()
print(eca.rule)
eca.createSimScreen("Simulation", eca.seedConfig.length*2, eca.steps*2)
for i in range(eca.steps):
	for j in range(eca.t0.length):
		if (eca.t0.bits[j] ^ eca.tDam.bits[j]):
			eca.damageFreq[j] += 1
	
	if (i > 0):
		lyapN=eca.countDefects()
		lyapExp=eca.getLyapunovExp(1, lyapN)
		#print(lyapExp)

	eca.updateScreen(y=i, bitStr=eca.t0, dmgBitstr=None)
	eca.getTopEntropy(3)
	print(eca.t0)
	eca.t0=copy.deepcopy(eca.evolve(eca.t0))
	eca.tDam=copy.deepcopy(eca.evolve(eca.tDam))
	#print(eca.hX)

eca.saveToPNG(".Simulation.png")
		