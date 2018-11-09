import numpy as np, copy, random

class BitString:
	
	bits=np.zeros(8, dtype=int)
	length=8

	def __init__(self, l):
		self.bits=np.zeros(l, dtype=int)
		self.length=l
	
	def bsFromInt(self, n):
		self.bits=self.intToBin(n, self.length)

	def __str__(self):
		string=""
		for i in range(self.length):
			string=string+str(self.bits[i])
		
		return string

	def copyBitString(self, bs):
		b=copy.deepcopy(bs)
		return b

	def getValue(self, i):
		n=self.mod(i)
		return self.bits[n]

	def setStringBits(self, str):
		for i in range(len(str)):
			if (str[i] == '1'):
				self.bits[i]=1
			else:
				self.bits[i]=0

	def setRandomBits(self, dens):
		freq=0
		while(freq < dens):
			n=random.randint(0, self.length)
			if (self.bits[n] != 1):
				self.bits[n]=1
				freq += 1


	def mod(self, n):
		if (n < 0):
			return self.length + n
		else:
			return n % self.length
	
	def binToInt(self):
		n=0
		for i in range(self.length):
			if self.bits[i]:
				n += (2 ** i)
		
		return n

	def intToBin(self, n, size):
		b=np.zeros(size, dtype=int)
		bits=np.zeros(size, dtype=int)
		i=0
		j=0
		while(n):
			b[i]=(n % 2)
			n=(n // 2)
			i += 1
		i -= 1
		print(b)
		
		while(j < size):
			if(i >= 0):
				bits[i]=b[i]
				i -= 1
			j += 1

		return bits

print("Create BitString")
bitS=BitString(8)
print(bitS)
print("Set BitString int value")
bitS.bsFromInt(10)
print(bitS)
print(bitS.binToInt())

config=BitString(50)
dens=(50 * 50) // 100
config.setRandomBits(dens)
print(config)

configStr=BitString(10)
configStr.setStringBits("0111101010")
print(configStr)