import numpy as np, copy, random, math
from numba import njit

class BitString:
	"""
	The BitString object contains the representation in base 2 of a base 10 number.

	Parameters
	----------
	l : int 
		Length of the bitstring.

	Attributes
	----------
	bits : unsigned int8 array.
		Contains the values of the bitstring.
	length : int 
		Length of the bitstring.
	"""
	bits=np.zeros(8, dtype=np.uint8)
	length=8

	def __init__(self, l):
		self.bits=np.zeros(l, dtype=np.uint8)
		self.length=l

	def bsFromInt(self, n):
		"""
		Initialize the bitstring from a base 10 number.

		Parameters
		----------
		n : int
			Base 10 number to convert.
		"""
		self.bits=self.intToBin(n, self.length)

	def bsFromString(self, str):
		"""
		Initialize the bitstring from a string.

		Parameters
		----------
		str : string
			String with the values for the bitstring.
		"""
		x=self.length - len(str)
		x=x // 2
		for i in range(len(str)):
			if (str[i] == '1'):
				self.bits[x + i]=1
			else:
				self.bits[x + i]=0

	def bsFromRandomVal(self, dens):
		"""
		Initialize the bitstring with a random configuration.

		Parameters
		----------
		dens : int
			Density of 1 values in the bitstring.
		"""
		self.bits=np.ones(self.length, dtype=np.uint8)
		freq=self.length
		while(freq > dens):
			n=random.randint(0, self.length - 1)
			if (self.bits[n]):
				self.bits[n]=0
				freq -= 1

	def getValue(self, i):
		"""
		Get the value of the element in certain position.

		Parameters
		----------
		i : int
			Position of the element.

		Returns
		-------
		bits[mod(i)]
			The element in the position mod(i) (gets the module of i due to ring condition).
		"""
		n=self.mod(i)
		return self.bits[n]


	def mod(self, n):
		"""
		Gets the module of a number based in the length of the bitstring.

		Parameters
		----------
		n : int
			Number to get the module.
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
			Base 10 value of the bitstring.
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
			Base 10 number to convert.
		size : int
			Number of bits for the bitstring.
		Returns
		-------
		bits :
			Base 2 value of the base 10 number n.
		"""
		if(n):
			binstr=np.base_repr(n, base=2)
			binstr=np.base_repr(n, base=2, padding=(size - len(binstr)))
			bits=np.zeros(size, dtype=np.uint8)
			x=size - 1
			for i in range(size):
				if(binstr[i] == '1'):
					bits[x]=1
				x -= 1
		else:
			bits=np.zeros(size, dtype=np.uint8)

		return bits
