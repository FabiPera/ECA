import numpy as np, copy
from Bitstring import Bitstring

class ECA:

	"""
	ECA object contains the representation of a Elementary Cellular Automata.

	Parameters
	----------
		rule : int
			Value of the rule.
		length : int
			Number of cells in the configuration.

	Attributes
	----------
		rule : Bitstring
			Base 2 representation of the rule.
		neighb : Bitstring
			Bitstring to compute the neighborhood of the current cell.
		initConf : Bitstring 
			Initial configuration of the ECA.
	"""
	rule = Bitstring(8)
	x = Bitstring()

	def __init__(self, rule=0, length=8):
		self.rule.bsFromInt(rule)
		self.x = Bitstring(length)

	def setConf(self, seed, oz):
		"""
		Initializes the configuration from a string.

		Parameters
		----------
			seed : string
				Seed string to initalize the configuration.
			oz : int
				Value to fill the remaining cells (0 or 1).
		"""
		if(oz):
			self.x.bits = np.ones(self.x.length, dtype=np.uint8)

		self.x.bsFromString(seed)

	def setRandConf(self, denPer=50):
		"""
		Initializes a random configuration.

		Parameters
		----------
			denPer: int
				Percentage of cells with value equals to 1.
		"""
		dens = ((denPer * self.x.length) // 100)
		self.x.bsFromRandomVal(dens)

	def evolve(self, x):
		"""
		Evolves a configuration with the ECA rule.
		
		Parameters
		----------
			t : Bitstring
				Configuration to evolve.

		Returns
		-------
			xn : Bitstring
				Configuration evolved.
		"""
		neighb = Bitstring(3)
		xn = Bitstring(x.length)
		n = 0
		for i in range(x.length):
			neighb.bits[2] = x.getValue(i - 1)
			neighb.bits[1] = x.getValue(i)
			neighb.bits[0] = x.getValue(i + 1)
			n = neighb.binToInt()
			if(self.rule.bits[n]):
				xn.bits[i] = 1
			else:
				xn.bits[i] = 0

		return xn