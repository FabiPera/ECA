import gi, sys, subprocess, os
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gio, Gdk
from FiGUI import *
from Simulation import *
from Analysis import *

class FiApp(Gtk.Application):

	cellSize = 1
	dColor = Gdk.RGBA(1, 0, 0, 1)
	s1Color = Gdk.RGBA(0, 0, 0, 1)
	s0Color = Gdk.RGBA(1, 1, 1, 1)
	bColor = Gdk.RGBA(0.62, 0.62, 0.62, 1)
	switchRandValue = 0
	switchConfValue = 0
	switchAnalysisValue = 0
	analysisOp = [1, 0, 0]
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
		self.mainWindow.tab1.scaleDens.connect("value_changed", self.onDensChange)
		self.mainWindow.tab2.adjStrLenght.connect("value_changed", self.onStrLenChange)
		self.mainWindow.tab2.switchSrc.connect("notify::active", self.onAnalysisSwitch)
		self.mainWindow.tab2.scaleDfectPos.connect("value_changed", self.onDfctChange)
		self.mainWindow.tab2.densCheck.connect("notify::active", self.onDensCheck)
		self.mainWindow.tab2.entrCheck.connect("notify::active", self.onEntrCheck)
		self.mainWindow.tab2.lyapCheck.connect("notify::active", self.onLyapCheck)
		self.mainWindow.tab3.comboCellSize.connect("changed", self.onCellSizeChange)
		self.mainWindow.tab3.s1Color.connect("color-set", self.onColor1Change)
		self.mainWindow.tab3.s0Color.connect("color-set", self.onColor2Change)
		self.mainWindow.tab3.bColor.connect("color-set", self.onColor3Change)
		self.mainWindow.tab3.dColor.connect("color-set", self.onColor4Change)

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
			self.mainWindow.tab2.densCheck.set_active(True)
			self.mainWindow.tab2.entrCheck.set_active(True)
			self.mainWindow.tab2.lyapCheck.set_active(True)
			self.mainWindow.tab2.scaleDfectPos.set_sensitive(False)
			self.mainWindow.tab2.densCheck.set_sensitive(False)
			self.mainWindow.tab2.entrCheck.set_sensitive(False)
			self.mainWindow.tab2.lyapCheck.set_sensitive(False)
		else:
			self.switchAnalysisValue = 0
			label.set_text("Simulation Analysis: ")
			self.mainWindow.tab2.densCheck.set_active(False)
			self.mainWindow.tab2.entrCheck.set_active(False)
			self.mainWindow.tab2.lyapCheck.set_active(False)
			self.mainWindow.tab2.scaleDfectPos.set_sensitive(True)
			self.mainWindow.tab2.densCheck.set_sensitive(True)
			self.mainWindow.tab2.entrCheck.set_sensitive(True)
			self.mainWindow.tab2.lyapCheck.set_sensitive(True)

		print(self.analysisOp)
	
	def onDfctChange(self, widget):
		val = self.mainWindow.tab2.getDfctPos()
		self.dfctPos0 = int(val)

	def onDensCheck(self, check, active):
		if(check.get_active()):
			self.analysisOp[0] = 1
		else:
			self.analysisOp[0] = 0

	def onEntrCheck(self, check, active):
		if(check.get_active()):
			self.analysisOp[1] = 1
		else:
			self.analysisOp[1] = 0

	def onLyapCheck(self, check, active):
		if(check.get_active()):
			self.analysisOp[2] = 1
		else:
			self.analysisOp[2] = 0
	
	def onRuleChange(self, widget):
		label = self.mainWindow.tab1.labelRuleIcon
		val = self.mainWindow.tab1.getRuleValue()
		self.rule = val
		label.set_text("Rule "+str(val)+" icon")
		self.mainWindow.tab1.ruleImage.set_from_file("../img/rule"+str(val)+".png")

	def onDensChange(self, widget):
		val = self.mainWindow.tab1.getDensValue()
		self.density = int(val)

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

	def onCellSizeChange(self, combo):
		self.cellSize = self.mainWindow.tab3.getSize()
		print(self.cellSize)

	def onColor1Change(self, widget):
		color = widget.get_rgba()
		self.s1Color = Gdk.RGBA(color.red, color.green, color.blue, 1)

	def onColor2Change(self, widget):
		color = widget.get_rgba()
		self.s0Color = Gdk.RGBA(color.red, color.green, color.blue, 1)

	def onColor3Change(self, widget):
		color = widget.get_rgba()
		self.bColor = Gdk.RGBA(color.red, color.green, color.blue, 1)

	def onColor4Change(self, widget):
		color = widget.get_rgba()
		self.dColor = Gdk.RGBA(color.red, color.green, color.blue, 1)

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

		print("Rule: " + str(self.rule))
		print("Seed: " + self.seed)
		print("Steps: " + str(self.steps))
		print("Length: " + str(self.length))
		print("Density: " + str(self.density))
		print("Defect Position: " + str(self.dfctPos))
		print("String length: " + str(self.strLen))
		print("Cell size: " + str(self.cellSize))

		sim = Simulation(self.steps, self.cellSize, self.s0Color, self.s1Color, self.bColor, self.dColor, eca)
		for i in range(self.steps):
			sim.stepForward(i)
		
		sim.saveToPNG("../sim/", "simulation.png")

	def runAnalysis(self, button):
		print("Runing analysis...")
		self.seed = self.mainWindow.tab1.getSeedValue()
		if(self.switchAnalysisValue):
			print("Rule analysis")
			eca = ECA(self.rule, 10001)
			eca.setRandConf(50)
			analysis = Analysis(5000, 16, eca, self.analysisOp)
			sim1 = Simulation(5000, 1, self.s0Color, self.s1Color, self.bColor, self.dColor, eca)
			sim2 = Simulation(5000, 1, self.s0Color, self.s1Color, self.bColor, self.dColor, eca)
			sim2.eca.x = analysis.setDefect()
			sim2.xn = copy.deepcopy(sim2.eca.x)
			analysis.ruleAnalysis()
		else:
			print("Simulation analysis")
			eca = ECA(self.rule, self.length)
			if(self.switchRandValue):
				eca.setRandConf(self.density)
			else:
				eca.setConf(self.seed, self.switchConfValue)
			
			analysis = Analysis(self.dfctPos, self.strLen, eca, self.analysisOp)
			sim1 = Simulation(self.steps, self.cellSize, self.s0Color, self.s1Color, self.bColor, self.dColor, eca)
			sim2 = Simulation(self.steps, self.cellSize, self.s0Color, self.s1Color, self.bColor, self.dColor, eca)
			sim2.eca.x = analysis.setDefect()
			sim2.xn = copy.deepcopy(sim2.eca.x)
			analysis.simAnalysis(sim1, sim2)

		print("Rule: " + str(self.rule))
		print("Seed: " + self.seed)
		print("Steps: " + str(self.steps))
		print("Length: " + str(self.length))
		print("Density: " + str(self.density))
		print("Defect Position: " + str(self.dfctPos))
		print("String length: " + str(self.strLen))
		print("Cell size: " + str(self.cellSize))
	
	def saveSettings(self, button):
		print("Saving setings...")

app=FiApp()
app.run(sys.argv)
