import numpy as np, copy, gi, cairo, Plotter
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gio, Gdk
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

class Simulation:
	
	steps = 0
	eca = ECA()
	xn = Bitstring()

	def __init__(self, eca=ECA()):
		self.eca = copy.deepcopy(eca)
		self.xn = copy.deepcopy(eca.x)

	def setSteps(self, steps=512):
		self.steps = steps

	def setECA(self, eca=ECA()):
		self.eca = copy.deepcopy(eca)

	def setXn(self, xn=Bitstring()):
		self.xn = copy.deepcopy(xn)

	def runSimulation(self):
		width = self.eca.x.length * 1
		height = self.steps * 1
		surface = cairo.ImageSurface(cairo.FORMAT_RGB24, width, height)
		for i in range(self.steps):
			Plotter.drawSimStep(surface, y=i, t=self.xn)
			self.xn = copy.deepcopy(self.eca.evolve(self.xn))
		surface.write_to_png("../img/Simulation.png")

	def nextStep(self, x=None):
		self.xn = copy.deepcopy(self.eca.evolve(self.xn))
		steps -= 1

class SimSettings():

	cellSize = 1
	state0Color = Gdk.RGBA(1, 1, 1, 1)
	state1Color = Gdk.RGBA(0, 0, 0, 1)
	bckgColor = Gdk.RGBA(0.62, 0.62, 0.62, 1)
	dfctColor = Gdk.RGBA(1, 0, 0, 1)

	def __init__(self, cellSize=1, state0Color=Gdk.RGBA(1, 1, 1, 1), state1Color=Gdk.RGBA(0, 0, 0, 1), bckgColor=Gdk.RGBA(0.62, 0.62, 0.62, 1), dfctColor=Gdk.RGBA(1, 0, 0, 1)):
		self.cellSize = cellSize
		self.state0Color = state0Color
		self.state1Color = state1Color
		self.bckgColor = bckgColor
		self.dfctColor = dfctColor

	def setCellSize(self, cellSize=1):
		self.cellSize = cellSize

	def setState0Color(self, state0Color=Gdk.RGBA(1, 1, 1, 1)):
		self.state0Color = state0Color

	def setState1Color(self, state1Color=Gdk.RGBA(0, 0, 0, 1)):
		self.state1Color = state1Color

	def setBckgColor(self, bckgColor=Gdk.RGBA(0.62, 0.62, 0.62, 1)):
		self.bckgColor = bckgColor

	def setDfctColor(self, dfctColor=Gdk.RGBA(1, 0, 0, 1)):
		self.dfctColor = dfctColor

	
