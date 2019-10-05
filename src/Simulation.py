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

	def __init__(self, rule=0, length=5000):
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
	cellSize = 1
	dColor = Gdk.RGBA(1, 0, 0, 1)
	s0Color = Gdk.RGBA(1, 1, 1, 1)
	s1Color = Gdk.RGBA(0, 0, 0, 1)
	bColor = Gdk.RGBA(0.62, 0.62, 0.62, 1)
	surface = cairo.ImageSurface(cairo.FORMAT_RGB24, 0, 0)

	def __init__(self, steps, size, s0Color, s1Color, bColor, dColor, eca=ECA()):
		self.setECA(eca)
		self.setSteps(steps)
		self.setCellSize(size)
		self.setXn(eca.x)
		self.setSurface()
		self.sets1Color(s1Color)
		self.sets0Color(s0Color)
		self.setdColor(dColor)
		self.setbColor(bColor)
		context = cairo.Context(self.surface)
		context.rectangle(0, 0, (self.xn.length * self.cellSize), (self.steps * self.cellSize))
		context.set_source_rgb(self.bColor.red, self.bColor.green, self.bColor.blue)
		context.fill()

	def setCellSize(self, cellSize):
		self.cellSize = cellSize

	def sets0Color(self, color):
		self.s0Color = Gdk.RGBA(color.red, color.green, color.blue, 1)

	def sets1Color(self, color):
		self.s1Color = Gdk.RGBA(color.red, color.green, color.blue, 1)

	def setbColor(self, color):
		self.bColor = Gdk.RGBA(color.red, color.green, color.blue, 1)

	def setdColor(self, color):
		self.dColor = Gdk.RGBA(color.red, color.green, color.blue, 1)

	def setECA(self, eca):
		self.eca = copy.deepcopy(eca)

	def setSteps(self, steps):
		self.steps = steps

	def setXn(self, x):
		self.xn = copy.deepcopy(x)

	def setSurface(self):
		self.surface = cairo.ImageSurface(cairo.FORMAT_RGB24, (self.xn.length * self.cellSize), (self.steps * self.cellSize))

	def stepForward(self, i, xp=None):
		self.draw(y=i, t=self.xn, tp=xp)
		self.xn = copy.deepcopy(self.eca.evolve(self.xn))

	def draw(self, y=0, xL=0, xR=None, t=None, tp=None):
		context = cairo.Context(self.surface)
		context.set_line_width(0.5)

		if(xR == None):
			xR = t.length

		y *= self.cellSize
		x = xL * self.cellSize

		for i in range(xL, xR):
			if(tp == None):
				if(t.bits[i]):
					context.rectangle(x, y, self.cellSize, self.cellSize)
					context.set_source_rgb(self.s1Color.red, self.s1Color.green, self.s1Color.blue)
					context.fill()
				else:
					context.set_source_rgb(self.s1Color.red, self.s1Color.green, self.s1Color.blue)
					context.rectangle(x, y, self.cellSize, self.cellSize)
					context.set_source_rgb(self.s0Color.red, self.s0Color.green, self.s0Color.blue)
					context.fill()
			else:
				if(t.bits[i] ^ tp.bits[i]):
					context.rectangle(x, y, self.cellSize, self.cellSize)
					context.set_source_rgb(self.dColor.red, self.dColor.green, self.dColor.blue)
					context.fill()
				else:
					if(t.bits[i]):
						context.rectangle(x, y, self.cellSize, self.cellSize)
						context.set_source_rgb(self.s1Color.red, self.s1Color.green, self.s1Color.blue)
						context.fill()
					else:
						context.set_source_rgb(self.s1Color.red, self.s1Color.green, self.s1Color.blue)
						context.rectangle(x, y, self.cellSize, self.cellSize)
						context.set_source_rgb(self.s0Color.red, self.s0Color.green, self.s0Color.blue)
						context.fill()
			x += self.cellSize

	def saveToPNG(self, path="../sim/", fileName="simulation.png"):
		simpng = path + fileName
		self.surface.write_to_png(simpng)
		print("PNG written")