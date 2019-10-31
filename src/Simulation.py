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
	
	"""
	Simulation object containst the representation of a ECA evolution.

	Parameters
	----------
	steps : int
		Value of steps for the evolution.
	size : int 
		Value of the cell's size 
	s0Color : Gdk.RGBA
		Color for the cells in state 0.
	s1Color : Gdk.RGBA
		Color for the cells in state 1.
	bColor : Gdk.RGBA
		Color for the background.
	dColor : Gdk.RGBA
		Color for the cells with a defect.
	eca : ECA
		ECA which going to evolve in the simulation.

	Attributes
	----------
	steps : int
		Value of steps for the evolution.
	eca : ECA
		ECA which going to evolve in the simulation.
	xn : Bitstring
		Current configuration in the evolution.
	cellSize: int
		Value of the cell's size.
	dColor : Gdk.RGBA
		Color for the cells with a defect.
	s0Color : Gdk.RGBA
		Color for the cells in state 0.
	s1Color : Gdk.RGBA
		Color for the cells in state 1.
	bColor: Gdk.RGBA
		Color for the background.
	surface : cairo.ImageSurface
		Surface in which the simulation will be drawn
	"""

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

		"""
		Sets the size of the cells in the simulation.

		Parameters
		----------
		cellSize : int
			Value for the cell's size
		"""

		self.cellSize = cellSize

	def sets0Color(self, color):

		"""
		Sets the color for the cells with state 0.

		Parameters
		----------
		color : Gdk.RGBA
			RGBA object that contains the color to draw cells with state 0.
		"""

		self.s0Color = Gdk.RGBA(color.red, color.green, color.blue, 1)

	def sets1Color(self, color):

		"""
		Sets the color for the cells with state 1.

		Parameters
		----------
		color : Gdk.RGBA
			RGBA object that contains the color to draw cells with state 1.
		"""

		self.s1Color = Gdk.RGBA(color.red, color.green, color.blue, 1)

	def setbColor(self, color):

		"""
		Sets the color for the background.

		Parameters
		----------
		color : Gdk.RGBA
			RGBA object that contains the color to draw the background.
		"""

		self.bColor = Gdk.RGBA(color.red, color.green, color.blue, 1)

	def setdColor(self, color):

		"""
		Sets the color for the cells with a defect.

		Parameters
		----------
		color : Gdk.RGBA
			RGBA object that contains the color to draw the cells with a defect.
		"""

		self.dColor = Gdk.RGBA(color.red, color.green, color.blue, 1)

	def setECA(self, eca):
		
		"""
		Sets ECA which going to evolve.

		Parameters
		---------
		eca : ECA
			ECA object that contains the rule and initial configuration for the simulation.
		"""

		self.eca = copy.deepcopy(eca)

	def setSteps(self, steps):

		"""
		Sets the time steps for the simulation.

		Parameters
		----------
		steps : int
			Number of time steps the initial configuration is going to evolve.
		"""

		self.steps = steps

	def setXn(self, x):

		"""
		Sets the configuration in the n-th time step.

		Parameters
		----------
		x : Bitstring
			Bitstring that contains the configuration value in the n-th time step.
		"""

		self.xn = copy.deepcopy(x)

	def setSurface(self):

		"""
		Sets the surface configuration in which the simulation will be drawn.
		"""

		self.surface = cairo.ImageSurface(cairo.FORMAT_RGB24, (self.xn.length * self.cellSize), (self.steps * self.cellSize))

	def stepForward(self, i, xp=None):

		"""
		Evolves the current configuration one time step.

		Parameters
		----------
			i : int
				Current time step of the simulation.
			xp : Bitstring
				Cnofiguration 
		"""

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

	def saveToPNG(self, path="../img/simulation/", fileName="simulation.png"):
		simpng = path + fileName
		self.surface.write_to_png(simpng)
		print("PNG written")