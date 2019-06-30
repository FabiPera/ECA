import numpy as np, copy
from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import as_completed
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
	xn = Bitstring()
	#threadpool = ThreadPoolExecutor(64)

	def __init__(self, rule=0, length=8):
		self.rule.bsFromInt(rule)
		self.xn = Bitstring(length)

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
			self.xn.bits=np.ones(self.xn.length, dtype=np.uint8)

		self.xn.bsFromString(seed)

	def setRandConf(self, denPer=50):
		"""
		Initializes a random configuration.

		Parameters
		----------
			denPer: int
				Percentage of cells with value equals to 1.
		"""
		dens = ((denPer * self.xn.length) // 100)
		self.xn.bsFromRandomVal(dens)
	
	def threadingEvol(self, i):
		neighb=Bitstring(3)
		neighb.bits[2]=self.xn.getValue(i - 1)
		neighb.bits[1]=self.xn.getValue(i)
		neighb.bits[0]=self.xn.getValue(i + 1)
		n=neighb.binToInt()
		if(self.rule.bits[n]):
			return 1
		else:
			return 0


	def evolve(self):
		"""
		Evolves a configuration with the ECA rule.
		
		Parameters
		----------
			t : Bitstring
				Configuration to evolve.

		Returns
		-------
			tn : Bitstring
				Configuration evolved.
		
		neighb=Bitstring(3)
		tn=Bitstring(t.length)
		n=0
		for i in range(t.length):
			neighb.bits[2]=t.getValue(i - 1)
			neighb.bits[1]=t.getValue(i)
			neighb.bits[0]=t.getValue(i + 1)
			n=neighb.binToInt()
			if(self.rule.bits[n]):
				tn.bits[i]=1
			else:
				tn.bits[i]=0

		return tn
		"""
		indices = [i for i in range(self.xn.length)]
		with ThreadPoolExecutor(max_workers = 64) as executor:
			results = executor.map(self.threadingEvol, indices)
		r = ""
		for result in results:
			r += str(result)
		
		#print(r)
		
		tn = Bitstring(len(r))
		tn.bsFromString(r)

		self.xn = copy.deepcopy(tn)