import gi, FileManager as fileMan, copy
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gio
from ECA import ECA
from Simulation import Simulation
from SimScreen import SimScreen

class SimModule(Gtk.Box):

	grid=Gtk.Grid()
	adjRule=Gtk.Adjustment.new(0, 0, 256, 1, 1, 1)
	adjDens=Gtk.Adjustment.new(50, 0, 100, 1, 1, 1)
	adjWidth=Gtk.Adjustment.new(8, 8, 8192, 8, 1, 1)
	adjHeigth=Gtk.Adjustment.new(8, 8, 8192, 8, 1, 1)
	switchRandConf=Gtk.Switch.new()
	switchStr=Gtk.Switch.new()
	scaleRule=Gtk.Scale.new(0, adjRule)
	scaleDens=Gtk.Scale.new(0, adjDens)
	entrySeed=Gtk.Entry.new()
	entrySteps=Gtk.SpinButton.new(adjHeigth, 8, 0)
	entryCells=Gtk.SpinButton.new(adjWidth, 8, 0)
	image=Gtk.Image.new_from_file("./Rules/rule0.png")
	imageLayout=Gtk.Box(orientation=0, spacing=50)
	switchRandValue=0
	switchConfValue=0

	def __init__(self):
		super(SimModule, self).__init__(orientation=1, spacing=30)
		self.grid.set_hexpand(0)
		self.createToolBar()
		self.createTab()
		self.pack_start(self.grid, 1, 0, 0)

	def createToolBar(self):
		toolbar=Gtk.Toolbar()
		
		toolbar.set_style(Gtk.ToolbarStyle(2))
		imgLoad=Gtk.Image.new_from_icon_name("document-open", 0)
		imgSave=Gtk.Image.new_from_icon_name("media-floppy", 0)
		imgRun=Gtk.Image.new_from_icon_name("media-playback-start", 0)

		load=Gtk.ToolButton.new(imgLoad, "Load settings")
		save=Gtk.ToolButton.new(imgSave, "Save settings")
		run=Gtk.ToolButton.new(imgRun, "Run simulation")

		toolbar.insert(run, -1)
		toolbar.insert(load, -1)
		toolbar.insert(save, -1)

		run.connect("clicked", self.runSimulation)

		self.grid.attach(toolbar, 0, 0, 5, 1)

	def createTab(self):
		labelRule=Gtk.Label.new("Rule: ")
		labelRandConf=Gtk.Label.new("Random conf: ")
		labelConf=Gtk.Label.new("Seed: ")
		labelFill=Gtk.Label.new("Fill with 0's:")
		labelSteps=Gtk.Label.new("Steps: ")
		labelCells=Gtk.Label.new("Length: ")
		labelDens=Gtk.Label.new("Density (%): ")
		labelRuleIcon=Gtk.Label.new("Rule 0 icon")

		self.switchStr.set_active(False)
		self.switchRandConf.set_active(False)
		self.scaleRule.set_digits(0)
		self.scaleDens.set_sensitive(False)
		self.entrySeed.set_width_chars(20)
		self.entrySteps.set_width_chars(5)
		self.entryCells.set_width_chars(5)
		self.set_border_width(20)
		self.grid.set_row_spacing(10)
		self.grid.set_column_spacing(25)
		self.grid.set_column_homogeneous(False)

		layoutRandSwitch=Gtk.Box(orientation=0, spacing=50)
		layoutFillSwitch=Gtk.Box(orientation=0, spacing=50)
		layoutRandSwitch.pack_start(self.switchRandConf, 0, 0, 50)
		layoutFillSwitch.pack_start(self.switchStr, 0, 0, 50)

		self.grid.attach(labelRandConf, 0, 1, 1, 1)
		self.grid.attach(layoutRandSwitch, 1, 1, 1, 1)
		self.grid.attach(labelRuleIcon, 3, 1, 2, 1)
		self.grid.attach(labelFill, 0, 2, 1, 1)
		self.grid.attach(layoutFillSwitch, 1, 2, 1, 1)
		self.grid.attach(labelRule, 0, 3, 1, 1)
		self.grid.attach(self.scaleRule, 1, 3, 1, 1)
		self.grid.attach(labelConf, 0, 4, 1, 1)
		self.grid.attach(self.entrySeed, 1, 4, 1, 1)
		self.grid.attach(labelSteps, 0, 5, 1, 1)
		self.grid.attach(self.entrySteps, 1, 5, 1, 1)
		self.grid.attach(labelCells, 0, 6, 1, 1)
		self.grid.attach(self.entryCells, 1, 6, 1, 1)
		self.grid.attach(labelDens, 0, 7, 1, 1)
		self.grid.attach(self.scaleDens, 1, 7, 1, 1)
		self.grid.attach(self.imageLayout, 3, 2, 2, 5)
		self.imageLayout.pack_start(self.image, 1, 0, 0)

		self.switchRandConf.connect("notify::active", self.switchRandActivate)
		self.switchStr.connect("notify::active", self.switchConfActivate)
		self.adjWidth.connect("value_changed", self.changeStepWidth)
		self.adjHeigth.connect("value_changed", self.changeStepHeigth)
		self.scaleRule.connect("value_changed", self.changeRuleImg)

	def runSimulation(self, button):
		print("Simulation")
		sim=self.setSimulationSettings()
		sim.run()
		fileMan.openImage("Simulation.png")

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

	def getIntValue(self, entry):
		value=entry.get_text()
		return int(value)

	def getStringValue(self, entry):
		value=entry.get_text()
		return str(value)

	def switchRandActivate(self, switchRandConf, active):
		if(switchRandConf.get_active()):
			self.entrySeed.set_sensitive(False)
			self.switchStr.set_sensitive(False)
			self.scaleDens.set_sensitive(True)
			self.switchRandValue=1
		else:
			self.entrySeed.set_sensitive(True)
			self.switchStr.set_sensitive(True)
			self.scaleDens.set_sensitive(False)
			self.switchRandValue=0
		
	def switchConfActivate(self, switchStr, active):
		label=self.grid.get_child_at(0, 2)
		if(switchStr.get_active()):
			self.switchConfValue=1
			label.set_text("Fill with 1's")
		else:
			self.switchConfValue=0
			label.set_text("Fill with 0's")

	def changeRuleImg(self, widget):
		val=int(self.scaleRule.get_value())
		label=self.grid.get_child_at(3, 1)
		label.set_text("Rule "+str(val)+" icon")
		self.image.set_from_file("./Rules/rule"+str(val)+".png")

	def changeStepWidth(self, widget):
		val=self.adjWidth.get_value()
		if(val):
			self.adjWidth.set_step_increment(val)
		else:
			self.adjWidth.set_step_increment(8)

	def changeStepHeigth(self, widget):
		val=self.adjHeigth.get_value()
		if(val):
			self.adjHeigth.set_step_increment(val)
		else:
			self.adjHeigth.set_step_increment(8)

	def getSwitchRandValue(self):
		return self.switchRandValue

	def getSwitchConfValue(self):
		return self.switchConfValue

	def getRuleValue(self):
		rule=int(self.scaleRule.get_value())
		return rule

	def getSeedValue(self):
		seed=str(self.entrySeed.get_text())
		return seed
		
	def getStepsValue(self):
		steps=int(self.entrySteps.get_value())
		return steps
	
	def getLengthValue(self):
		length=int(self.entryCells.get_value())
		return length

	def getDensValue(self):
		dens=int(self.scaleDens.get_value())
		return dens