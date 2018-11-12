from BitString import BitString
import numpy as np, copy, math

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

	def __init__(self, r, s, l):
		#self.rule=BitString(8)
		self.rule.bsFromInt(r)
		self.steps=s
		self.seedConfig=BitString(l)
		self.t0=BitString(l)
		self.tDam=BitString(l)
		self.frequencies=np.zeros(self.steps)
		self.damaFreq=np.zeros(l)

	def setT0(self, str0):
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
eca=ECA(30, 50, 21)
eca.setT0("0101101110010010001")
print(eca.seedConfig)
eca.dmgPos=9
eca.setDamage()
print(eca.rule)
for i in range(eca.steps):
	for j in range(eca.t0.length):
		if (eca.t0.bits[j] ^ eca.tDam.bits[j]):
			eca.damageFreq[j] += 1
	
	if (i > 0):
		lyapN=eca.countDefects()
		lyapExp=eca.getLyapunovExp(1, lyapN)
		#print(lyapExp)

	eca.getTopEntropy(3)
	eca.t0.copyBitString(eca.evolve(eca.t0))
	eca.tDam.copyBitString(eca.evolve(eca.tDam))
	print(eca.hX)
		