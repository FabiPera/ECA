import gi, sys, copy, matplotlib.pyplot as plt, numpy as np
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from gi.repository import Gio
from ECA import ECA
from Simulation import Simulation
from PhenAnalyzer import PhenAnalyzer
from SimScreen import SimScreen

class Widgets():

	mainLayout = Gtk.Box(orientation=1)
	toolbarLayout = Gtk.Box(orientation=0)
	tabViewLayout = Gtk.Box(orientation=0, spacing=30)
	tab1Layout = Gtk.Box(orientation=1, spacing=30)
	tab2Layout = Gtk.Box(orientation=1, spacing=30)
	layout11 = Gtk.Box(orientation=0)
	layout12 = Gtk.Box(orientation=0)
	layout13 = Gtk.Box(orientation=0)
	layout21 = Gtk.Box(orientation=0)
	layout22 = Gtk.Box(orientation=0)
	toolbar = Gtk.Toolbar()
	tabView = Gtk.Notebook.new()
	adjRule = Gtk.Adjustment.new(0, 0, 256, 1, 1, 1)
	entryRule = Gtk.SpinButton.new(adjRule, 1, 0)
	switchRandConf = Gtk.Switch.new()
	switchStr = Gtk.Switch.new()
	entrySeed = Gtk.Entry.new()
	entrySteps = Gtk.Entry.new()
	entryCells = Gtk.Entry.new()
	entryPer = Gtk.Entry.new()
	entryDefect = Gtk.Entry.new()
	entryStrLength = Gtk.Entry.new()
	switchRandValue = 0
	switchConfValue = 0
	simulationWindow = Gtk.Window.new(0)
	spinnerLayout = Gtk.Box(orientation=0)
	spinner = Gtk.Spinner()
	phenA=PhenAnalyzer()
	
	def __init__(self):
		self.createToolbar()
		self.createTabView()
		self.toolbarLayout.pack_start(self.toolbar, 0, 0, 0)
		self.tabViewLayout.pack_start(self.tabView, 0, 0, 0)
		self.mainLayout.pack_start(self.toolbarLayout, 0, 0, 0)
		self.mainLayout.pack_start(self.tabViewLayout, 0, 0, 0)

	def createToolbar(self):
		imgExit=Gtk.Image.new_from_icon_name("application-exit", 0)
		imgLoad=Gtk.Image.new_from_icon_name("document-open", 0)
		imgSave=Gtk.Image.new_from_icon_name("document-save-as", 0)
		imgRun=Gtk.Image.new_from_icon_name("media-playback-start", 0)
		imgAnalysis=Gtk.Image.new_from_icon_name("edit-find", 0)

		exitApp=Gtk.ToolButton.new(imgExit, "Exit")
		load=Gtk.ToolButton.new(imgLoad, "Load settings")
		save=Gtk.ToolButton.new(imgSave, "Save settings")
		run=Gtk.ToolButton.new(imgRun, "Run simulation")
		analysis=Gtk.ToolButton.new(imgAnalysis, "Run analysis")

		self.toolbar.insert(exitApp, -1)
		self.toolbar.insert(load, -1)
		self.toolbar.insert(save, -1)
		self.toolbar.insert(run, -1)
		self.toolbar.insert(analysis, -1)

		run.connect("clicked", self.runSimulation)
		analysis.connect("clicked", self.runAnalysis)

	def createTab1(self):
		labelRule=Gtk.Label.new("Rule: ")
		labelRandConf=Gtk.Label.new("Random configuration: ")
		labelConf=Gtk.Label.new("Seed: ")
		labelStr0=Gtk.Label.new("0")
		labelStr1=Gtk.Label.new("1")
		labelSteps=Gtk.Label.new("Steps: ")
		labelCells=Gtk.Label.new("Cells: ")
		labelDens=Gtk.Label.new("Density (%): ")

		self.switchStr.set_active(False)
		self.switchRandConf.set_active(False)
		self.entryPer.set_sensitive(False)
		self.entrySeed.set_width_chars(20)
		self.entrySteps.set_width_chars(5)
		self.entryCells.set_width_chars(5)
		self.entryPer.set_width_chars(5)
		
		self.layout11.set_halign(0)
		self.layout12.set_halign(0)
		self.layout11.pack_start(labelRule, 1, 0, 10)
		self.layout11.pack_start(self.entryRule, 1, 0, 10)
		self.layout11.pack_start(labelRandConf, 1, 0, 10)
		self.layout11.pack_start(self.switchRandConf, 1, 0, 10)
		self.layout12.pack_start(labelConf, 1, 0, 10)
		self.layout12.pack_start(self.entrySeed, 1, 0, 10)
		self.layout12.pack_start(labelStr0, 1, 0, 5)
		self.layout12.pack_start(self.switchStr, 1, 0, 10)
		self.layout12.pack_start(labelStr1, 1, 0, 5)
		self.layout13.pack_start(labelSteps, 1, 0, 10)
		self.layout13.pack_start(self.entrySteps, 1, 0, 10)
		self.layout13.pack_start(labelCells, 1, 0, 10)
		self.layout13.pack_start(self.entryCells, 1, 0, 10)
		self.layout13.pack_start(labelDens, 1, 0, 10)
		self.layout13.pack_start(self.entryPer, 1, 0, 10)
		self.spinnerLayout.pack_start(self.spinner, 1, 0, 0)
		self.tab1Layout.pack_start(self.layout11, 1, 0, 0)
		self.tab1Layout.pack_start(self.layout12, 1, 0, 0)
		self.tab1Layout.pack_start(self.layout13, 1, 0, 0)
		self.tab1Layout.pack_start(self.spinnerLayout, 1, 0, 0)

		self.switchRandConf.connect("notify::active", self.switchRandActivate)
		self.switchStr.connect("notify::active", self.switchConfActivate)

	def createTab2(self):
		labelDefect=Gtk.Label.new("Defect position: ")
		labelStrLength=Gtk.Label.new("String length: ")
		
		self.entryDefect.set_width_chars(5)
		self.entryStrLength.set_width_chars(5)

		self.layout21.set_halign(0)
		self.layout22.set_halign(0)
		self.layout21.pack_start(labelDefect, 1, 0, 10)
		self.layout21.pack_start(self.entryDefect, 1, 0, 10)
		self.layout22.pack_start(labelStrLength, 1, 0, 10)
		self.layout22.pack_start(self.entryStrLength, 1, 0, 10)
		self.tab2Layout.pack_start(self.layout21, 1, 0, 0)
		self.tab2Layout.pack_start(self.layout22, 1, 0, 0)
	
	def createTabView(self):
		tabLabel1=Gtk.Label.new("Simulation Settings")
		tabLabel2=Gtk.Label.new("Analysis")
		self.tabView.set_border_width(20)
		self.tab1Layout.set_border_width(20)
		self.tab2Layout.set_border_width(20)
		self.createTab1()
		self.createTab2()
		self.tabView.append_page(self.tab1Layout, tabLabel1)
		self.tabView.append_page(self.tab2Layout, tabLabel2)

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
			self.entryPer.set_sensitive(True)
			self.switchRandValue=1
		else:
			self.entrySeed.set_sensitive(True)
			self.switchStr.set_sensitive(True)
			self.entryPer.set_sensitive(False)
			self.switchRandValue=0
		
	def switchConfActivate(self, switchStr, active):
		if (switchStr.get_active()):
			self.switchConfValue=1
		else:
			self.switchConfValue=0

	def saveSettings(self):
		pass
		#Dlg=gtk.FileChooserDialog(title="Save", parent=None, action = gtk.FILE_CHOOSER_ACTION_SAVE,  buttons=None, backend=None)

	def setSimulationSettings(self):
		rule=self.entryRule.get_value_as_int()
		steps=self.getIntValue(self.entrySteps)
		cells=self.getIntValue(self.entryCells)
		eca=ECA(rule, cells)
		
		if self.switchRandValue:
			dens=self.getIntValue(self.entryPer)
			eca.denPer=dens
			eca.setRandInitConf()
		else:
			seed=self.getStringValue(self.entrySeed)
			eca.setInitConf(seed, self.switchConfValue)

		sim=Simulation(steps, eca)
		print(rule)
		print(steps)
		print(cells)

		return sim
	
	def setAnalysisSettings(self, sim=Simulation()):
		defectPos=self.getIntValue(self.entryDefect)
		strLength=self.getIntValue(self.entryStrLength)
		self.phenA=PhenAnalyzer(defectPos, strLength)
		self.phenA.setSimulation(sim)

	def runSimulation(self, button):
		print("Simulation")
		self.spinner.start()
		sim=self.setSimulationSettings()
		sim.run()
		self.spinner.stop()
		
	def runAnalysis(self, button):
		print("Analysis")
		self.spinner.start()
		sim=self.setSimulationSettings()
		self.setAnalysisSettings(sim)
		self.phenA.runAnalysis()
		self.spinner.stop()

	#0101101110010010001
	#8191 max