import numpy as np, copy, gi, Plotter, ECA, Bitstring
gi.require_version('Gtk', '3.0')
from gi.repository import Gdk

class Simulation():

	eca = ECA.ECA()
	steps = 512
	settings = Plotter.SimSettings()
	xn = Bitstring.Bitstring()

	def __init__(self, eca=ECA.ECA(), steps=512, settings=Plotter.SimSettings()):
		self.eca = copy.deepcopy(eca)
		self.steps = steps
		self.settings = copy.deepcopy(settings)
		self.xn = copy.deepcopy(self.eca.x)

	def setECA(self, eca=ECA.ECA()):
		self.eca = copy.deepcopy(eca)

	def setSteps(self, steps):
		self.steps = steps

	def setSettings(self, settings=Plotter.SimSettings()):
		self.settings = copy.deepcopy(settings)
	
	def setXn(self, xn=Bitstring.Bitstring()):
		self.xn = xn


def runSimulation(simulation=Simulation()):
	surface = Plotter.createSurface(simulation.xn.length, simulation.steps, simulation.settings.cellSize)

	for i in range(simulation.steps):
		surface = copy.deepcopy(Plotter.drawSimStep(surface=surface, settings=simulation.settings, y=i, t=simulation.xn))
		simulation.xn = copy.deepcopy(simulation.eca.evolve(simulation.xn))

	return surface
"""
class Simulator(Gtk.Box):	

	tab1Grid = Gtk.Grid()
	adjRule = Gtk.Adjustment.new(0, 0, 256, 1, 1, 1)
	adjDens = Gtk.Adjustment.new(50, 0, 100, 1, 1, 1)
	adjWidth = Gtk.Adjustment.new(8, 8, 8192, 8, 1, 1)
	adjHeigth = Gtk.Adjustment.new(8, 8, 8192, 8, 1, 1)
	switchRandConf = Gtk.Switch.new()
	switchStr = Gtk.Switch.new()
	scaleRule = Gtk.Scale.new(0, adjRule)
	scaleDens = Gtk.Scale.new(0, adjDens)
	entrySeed = Gtk.Entry.new()
	entrySteps = Gtk.SpinButton.new(adjHeigth, 8, 0)
	entryCells = Gtk.SpinButton.new(adjWidth, 8, 0)
	ruleImage = Gtk.Image.new_from_file("../img/rule0.png")
	ruleImageLayout = Gtk.Box(orientation=0, spacing=50)
	switchRandValue = 0
	switchConfValue = 0

	def __init__(self, eca=ECA()):
		super(Simulator, self).__init__(orientation=1, spacing=30)
		self.set_border_width(20)

		labelRule = Gtk.Label.new("Rule:")
		labelRandConf = Gtk.Label.new("Random: ")
		labelConf = Gtk.Label.new("Seed: ")
		labelFill = Gtk.Label.new("Fill w/0:")
		labelSteps = Gtk.Label.new("Steps: ")
		labelCells = Gtk.Label.new("Length: ")
		labelDens = Gtk.Label.new("Density (%): ")
		labelRuleIcon = Gtk.Label.new("Rule 0 icon")

		self.switchStr.set_active(False)
		self.switchRandConf.set_active(False)
		self.scaleDens.set_sensitive(False)

		self.scaleRule.set_digits(0)
		self.scaleDens.set_digits(0)
		
		self.entrySeed.set_width_chars(20)
		self.entrySteps.set_width_chars(5)
		self.entryCells.set_width_chars(5)

		self.tab1Grid.set_row_spacing(10)
		self.tab1Grid.set_column_spacing(25)
		self.tab1Grid.set_column_homogeneous(False)

		layoutRandSwitch = Gtk.Box(orientation=0, spacing=50)
		layoutFillSwitch = Gtk.Box(orientation=0, spacing=50)
		layoutRandSwitch.pack_start(self.switchRandConf, 0, 0, 50)
		layoutFillSwitch.pack_start(self.switchStr, 0, 0, 50)

		self.tab1Grid.attach(labelRandConf, 0, 0, 1, 1)
		self.tab1Grid.attach(layoutRandSwitch, 1, 0, 1, 1)
		self.tab1Grid.attach(labelRuleIcon, 2, 0, 3, 1)
		self.tab1Grid.attach(labelFill, 0, 1, 1, 1)
		self.tab1Grid.attach(layoutFillSwitch, 1, 1, 1, 1)
		self.tab1Grid.attach(labelRule, 0, 2, 1, 1)
		self.tab1Grid.attach(self.scaleRule, 1, 2, 1, 1)
		self.tab1Grid.attach(labelConf, 0, 3, 1, 1)
		self.tab1Grid.attach(self.entrySeed, 1, 3, 1, 1)
		self.tab1Grid.attach(labelSteps, 0, 4, 1, 1)
		self.tab1Grid.attach(self.entrySteps, 1, 4, 1, 1)
		self.tab1Grid.attach(labelCells, 0, 5, 1, 1)
		self.tab1Grid.attach(self.entryCells, 1, 5, 1, 1)
		self.tab1Grid.attach(labelDens, 0, 6, 1, 1)
		self.tab1Grid.attach(self.scaleDens, 1, 6, 1, 1)
		self.tab1Grid.attach(self.ruleImageLayout, 3, 1, 2, 5)
		self.ruleImageLayout.pack_start(self.ruleImage, 1, 0, 0)
		self.pack_start(self.tab1Grid, 1, 0, 0)

		self.switchRandConf.connect("notify::active", self.switchRandActivate)
		self.switchStr.connect("notify::active", self.switchConfActivate)
		self.adjWidth.connect("value_changed", self.changeStepWidth)
		self.adjHeigth.connect("value_changed", self.changeStepHeigth)
		self.scaleRule.connect("value_changed", self.changeRuleImg)
		#self.adjStrLenght.connect("value_changed", self.changeStrLenght)

	def switchRandActivate(self, switchRandConf, active):
		if(switchRandConf.get_active()):
			self.entrySeed.set_sensitive(False)
			self.switchStr.set_sensitive(False)
			self.scaleDens.set_sensitive(True)
			self.switchRandValue = 1
		else:
			self.entrySeed.set_sensitive(True)
			self.switchStr.set_sensitive(True)
			self.scaleDens.set_sensitive(False)
			self.switchRandValue = 0
		
	def switchConfActivate(self, switchStr, active):
		label = self.tab1Grid.get_child_at(0, 1)
		if(switchStr.get_active()):
			self.switchConfValue = 1
			label.set_text("Fill w/1")
		else:
			self.switchConfValue = 0
			label.set_text("Fill w/0")

	def changeRuleImg(self, widget):
		label = self.tab1Grid.get_child_at(2, 0)
		val = int(self.scaleRule.get_value())
		label.set_text("Rule "+str(val)+" icon")
		self.ruleImage.set_from_file("../img/rule"+str(val)+".png")

	def changeStepWidth(self, widget):
		val = self.adjWidth.get_value()
		#self.adjDfctPos.set_upper(val)
		#self.adjDfctPos.set_value((val // 2) - 1)
		if(val):
			self.adjWidth.set_step_increment(val)
		else:
			self.adjWidth.set_step_increment(8)

	def changeStepHeigth(self, widget):
		val = self.adjHeigth.get_value()
		if(val):
			self.adjHeigth.set_step_increment(val)
		else:
			self.adjHeigth.set_step_increment(8)

	def getSwitchRandValue(self):
		return self.switchRandValue

	def getSwitchConfValue(self):
		return self.switchConfValue

	def getRuleValue(self):
		rule = int(self.scaleRule.get_value())
		return rule

	def getSeedValue(self):
		seed = str(self.entrySeed.get_text())
		return seed
		
	def getStepsValue(self):
		steps = int(self.entrySteps.get_value())
		return steps
	
	def getLengthValue(self):
		length = int(self.entryCells.get_value())
		return length

	def getDensValue(self):
		dens = int(self.scaleDens.get_value())
		return dens

	def saveSettings(self, button):
		dialog = Gtk.FileChooserDialog("Save settings", None, Gtk.FileChooserAction.SAVE, (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_SAVE, Gtk.ResponseType.OK))
		response = dialog.run()
		if(response == Gtk.ResponseType.OK):
			rule = self.getRuleValue()
			steps = self.getStepsValue()
			cells = self.getStepsValue()
			seed = self.getSeedValue()

			data = {}
			data["rule"] = rule
			data["seed"] = seed
			data["steps"] = steps
			data["cells"] = cells
			data["fill"] = self.switchConfValue
			fileMan.writeJSON(dialog.get_filename(), data)
			print("Settings saved")
			print("File selected: " + dialog.get_filename())
		elif(response == Gtk.ResponseType.CANCEL):
			print("Cancel clicked")
		dialog.destroy()

	def loadSettings(self, button):
		dialog = Gtk.FileChooserDialog("Load settings", None, Gtk.FileChooserAction.OPEN, (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OPEN, Gtk.ResponseType.OK))
		response = dialog.run()
		if(response == Gtk.ResponseType.OK):
			with open(dialog.get_filename()) as json_file:  
				data = json.load(json_file)
				for p in data['people']:
					print('Name: ' + p['name'])
					print('Website: ' + p['website'])
					print('From: ' + p['from'])
					print('')
			rule = self.getRuleValue()
			steps = self.getStepsValue()
			cells = self.getStepsValue()
			seed = self.getSeedValue()
			print("Settings load")
			print("File selected: " + dialog.get_filename())
		elif(response == Gtk.ResponseType.CANCEL):
			print("Cancel clicked")
		dialog.destroy()
		
	def setSimulationSettings(self):
		rule=self.getRuleValue()
		steps=self.getStepsValue()
		cells=self.getLengthValue()
		eca=ECA(rule, cells)
		
		if self.switchRandValue:
			dens=self.getDensValue()
			eca.setRandInitConf(dens)
		else:
			seed=self.getSeedValue()
			eca.setInitConf(seed, self.switchConfValue)

		sim=Simulation(steps, eca)
		print(rule)
		print(steps)
		print(cells)

		return sim

	def runSimulation(self, button):
		print("Simulation")
		sim=self.setSimulationSettings()
		sim.run()
		fileMan.openImage("Simulation.png")

	def setAnalysisSettings(self, sim=Simulation()):
		defectPos=self.getDfctPos()
		strLength=self.getStrLength()
		print(defectPos)
		print(strLength)
		self.phenA=PhenAnalyzer(defectPos, strLength)
		self.phenA.setSimulation(sim)
		
	def runAnalysis(self, button):
		print("Analysis")
		sim=self.setSimulationSettings()
		self.setAnalysisSettings(sim)
		self.phenA.runAnalysis() 
		fileMan.openImage("DamageSimulation.png")
		fileMan.openImage("DamageCone.png")
		fileMan.openImage("Density.png")
		fileMan.openImage("LyapunovExp.png")
		fileMan.openImage("Entropy.png")
"""
	#0101101110010010001
	#8191 max