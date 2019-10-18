import gi, sys, subprocess, os, math, copy, re, Files
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gio, Gdk
from Analysis import Analysis
from Simulation import ECA, Simulation
from FiGUI import MainWindow, SimulationTab, AnalysisTab, SettingsTab

class FiApp(Gtk.Application):

	cellSize = 1
	dColor = Gdk.RGBA(1, 0, 0, 1)
	s1Color = Gdk.RGBA(0, 0, 0, 1)
	s0Color = Gdk.RGBA(1, 1, 1, 1)
	bColor = Gdk.RGBA(0.62, 0.62, 0.62, 1)
	simPath = "../img/simulation/"
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
		self.mainWindow.tab3.folderButton.connect("clicked", self.selectFolder)

		run = self.mainWindow.toolbar.get_nth_item(0)
		analysis = self.mainWindow.toolbar.get_nth_item(1)
		save = self.mainWindow.toolbar.get_nth_item(2)
		load = self.mainWindow.toolbar.get_nth_item(3)

		run.connect("clicked", self.runSimulation)
		analysis.connect("clicked", self.runAnalysis)		
		save.connect("clicked", self.saveSettings)
		load.connect("clicked", self.loadSettings)
		
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
	
	def onRuleChange(self, widget):
		label = self.mainWindow.tab1.labelRuleIcon
		val = self.mainWindow.tab1.getRuleValue()
		self.rule = val
		label.set_text("Rule "+str(val)+" icon")
		self.mainWindow.tab1.ruleImage.set_from_file("../img/rules/rule"+str(val)+".png")

	def onDensChange(self, widget):
		val = self.mainWindow.tab1.getDensValue()
		self.density = int(val)

	def onWidthChange(self, widget):
		val = self.mainWindow.tab1.adjWidth.get_value()
		self.mainWindow.tab2.adjDfctPos.set_upper(val)
		self.mainWindow.tab2.adjDfctPos.set_value((val // 2) - 1)
		self.length = int(val)
		self.strLen = int(math.log(self.length, 2) - 1)
		self.mainWindow.tab2.entryStrLength.set_value(self.strLen)
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

	def onStrLenChange(self, widget):
		val = self.mainWindow.tab2.adjStrLenght.get_value()
		self.strLen = int(val)

	def onCellSizeChange(self, combo):
		self.cellSize = self.mainWindow.tab3.getSize()
		upper = 16385 // self.cellSize
		self.mainWindow.tab1.adjHeight.set_upper(upper)
		self.mainWindow.tab1.adjWidth.set_upper(upper)

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

	def selectFolder(self, button):
		dialog = Gtk.FileChooserNative.new(title="Select folder", parent=None, action=Gtk.FileChooserAction.SELECT_FOLDER)
		response = dialog.run()

		if(response == Gtk.ResponseType.ACCEPT):
			self.mainWindow.tab3.labelFolderPath.set_text(dialog.get_filename() + "/")
			self.simPath = dialog.get_filename() + "/"
			# print("Folder selected: " + dialog.get_filename())

		elif(response == Gtk.ResponseType.CANCEL):
			print("Folder selection canceled")	
		
		dialog.destroy()

	def checkSeedEntry(self):
		self.seed = self.mainWindow.tab1.getSeedValue()
		match = re.search(r"[^01]", self.seed)
		if(self.seed == "" or match or len(self.seed) > self.length):
			return False
		else:
			return True

	def runSimulation(self, button=None):
		if(self.checkSeedEntry()):
			print("Runing simulation...")
			self.seed = self.mainWindow.tab1.getSeedValue()
			eca = ECA(self.rule, self.length)
			
			print("Rule: " + str(self.rule))
			if(self.switchRandValue):
				eca.setRandConf(self.density)
				print("Density: " + str(self.density))

			else:
				eca.setConf(self.seed, self.switchConfValue)
				print("Seed: " + self.seed)

			print("Steps: " + str(self.steps))
			print("Length: " + str(self.length))
			print("Cell size: " + str(self.cellSize))

			sim = Simulation(self.steps, self.cellSize, self.s0Color, self.s1Color, self.bColor, self.dColor, eca)
			for i in range(self.steps):
				sim.stepForward(i)
			
			sim.saveToPNG(self.simPath, "simulation.png")
		
		else:
			print("Intoduce a correct seed")


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
			print("Rule: " + str(self.rule))
			if(self.switchRandValue):
				eca.setRandConf(self.density)
				print("Density: " + str(self.density))
				analysis = Analysis(self.dfctPos, self.strLen, eca, self.analysisOp)
				sim1 = Simulation(self.steps, self.cellSize, self.s0Color, self.s1Color, self.bColor, self.dColor, eca)
				sim2 = Simulation(self.steps, self.cellSize, self.s0Color, self.s1Color, self.bColor, self.dColor, eca)
				sim2.eca.x = analysis.setDefect()
				sim2.xn = copy.deepcopy(sim2.eca.x)
				analysis.simAnalysis(sim1, sim2, self.simPath)
				print("Steps: " + str(self.steps))
				print("Length: " + str(self.length))
				print("Defect Position: " + str(self.dfctPos))
				print("String length: " + str(self.strLen))
				print("Cell size: " + str(self.cellSize))

			else:
				if(self.checkSeedEntry()):
					eca.setConf(self.seed, self.switchConfValue)
					print("Seed: " + self.seed)
					analysis = Analysis(self.dfctPos, self.strLen, eca, self.analysisOp)
					sim1 = Simulation(self.steps, self.cellSize, self.s0Color, self.s1Color, self.bColor, self.dColor, eca)
					sim2 = Simulation(self.steps, self.cellSize, self.s0Color, self.s1Color, self.bColor, self.dColor, eca)
					sim2.eca.x = analysis.setDefect()
					sim2.xn = copy.deepcopy(sim2.eca.x)
					analysis.simAnalysis(sim1, sim2, self.simPath)
					print("Steps: " + str(self.steps))
					print("Length: " + str(self.length))
					print("Defect Position: " + str(self.dfctPos))
					print("String length: " + str(self.strLen))
					print("Cell size: " + str(self.cellSize))

				else:
					print("Intoduce a correct seed")
	
	def saveSettings(self, button):
		self.seed = self.mainWindow.tab1.getSeedValue()
		dialog = Gtk.FileChooserNative.new(title="Save settings", parent=None, action=Gtk.FileChooserAction.SAVE)
		response = dialog.run()

		if(response == Gtk.ResponseType.ACCEPT):
			fill = self.switchConfValue
			rule = self.rule
			steps = self.steps
			cells = self.length
			seed = self.seed
			self.runSimulation()
			b64String = Files.imageToString("../img/simulation/simulation.png")
			data = {"fill": fill, "rule": rule, "seed": seed, "steps": steps, "cells": cells, "img": str(b64String)}
			Files.writeJSON(dialog.get_filename(), data)
			print("Settings saved")
			print("File selected: " + dialog.get_filename())

		elif(response == Gtk.ResponseType.CANCEL):
			print("Saving canceled")

		dialog.destroy()

	def loadSettings(self, button):
		dialog = Gtk.FileChooserNative.new(title="Load settings", parent=None, action=Gtk.FileChooserAction.OPEN)
		response = dialog.run()

		if(response == Gtk.ResponseType.ACCEPT):
			data = Files.loadSettings(dialog.get_filename())
			self.mainWindow.tab1.switchRandConf.set_active(False)
			self.mainWindow.tab1.switchStr.set_active(bool(data["fill"]))
			self.mainWindow.tab1.scaleRule.set_value(data["rule"])
			self.mainWindow.tab1.entrySeed.set_text(data["seed"])
			self.mainWindow.tab1.entrySteps.set_value(data["steps"])
			self.mainWindow.tab1.entryCells.set_value(data["cells"])
			Files.openFile(fileName=dialog.get_filename().split(".")[0] + ".png")
			print("Settings loaded")
			print("File selected: " + dialog.get_filename())

		elif(response == Gtk.ResponseType.CANCEL):
			print("Loading canceled")

		dialog.destroy()


app=FiApp()
app.run(sys.argv)