import gi, sys, subprocess, os
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gio, Gdk
from FiGUI import *
from Simulation import *
from Analysis import *

class FiApp(Gtk.Application):

	cellSize = 1
	cell1 = Gdk.RGBA(0, 0, 0, 1)
	cell0 = Gdk.RGBA(1, 1, 1, 1)
	bckg = Gdk.RGBA(0.62, 0.62, 0.62, 1)
	dfct = Gdk.RGBA(1, 0, 0, 1)
	switchRandValue = 0
	switchConfValue = 0
	switchAnalysisValue = 0
	rule = 0
	seed = ""
	steps = 8
	length = 8
	density = 0
	dfctPos = 4
	strLen = 8
	
	def __init__(self):
		super(FiApp, self).__init__()
	
	def do_activate(self):
		self.mainWindow = MainWindow(self)
		
		self.mainWindow.tab1.switchRandConf.connect("notify::active", self.onRandConfSwitch)
		self.mainWindow.tab1.switchStr.connect("notify::active", self.onFillSwitch)
		self.mainWindow.tab1.adjWidth.connect("value_changed", self.onWidthChange)
		self.mainWindow.tab1.adjHeight.connect("value_changed", self.onHeightChange)
		self.mainWindow.tab1.scaleRule.connect("value_changed", self.onRuleChange)
		self.mainWindow.tab2.adjStrLenght.connect("value_changed", self.onStrLenChange)
		self.mainWindow.tab2.switchSrc.connect("notify::active", self.onAnalysisSwitch)
		self.mainWindow.tab3.state1Color.connect("color-set", self.onColor1Change)
		self.mainWindow.tab3.state0Color.connect("color-set", self.onColor2Change)
		self.mainWindow.tab3.bckgColor.connect("color-set", self.onColor3Change)
		self.mainWindow.tab3.dfctColor.connect("color-set", self.onColor4Change)

		run = self.mainWindow.toolbar.get_nth_item(0)
		analysis = self.mainWindow.toolbar.get_nth_item(1)
		save = self.mainWindow.toolbar.get_nth_item(2)

		run.connect("clicked", self.runSimulation)
		analysis.connect("clicked", self.runAnalysis)		
		save.connect("clicked", self.saveSettings)
		
		self.mainWindow.show_all()

	def do_startup(self):
		Gtk.Application.do_startup(self)

	def onRandConfSwitch(self, switchRandConf, active):
		if(switchRandConf.get_active()):
			self.mainWindow.tab1.entrySeed.set_sensitive(False)
			self.mainWindow.tab1.switchStr.set_sensitive(False)
			self.mainWindow.tab1.scaleDens.set_sensitive(True)
			self.density = 50
			self.switchRandValue = 1
		else:
			self.mainWindow.tab1.entrySeed.set_sensitive(True)
			self.mainWindow.tab1.switchStr.set_sensitive(True)
			self.mainWindow.tab1.scaleDens.set_sensitive(False)
			self.density = 0
			self.switchRandValue = 0
		
	def onFillSwitch(self, switchStr, active):
		label = self.mainWindow.tab1.labelFill
		if(switchStr.get_active()):
			self.switchConfValue = 1
			label.set_text("Fill w/1: ")
		else:
			self.switchConfValue = 0
			label.set_text("Fill w/0: ")

	def onAnalysisSwitch(self, switchAnalysis, active):
		label = self.mainWindow.tab2.labelSrc
		if(switchAnalysis.get_active()):
			self.switchAnalysisValue = 1
			label.set_text("Rule Analysis: ")
			self.mainWindow.tab2.scaleDfectPos.set_sensitive(False)
		else:
			self.switchAnalysisValue = 0
			label.set_text("Simulation Analysis: ")
			self.mainWindow.tab2.scaleDfectPos.set_sensitive(True)
	
	def onRuleChange(self, widget):
		label = self.mainWindow.tab1.labelRuleIcon
		val = self.mainWindow.tab1.getRuleValue()
		self.rule = val
		label.set_text("Rule "+str(val)+" icon")
		self.mainWindow.tab1.ruleImage.set_from_file("../img/rule"+str(val)+".png")

	def onWidthChange(self, widget):
		val = self.mainWindow.tab1.adjWidth.get_value()
		self.mainWindow.tab2.adjDfctPos.set_upper(val)
		self.mainWindow.tab2.adjDfctPos.set_value((val // 2) - 1)
		self.length = int(val)
		self.dfctPos = int((val // 2) - 1)
		if(val):
			self.mainWindow.tab1.adjWidth.set_step_increment(val)
		else:
			self.mainWindow.tab1.adjWidth.set_step_increment(8)

	def onHeightChange(self, widget):
		val = self.mainWindow.tab1.adjHeight.get_value()
		self.steps = int(val)
		if(val):
			self.mainWindow.tab1.adjHeight.set_step_increment(val)
		else:
			self.mainWindow.tab1.adjHeight.set_step_increment(8)

	def onStrLenChange(self, widget):
		val = self.mainWindow.tab2.adjStrLenght.get_value()
		self.strLen = int(val)
		if(val):
			self.mainWindow.tab2.adjStrLenght.set_step_increment(val)
		else:
			self.mainWindow.tab2.adjStrLenght.set_step_increment(8)

	def onColor1Change(self, widget):
		self.cell1.red = widget.get_rgba().red
		self.cell1.blue = widget.get_rgba().blue
		self.cell1.green = widget.get_rgba().green

	def onColor2Change(self, widget):
		self.cell0.red = widget.get_rgba().red
		self.cell0.blue = widget.get_rgba().blue
		self.cell0.green = widget.get_rgba().green

	def onColor3Change(self, widget):
		self.bckg.red = widget.get_rgba().red
		self.bckg.blue = widget.get_rgba().blue
		self.bckg.green = widget.get_rgba().green

	def onColor4Change(self, widget):
		self.dfct.red = widget.get_rgba().red
		self.dfct.blue = widget.get_rgba().blue
		self.dfct.green = widget.get_rgba().green

	def openFile(self, filePath="../img/", fileName="simulation.png"):
		path = filePath + fileName
		if sys.platform.startswith("darwin"):
			subprocess.call(("open", path))
		elif os.name == "nt":
			os.startfile(path)
		elif os.name == "posix":
			subprocess.call(("xdg-open", path))

	def runSimulation(self, button):
		print("Runing simulation...")
		self.seed = self.mainWindow.tab1.getSeedValue()
		eca = ECA(self.rule, self.length)
		if(self.switchRandValue):
			eca.setRandConf(self.density)
		else:
			eca.setConf(self.seed, self.switchConfValue)
			print("Initial configuration")
		
		if(self.switchConfValue):
			print("Fill with 1")
		else:
			print("Fill with 0")

		print("Rule: " + str(self.rule))
		print("Seed: " + self.seed)
		print("Steps: " + str(self.steps))
		print("Length: " + str(self.length))
		print("Density: " + str(self.density))

		sim = Simulation(eca, self.steps)
		sim.setState0Color(self.cell0)
		sim.setState1Color(self.cell1)
		sim.setBckgColor(self.bckg)
		sim.run()
		sim.saveToPNG()
		self.openFile()

	def runAnalysis(self, button):
		self.seed = self.mainWindow.tab1.getSeedValue()
		if(self.switchAnalysisValue):
			print("Running rule analysis...")
			eca = ECA(self.rule)
			eca.setRandConf(50)
			analysis = Analysis(self.dfctPos, self.strLen, eca)
		else:
			print("Running simulation analysis...")
			print("Rule: " + str(self.rule))
			print("Seed: " + self.seed)
			print("Steps: " + str(self.steps))
			print("Length: " + str(self.length))
			print("Defect Position: " + str(self.dfctPos))
			print("String length: " + str(self.strLen))
			eca = ECA(self.rule, self.length)
			eca.setConf(self.seed, self.switchConfValue)
			sim = Simulation(eca, self.steps)
			analysis = Analysis(self.dfctPos, self.strLen, sim)
			analysis.simAnalysis()
	
	def saveSettings(self, button):
		print("Saving setings...")

app=FiApp()
app.run(sys.argv)
