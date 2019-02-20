import numpy as np, copy, random

class BitString:
	
	"""
	Attributes
	----------
		bits : numpy array
			contains the values of the bitstring
		length : int 
			length of the bitstring
	"""
	bits=np.zeros(8, dtype=int)
	length=8

	def __init__(self, l):
		self.bits=np.zeros(l, dtype=int)
		self.length=l

	def bsFromInt(self, n):
		"""
		Initialize the bitstring from a number in base 10

		Parameters
		----------
			n : int
				number in base 10 to convert
		"""
		self.bits=self.intToBin(n, self.length)

	def setStringBits(self, str):
		"""
		Initialize the bitstring from a string.

		Parameters
		----------
			str : string
				string with the values for the bitstring.
		"""
		x=self.length - len(str)
		x=x // 2
		for i in range(len(str)):
			if (str[i] == '1'):
				self.bits[x + i]=1
			else:
				self.bits[x + i]=0

	def setRandomBits(self, dens):
		"""
		Initialize the bitstring with a random configuration.

		Parameters
		----------
			dens : int
				density of 1 values in the bitstring.
		"""
		self.bits=np.ones(self.length, dtype=int)
		freq=self.length
		while(freq > dens):
			n=random.randint(0, self.length - 1)
			if (self.bits[n]):
				self.bits[n]=0
				freq -= 1

	def __str__(self):
		"""
		Get the string form of a bitstring

		Returns
		-------
			string
				string from the values of the bitstring numpy array
		"""
		string=""
		for i in range(self.length):
			string=string+str(self.bits[i])
		
		return string

	def getValue(self, i):
		"""
		Get the value of the element in certain position

		Parameters
		----------
			i : int
				position of the element.

		Returns
		-------
			bits[mod(i)]
				the element in the position mod(i) (gets the module of i due to ring condition)
		"""
		n=self.mod(i)
		return self.bits[n]


	def mod(self, n):
		"""
		Gets the module of a number based in the length of the bitstring.

		Parameters
		----------
			n : int
				number to get the module.
		"""
		if (n < 0):
			return self.length + n
		else:
			return n % self.length
	
	def binToInt(self):
		"""
		Get the base 10 value of the bitstring.

		Returns
		-------
			n : int
				base 10 value of the bitstring.
		"""
		n=0
		for i in range(self.length):
			if self.bits[i]:
				n += (2 ** i)
		
		return n

	def intToBin(self, n, size):
		"""
		Get a bitstring from a int.

		Parameters
		----------
			n : int
				decimal number to convert.
			size : int
				number of bits for the bitstring.
		
		Returns
		-------
			bits : numpy array
				base 2 value of the base 10 number n.
		"""
		b=np.zeros(size, dtype=int)
		bits=np.zeros(size, dtype=int)
		i=0
		j=0
		while(n):
			b[i]=(n % 2)
			n=(n // 2)
			i += 1
		i -= 1
		
		while(j < size):
			if(i >= 0):
				bits[i]=b[i]
				i -= 1
			j += 1

		return bits

'''
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
00000000000000000000000
000000000000000000000000
'''