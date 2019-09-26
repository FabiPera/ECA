import numpy as np, copy, gi, cairo
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

	eca = ECA()
	steps = 0
	xn = Bitstring()
	cellSize = 1
	state0Color = Gdk.RGBA(1, 1, 1, 1)
	state1Color = Gdk.RGBA(0, 0, 0, 1)
	bckgColor = Gdk.RGBA(0.62, 0.62, 0.62, 1)
	dfctColor = Gdk.RGBA(1, 0, 0, 1)
	surface = cairo.ImageSurface(cairo.FORMAT_RGB24, 0, 0)

	def __init__(self, eca=ECA(), steps=512):
		self.eca = copy.deepcopy(eca)
		self.steps = steps
		self.xn = copy.deepcopy(eca.x)
		self.surface = cairo.ImageSurface(cairo.FORMAT_RGB24, self.xn.length, self.steps)
		context = cairo.Context(self.surface)
		context.rectangle(0, 0, self.xn.length, self.steps)
		context.set_source_rgb(self.bckgColor.red, self.bckgColor.green, self.bckgColor.blue)
		context.fill()

	def setCellSize(self, cellSize):
		self.cellSize = cellSize

	def setState0Color(self, color):
		self.state0Color = color.copy()

	def setState1Color(self, color):
		self.state1Color = color.copy()

	def setBckgColor(self, color):
		self.bckgColor = color.copy()

	def setDfctColor(self, color):
		self.dfctColor = color.copy()

	def setECA(self, eca):
		self.eca = copy.deepcopy(eca)

	def setSteps(self, steps):
		self.steps = steps

	def setXn(self, x):
		self.xn = copy.deepcopy(x)

	def stepForward(self, i, xp=None):
		self.draw(y=i, t=self.xn, tp=xp)
		self.xn = copy.deepcopy(self.eca.evolve(self.xn))

	def draw(self, y=0, xL=None, xR=None, t=None, tp=None):
		context = cairo.Context(self.surface)

		if(xL == None and xR == None):
			xL = 0
			xR = t.length

		y *= self.cellSize
		x = xL * self.cellSize

		for i in range(xL, xR):
			if(tp == None):
				if(t.bits[i]):
					context.rectangle(x, y, self.cellSize, self.cellSize)
					context.set_source_rgb(self.state1Color.red, self.state1Color.green, self.state1Color.blue)
					context.fill()
				else:
					context.rectangle(x, y, self.cellSize, self.cellSize)
					context.set_source_rgb(self.state0Color.red, self.state0Color.green, self.state0Color.blue)
					context.fill()
			else:
				if(t.bits[i] ^ tp.bits[i]):
					context.rectangle(x, y, self.cellSize, self.cellSize)
					context.set_source_rgb(self.dfctColor.red, self.dfctColor.green, self.dfctColor.blue)
					context.fill()
				else:
					if(t.bits[i]):
						context.rectangle(x, y, self.cellSize, self.cellSize)
						context.set_source_rgb(self.state1Color.red, self.state1Color.green, self.state1Color.blue)
						context.fill()
					else:
						context.rectangle(x, y, self.cellSize, self.cellSize)
						context.set_source_rgb(self.state0Color.red, self.state0Color.green, self.state0Color.blue)
						context.fill()
			x += self.cellSize

	def saveToPNG(self, path="../img/", fileName="simulation.png"):
		simpng = path + fileName
		self.surface.write_to_png(simpng)
		print("PNG written")