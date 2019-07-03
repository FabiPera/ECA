import gi, FileManager as fileMan
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gio, GdkPixbuf
from ECA import ECA
#from PhenAnalyzer import PhenAnalyzer

class MainWindow(Gtk.ApplicationWindow):

	mainGrid = Gtk.Grid()
	tab1Grid = Gtk.Grid()
	tab2Grid = Gtk.Grid()
	adjRule = Gtk.Adjustment.new(0, 0, 256, 1, 1, 1)
	adjDens = Gtk.Adjustment.new(50, 0, 100, 1, 1, 1)
	adjWidth = Gtk.Adjustment.new(8, 8, 8192, 8, 1, 1)
	adjHeigth = Gtk.Adjustment.new(8, 8, 8192, 8, 1, 1)
	adjDfctPos = Gtk.Adjustment.new(4, 0, 8, 1, 1, 1)
	adjStrLenght = Gtk.Adjustment.new(8, 0, 1024, 8, 1, 1)
	switchRandConf = Gtk.Switch.new()
	switchStr = Gtk.Switch.new()
	scaleRule = Gtk.Scale.new(0, adjRule)
	scaleDens = Gtk.Scale.new(0, adjDens)
	entrySeed = Gtk.Entry.new()
	entrySteps = Gtk.SpinButton.new(adjHeigth, 8, 0)
	entryCells = Gtk.SpinButton.new(adjWidth, 8, 0)
	entryDefect = Gtk.Entry.new()
	scaleDfectPos = Gtk.Scale.new(0, adjDfctPos)
	entryStrLength = Gtk.SpinButton.new(adjStrLenght, 8, 0)
	ruleImage = Gtk.Image.new_from_file("../img/rule0.png")
	lyapunovImageLayout = Gtk.Box(orientation=0, spacing=50)
	ruleImageLayout = Gtk.Box(orientation=0, spacing=50)
	switchRandValue = 0
	switchConfValue = 0
	#phenA = PhenAnalyzer()
	
	def __init__(self, app):
		super(MainWindow, self).__init__(title="φ", application=app)
		self.set_default_size(500, 250)
		self.set_resizable(False)
		self.createHeaderBar()
		self.createToolBar()
		self.createTabView()
		self.add(self.mainGrid)

	def createHeaderBar(self):
		header = Gtk.HeaderBar.new()
		header.set_show_close_button(True)
		header.props.title="φ( )"

		settingsButton = Gtk.Button()
		settingsIcon = Gio.ThemedIcon(name="help-about")
		settings = Gtk.Image.new_from_gicon(settingsIcon, Gtk.IconSize.BUTTON)
		settingsButton.add(settings)

		aboutButton = Gtk.Button()
		aboutIcon = Gio.ThemedIcon(name="applications-graphics")
		about = Gtk.Image.new_from_gicon(aboutIcon, Gtk.IconSize.BUTTON)
		aboutButton.add(about)

		scienceButton = Gtk.Button()
		scienceIcon = Gio.ThemedIcon(name="applications-science")
		science = Gtk.Image.new_from_gicon(scienceIcon, Gtk.IconSize.BUTTON)
		scienceButton.add(science)

		header.pack_start(settingsButton)
		header.pack_start(aboutButton)
		header.pack_start(scienceButton)
		self.set_titlebar(header)

	def createToolBar(self):
		toolbar = Gtk.Toolbar()
		toolbar.set_style(Gtk.ToolbarStyle(2))

		imgLoad = Gtk.Image.new_from_icon_name("document-open", 0)
		imgSave = Gtk.Image.new_from_icon_name("media-floppy", 0)
		imgRun = Gtk.Image.new_from_icon_name("media-playback-start", 0)
		imgAnalysis = Gtk.Image.new_from_icon_name("edit-find", 0)

		load = Gtk.ToolButton.new(imgLoad, "Load settings")
		save = Gtk.ToolButton.new(imgSave, "Save settings")
		run = Gtk.ToolButton.new(imgRun, "Run simulation")
		analysis = Gtk.ToolButton.new(imgAnalysis, "Run Analysis")

		toolbar.insert(run, -1)
		toolbar.insert(load, -1)
		toolbar.insert(save, -1)
		toolbar.insert(analysis, -1)

		#run.connect("clicked", self.runSimulation)
		#analysis.connect("clicked", self.runAnalysis)		
		save.connect("clicked", self.saveSettings)

		self.mainGrid.attach(toolbar, 0, 0, 6, 1)

	def createTab1(self):
		tabLayout = Gtk.Box(orientation=1, spacing=30)
		tabLayout.set_border_width(20)

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
		self.scaleRule.set_digits(0)
		self.scaleDfectPos.set_digits(0)
		self.scaleDens.set_digits(0)
		self.scaleDens.set_sensitive(False)
		self.entrySeed.set_width_chars(20)
		self.entrySteps.set_width_chars(5)
		self.entryCells.set_width_chars(5)
		self.tab1Grid.set_row_spacing(10)
		self.tab1Grid.set_column_spacing(25)
		self.tab1Grid.set_column_homogeneous(False)
		self.tab2Grid.set_row_spacing(10)
		self.tab2Grid.set_column_spacing(25)
		self.tab2Grid.set_column_homogeneous(False)

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
		tabLayout.pack_start(self.tab1Grid, 1, 0, 0)

		self.switchRandConf.connect("notify::active", self.switchRandActivate)
		self.switchStr.connect("notify::active", self.switchConfActivate)
		self.adjWidth.connect("value_changed", self.changeStepWidth)
		self.adjHeigth.connect("value_changed", self.changeStepHeigth)
		self.scaleRule.connect("value_changed", self.changeRuleImg)
		self.adjStrLenght.connect("value_changed", self.changeStrLenght)

		return tabLayout

	def createTab2(self):
		tabLayout = Gtk.Box(orientation=1, spacing=30)
		tabLayout.set_border_width(20)

		labelDefect = Gtk.Label.new("Defect position: ")
		labelStrLength = Gtk.Label.new("String length: ")
		labelLyap = Gtk.Label.new("Damage spreading preview: ")
		
		self.entryDefect.set_width_chars(5)
		self.entryStrLength.set_width_chars(5)
		self.set_border_width(20)
		self.tab2Grid.set_row_spacing(10)
		self.tab2Grid.set_column_spacing(25)
		self.tab2Grid.set_column_homogeneous(False)

		self.tab2Grid.attach(labelDefect, 0, 0, 1, 1)
		self.tab2Grid.attach(self.scaleDfectPos, 1, 0, 2, 1)
		self.tab2Grid.attach(labelStrLength, 0, 2, 1, 1)
		self.tab2Grid.attach(self.entryStrLength, 1, 2, 2, 1)
		self.tab2Grid.attach(labelLyap, 3, 0, 3, 1)
		tabLayout.pack_start(self.tab2Grid, 1, 0, 0)

		return tabLayout
	
	def createTabView(self):
		tabView = Gtk.Notebook.new()
		tabView.set_border_width(10)

		tab1Layout = self.createTab1()
		tab2Layout = self.createTab2()

		tabLabel1 = Gtk.Label.new("Simulation Settings")
		tabLabel2 = Gtk.Label.new("Analysis")
		tabLabel3 = Gtk.Label.new("Settings")


		tabView.append_page(tab1Layout, tabLabel1)
		tabView.append_page(tab2Layout, tabLabel2)
		self.mainGrid.attach(tabView, 0, 1, 6, 1)

	"""
	def getIntValue(self, entry):
		value = entry.get_text()
		return int(value)

	def getStringValue(self, entry):
		value = entry.get_text()
		return str(value)
	"""

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
		val=self.adjWidth.get_value()
		self.adjDfctPos.set_upper(val)
		self.adjDfctPos.set_value((val // 2) - 1)
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

	def changeStrLenght(self, widget):
		val=self.adjStrLenght.get_value()
		if(val):
			self.adjStrLenght.set_step_increment(val)
		else:
			self.adjStrLenght.set_step_increment(8)

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

	def getDfctPos(self):
		pos = int(self.scaleDfectPos.get_value())
		return pos

	def getStrLength(self):
		length = int(self.entryStrLength.get_text())
		return length

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
		dialog=Gtk.FileChooserDialog("Load settings", None, Gtk.FileChooserAction.OPEN, (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OPEN, Gtk.ResponseType.OK))
		response=dialog.run()
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
	"""
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
	"""
	"""
	def setAnalysisSettings(self, sim=Simulation()):
		defectPos=self.getDfctPos()
		strLength=self.getStrLength()
		print(defectPos)
		print(strLength)
		self.phenA=PhenAnalyzer(defectPos, strLength)
		self.phenA.setSimulation(sim)
	"""
	"""	
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