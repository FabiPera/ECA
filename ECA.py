import numpy as np, copy, math, sys, pygame
from pygame.locals import *
from BitString import BitString

class ECA:
	
	rule=BitString(8)
	seedConfig=BitString(21)
	t0=BitString(21)
	tDam=BitString(21)
	damageFreq=np.zeros(21, dtype=int)
	steps=0
	denPer=0
	dmgPos=0
	entStringLen=3
	t0Freq=0
	damFreq=0
	strProb=np.zeros(2 ** entStringLen, dtype=float)
	dmgR=np.zeros(2, dtype=int)
	lyapExp=np.zeros(21, dtype=float)
	hX=0.0
	#Pygame variables
	cellColor=(0, 0, 0)
	bckgColor=(255, 255, 255)
	bckgGColor=(160, 160, 160)
	defectColor=(255, 0, 0)
	screen=pygame.Surface((0, 0))

	def __init__(self, r=94, s=512, l=1024):
		self.rule.bsFromInt(r)
		self.steps=s
		self.seedConfig=BitString(l)
		self.t0=BitString(l)
		self.tDam=BitString(l)
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
			neighb.bits[2]=t0.getValue(i - 1)
			neighb.bits[1]=t0.getValue(i)
			neighb.bits[0]=t0.getValue(i + 1)
			n=neighb.binToInt()
			if (self.rule.bits[n]):
				t1.bits[i]=1
			else:
				t1.bits[i]=0

		return t1
	
	def createSimScreen(self, hStr, width, height):
		self.screen=pygame.Surface((width, height))
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
					if dmgBitstr.bits[i]:
						self.screen.fill(self.cellColor, (x, y, 2, 2))
					else:
						self.screen.fill(self.bckgColor, (x, y, 2, 2))
			x += 2

	def drawCone(self, dmgBitstr, y):
		if (y == 0):
			if dmgBitstr.bits[self.dmgPos]:
				self.screen.fill(self.cellColor, (self.dmgPos * 2, 0, 2, 2))
			else:
				self.screen.fill(self.bckgColor, (self.dmgPos * 2, 0, 2, 2))
		else:
			y *= 2
			x=self.dmgR[0]
			for i in range(self.dmgR[0], self.dmgR[1] + 1):
				if dmgBitstr.bits[i]:
					self.screen.fill(self.cellColor, (x * 2, y, 2, 2))
				else:
					self.screen.fill(self.bckgColor, (x * 2, y, 2, 2))
				x += 1

	def saveToPNG(self, file):
		pygame.image.save(self.screen, file)
		print("Simulation saved")
	
	def setDamage(self):
		self.damageFreq=np.zeros(self.t0.length)
		self.lyapExp=np.zeros(self.t0.length, dtype=float)
		self.tDam=BitString(self.t0.length)
		self.t0=copy.deepcopy(self.seedConfig)
		self.tDam=copy.deepcopy(self.seedConfig)
		self.tDam.bits[self.dmgPos]=not(self.tDam.bits[self.dmgPos])

	def getConeRatio(self, t, y):
		if (y == 0):
			self.dmgR[0]=self.dmgPos
			self.dmgR[1]=self.dmgPos
		else:
			i=0
			while(i < self.dmgPos):
				if (self.t0.bits[i] ^ t.bits[i]):
					self.dmgR[0]=i
					break
				else:
					i += 1

			i=self.t0.length - 1
			while(i > self.dmgPos):
				if (self.t0.bits[i] ^ t.bits[i]):
					self.dmgR[1]=i
					break
				else:
					i -= 1

			if ((self.dmgR[1] - self.dmgR[0]) > (2 * y)):
				self.dmgR[0]=self.dmgPos
		
	def countDefects(self):
		for x in range(self.dmgR[0], self.dmgR[1]):
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
		for i in range(self.t0.length - entStringLen):
			k=i
			for j in range(self.entStringLen):
				str.bits[j]=self.t0.bits[k]
				k += 1
			n=str.binToInt()
			strProb[n] += 1.0
		
		for i in range(2 ** entStringLen):
			if (strProb[i]):
				strProb[i]=strProb[i] / (2 ** entStringLen)
				theta += 1
			
		self.hX=((1.0 / self.entStringLen) * math.log(theta, 2))

			
'''
print("Create ECA")
eca=ECA(94, 512, 1024)
eca.setT0("11111", 0)
print(eca.seedConfig)
eca.dmgPos=513
#eca.dmgPos=510
#eca.dmgPos=511
#eca.dmgPos=512
#eca.dmgPos=513
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

	eca.updateScreen(y=i, bitStr=eca.t0, dmgBitstr=eca.tDam)
	eca.getTopEntropy(3)
	#print(eca.tDam)
	eca.t0=copy.deepcopy(eca.evolve(eca.t0))
	eca.tDam=copy.deepcopy(eca.evolve(eca.tDam))
	#print(eca.hX)

eca.saveToPNG("Simulation18Dam5.png")
'''