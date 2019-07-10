import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gio, GdkPixbuf

class MainWindow(Gtk.ApplicationWindow):
	
	mainGrid = Gtk.Grid()

	def __init__(self, app):
		super(MainWindow, self).__init__(title="φ( )", application=app)
		self.set_default_size(500, 250)
		self.set_resizable(False)

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
		
		self.mainGrid.attach(toolbar, 0, 0, 6, 1)

		tabView = Gtk.Notebook.new()
		tabView.set_border_width(10)

		self.tab1Layout = SimulatorTab()
		self.tab2Layout = AnalyzerTab()

		tabLabel1 = Gtk.Label.new("Simulation Settings")
		tabLabel2 = Gtk.Label.new("Analysis")
		tabLabel3 = Gtk.Label.new("Settings")

		tabView.append_page(self.tab1Layout, tabLabel1)
		tabView.append_page(self.tab2Layout, tabLabel2)
		self.mainGrid.attach(tabView, 0, 1, 6, 1)
		self.add(self.mainGrid)

		#run.connect("clicked", self.runSimulation)
		#analysis.connect("clicked", self.runAnalysis)		
		#save.connect("clicked", self.saveSettings)

class SimulatorTab(Gtk.Box):	

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

	def __init__(self):
		super(SimulatorTab, self).__init__(orientation=1, spacing=30)
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

class AnalyzerTab(Gtk.Box):

	tab2Grid = Gtk.Grid()
	adjDfctPos = Gtk.Adjustment.new(4, 0, 8, 1, 1, 1)
	adjStrLenght = Gtk.Adjustment.new(8, 0, 1024, 8, 1, 1)
	entryDefect = Gtk.Entry.new()
	scaleDfectPos = Gtk.Scale.new(0, adjDfctPos)
	entryStrLength = Gtk.SpinButton.new(adjStrLenght, 8, 0)

	def __init__(self):
		super(AnalyzerTab, self).__init__(orientation=1, spacing=30)
		self.set_border_width(20)

		labelDefect = Gtk.Label.new("Defect position: ")
		labelStrLength = Gtk.Label.new("String length: ")
		labelLyap = Gtk.Label.new("Damage spreading preview: ")
		
		self.entryDefect.set_width_chars(5)
		self.entryStrLength.set_width_chars(5)
		self.scaleDfectPos.set_digits(0)

		self.tab2Grid.set_row_spacing(10)
		self.tab2Grid.set_column_spacing(25)
		self.tab2Grid.set_column_homogeneous(False)

		self.tab2Grid.attach(labelDefect, 0, 0, 1, 1)
		self.tab2Grid.attach(self.scaleDfectPos, 1, 0, 2, 1)
		self.tab2Grid.attach(labelStrLength, 0, 2, 1, 1)
		self.tab2Grid.attach(self.entryStrLength, 1, 2, 2, 1)
		self.tab2Grid.attach(labelLyap, 3, 0, 3, 1)
		self.pack_start(self.tab2Grid, 1, 0, 0)

	def getDfctPos(self):
		pos = int(self.scaleDfectPos.get_value())
		return pos

	def getStrLength(self):
		length = int(self.entryStrLength.get_text())
		return length
	