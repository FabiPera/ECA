import gi, cairo
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gio, Gdk

class MainWindow(Gtk.ApplicationWindow):
	
	mainGrid = Gtk.Grid()
	header = Gtk.HeaderBar.new()
	toolbar = Gtk.Toolbar()

	def __init__(self, app):
		super(MainWindow, self).__init__(title="φ( )", application=app)
		self.set_default_size(500, 250)
		self.set_resizable(False)

		#Create the header bar and attach it to the main window
		self.header.set_show_close_button(True)
		self.header.props.title="φ( )"

		# #Create the buttons for the header bar
		# settingsButton = Gtk.Button()
		# settingsIcon = Gio.ThemedIcon(name="help-about")
		# settings = Gtk.Image.new_from_gicon(settingsIcon, Gtk.IconSize.BUTTON)
		# settingsButton.add(settings)

		# aboutButton = Gtk.Button()
		# aboutIcon = Gio.ThemedIcon(name="applications-graphics")
		# about = Gtk.Image.new_from_gicon(aboutIcon, Gtk.IconSize.BUTTON)
		# aboutButton.add(about)

		# scienceButton = Gtk.Button()
		# scienceIcon = Gio.ThemedIcon(name="applications-science")
		# science = Gtk.Image.new_from_gicon(scienceIcon, Gtk.IconSize.BUTTON)
		# scienceButton.add(science)

		# self.header.pack_start(settingsButton)
		# self.header.pack_start(aboutButton)
		# self.header.pack_start(scienceButton)
		self.set_titlebar(self.header)

		#Create the toolbar and attach it to the main window
		self.toolbar.set_style(Gtk.ToolbarStyle(2))

		#Create the buttons for the toolbar
		imgLoad = Gtk.Image.new_from_icon_name("document-open", 0)
		imgSave = Gtk.Image.new_from_icon_name("media-floppy", 0)
		imgRun = Gtk.Image.new_from_icon_name("media-playback-start", 0)
		imgAnalysis = Gtk.Image.new_from_icon_name("edit-find", 0)

		load = Gtk.ToolButton.new(imgLoad, "Load settings")
		save = Gtk.ToolButton.new(imgSave, "Save settings")
		run = Gtk.ToolButton.new(imgRun, "Run simulation")
		analysis = Gtk.ToolButton.new(imgAnalysis, "Run Analysis")

		self.toolbar.insert(run, -1)
		self.toolbar.insert(analysis, -1)
		self.toolbar.insert(save, -1)
		self.toolbar.insert(load, -1)
		
		self.mainGrid.attach(self.toolbar, 0, 0, 6, 1)

		#Create the tabview and attach it to the main window
		tabView = Gtk.Notebook.new()
		tabView.set_border_width(10)

		self.tab1 = SimulationTab()
		self.tab2 = AnalysisTab()
		self.tab3 = SettingsTab()
		tabView.child_set_property(self.tab1, "tab-fill", True)
		tabView.child_set_property(self.tab2, "tab-fill", True)
		tabView.child_set_property(self.tab3, "tab-fill", True)

		tabLabel1 = Gtk.Label.new("Simulation Settings")
		tabLabel2 = Gtk.Label.new("Analysis")
		tabLabel3 = Gtk.Label.new("Settings")

		tabView.append_page(self.tab1, tabLabel1)
		tabView.append_page(self.tab2, tabLabel2)
		tabView.append_page(self.tab3, tabLabel3)
		self.mainGrid.attach(tabView, 0, 1, 6, 1)
		self.add(self.mainGrid)

class SimulationTab(Gtk.Box):	

	#Widgets for simulation inputs
	tab1Box = Gtk.Box(orientation=0, spacing=50)
	adjRule = Gtk.Adjustment.new(0, 0, 256, 1, 1, 1)
	adjDens = Gtk.Adjustment.new(50, 0, 100, 1, 1, 1)
	adjWidth = Gtk.Adjustment.new(8, 8, 8192, 8, 1, 1)
	adjHeight = Gtk.Adjustment.new(8, 8, 8192, 8, 1, 1)
	switchRandConf = Gtk.Switch.new()
	switchStr = Gtk.Switch.new()
	scaleRule = Gtk.Scale.new(0, adjRule)
	scaleDens = Gtk.Scale.new(0, adjDens)
	entrySeed = Gtk.Entry.new()
	entrySteps = Gtk.SpinButton.new(adjHeight, 8, 0)
	entryCells = Gtk.SpinButton.new(adjWidth, 8, 0)
	ruleImage = Gtk.Image.new_from_file("../img/rules/rule0.png")
	imagebox = Gtk.Box(orientation=0, spacing=50)
	labelRandConf = Gtk.Label("Random: ", xalign=0, yalign=0)
	labelFill = Gtk.Label("Fill w/0: ", xalign=0, yalign=0)
	labelRule = Gtk.Label("Rule:", xalign=0, yalign=0)
	labelConf = Gtk.Label("Seed: ", xalign=0, yalign=0)
	labelSteps = Gtk.Label("Steps: ", xalign=0, yalign=0)
	labelCells = Gtk.Label("Length: ", xalign=0, yalign=0)
	labelDens = Gtk.Label("Density (%): ", xalign=0, yalign=0)
	labelRuleIcon = Gtk.Label("Rule 0 icon", xalign=0.5, yalign=0.5)

	def __init__(self):
		super(SimulationTab, self).__init__(orientation=1, spacing=30)
		self.set_border_width(20)

		#Disable for random simulation
		self.switchStr.set_active(False)
		self.switchRandConf.set_active(False)
		self.scaleDens.set_sensitive(False)

		#Disable decimal digits
		self.scaleRule.set_digits(0)
		self.scaleDens.set_digits(0)
		
		#Set the width in chars for the inputs
		self.entrySeed.set_width_chars(20)
		self.entrySteps.set_width_chars(5)
		self.entryCells.set_width_chars(5)
		
		self.imagebox.pack_start(self.ruleImage, 1, 0, 0)
		
		listbox = Gtk.ListBox()
		listbox.set_selection_mode(0)
		row1 = Gtk.ListBoxRow()
		vbox1 = Gtk.Box(orientation=1, spacing=10)
		vbox2 = Gtk.Box(orientation=1, spacing=10)
		vbox3 = Gtk.Box(orientation=1, spacing=10)
		hbox1 = Gtk.Box(orientation=0, spacing=25)
		switchbox1 = Gtk.Box(orientation=0)
		switchbox2 = Gtk.Box(orientation=0)
		
		switchbox1.pack_start(self.switchRandConf, 0, 0, 0)
		switchbox2.pack_start(self.switchStr, 0, 0, 0)

		hbox1.pack_start(vbox1, 1, 1, 0)
		hbox1.pack_start(vbox2, 1, 1, 0)
		hbox1.pack_start(vbox3, 1, 1, 0)
		vbox1.pack_start(self.labelRandConf, 1, 1, 0)
		vbox1.pack_start(self.labelFill, 1, 1, 0)
		vbox1.pack_start(self.labelRule, 1, 1, 0)
		vbox1.pack_start(self.labelConf, 1, 1, 0)
		vbox1.pack_start(self.labelSteps, 1, 1, 0)
		vbox1.pack_start(self.labelCells, 1, 1, 0)
		vbox1.pack_start(self.labelDens, 1, 1, 0)
		vbox2.pack_start(switchbox1, 1, 1, 0)
		vbox2.pack_start(switchbox2, 1, 1, 0)
		vbox2.pack_start(self.scaleRule, 1, 1, 0)
		vbox2.pack_start(self.entrySeed, 1, 1, 0)
		vbox2.pack_start(self.entrySteps, 1, 1, 0)
		vbox2.pack_start(self.entryCells, 1, 1, 0)
		vbox2.pack_start(self.scaleDens, 1, 1, 0)
		vbox3.pack_start(self.labelRuleIcon, 1, 1, 0)
		vbox3.pack_start(self.imagebox, 1, 1, 0)
		
		row1.add(hbox1)
		listbox.add(row1)

		self.tab1Box.pack_start(listbox, 1, 0, 0)
		self.pack_start(self.tab1Box, 1, 0, 0)

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

class AnalysisTab(Gtk.Box):

	#Widgets for analysis inputs
	tab2Box = Gtk.Box(orientation=0, spacing=30)
	adjDfctPos = Gtk.Adjustment.new(4, 0, 8, 1, 1, 1)
	adjStrLenght = Gtk.Adjustment.new(3, 3, 16, 1, 1, 1)
	scaleDfectPos = Gtk.Scale.new(0, adjDfctPos)
	entryStrLength = Gtk.SpinButton.new(adjStrLenght, 8, 0)
	lyapCheck = Gtk.CheckButton.new()
	densCheck = Gtk.CheckButton.new()
	entrCheck = Gtk.CheckButton.new()
	switchSrc = Gtk.Switch.new()
	labelDefect = Gtk.Label("Defect position: ", xalign=0)
	labelStrLength = Gtk.Label("String length: ", xalign=0)
	labelSrc = Gtk.Label("Simulation Analysis: ", xalign=0)
	labelDens = Gtk.Label("Density: ", xalign=0)
	labelEntr = Gtk.Label("Entropy : ", xalign=0)
	labelLyap = Gtk.Label("Lyapunov Exp.: ", xalign=0)

	def __init__(self):
		super(AnalysisTab, self).__init__(orientation=1, spacing=30)
		self.set_border_width(20)
		
		#Set the width in chars for the inputs
		self.entryStrLength.set_width_chars(5)
		self.scaleDfectPos.set_digits(0)
		self.densCheck.set_active(True)

		listbox = Gtk.ListBox()
		listbox.set_selection_mode(0)
		row1 = Gtk.ListBoxRow()
		vbox1 = Gtk.Box(orientation=1, spacing=10)
		vbox2 = Gtk.Box(orientation=1, spacing=10)
		hbox1 = Gtk.Box(orientation=0, spacing=50)
		switchbox1 = Gtk.Box(orientation=0)

		switchbox1.pack_start(self.switchSrc, 0, 0, 0)
		
		hbox1.pack_start(vbox1, 1, 1, 0)
		hbox1.pack_start(vbox2, 1, 1, 0)
		vbox1.pack_start(self.labelSrc, 1, 1, 0)
		vbox1.pack_start(self.labelDens, 1, 1, 0)
		vbox1.pack_start(self.labelEntr, 1, 1, 0)
		vbox1.pack_start(self.labelLyap, 1, 1, 0)
		vbox1.pack_start(self.labelDefect, 1, 1, 0)
		vbox1.pack_start(self.labelStrLength, 1, 1, 0)
		vbox2.pack_start(switchbox1, 1, 1, 0)
		vbox2.pack_start(self.densCheck, 1, 1, 0)
		vbox2.pack_start(self.entrCheck, 1, 1, 0)
		vbox2.pack_start(self.lyapCheck, 1, 1, 0)
		vbox2.pack_start(self.scaleDfectPos, 1, 1, 0)
		vbox2.pack_start(self.entryStrLength, 1, 1, 0)
		
		row1.add(hbox1)
		listbox.add(row1)

		self.tab2Box.pack_start(listbox, 1, 0, 0)
		self.pack_start(self.tab2Box, 1, 0, 0)

	def getDfctPos(self):
		pos = int(self.scaleDfectPos.get_value())
		return pos

	def getStrLength(self):
		length = int(self.entryStrLength.get_text())
		return length
	
class SettingsTab(Gtk.Box):

	tab3Box = Gtk.Box(orientation=0, spacing=30)
	comboCellSize = Gtk.ComboBox.new()
	s1Color = Gtk.ColorButton.new()
	s0Color = Gtk.ColorButton.new()
	bColor = Gtk.ColorButton.new()
	dColor = Gtk.ColorButton.new()
	folderButton = Gtk.Button()
	labelCellSize = Gtk.Label("Cell size: ", xalign=0)
	labels1Color = Gtk.Label("State 1 color: ", xalign=0)
	labels0Color = Gtk.Label("State 0 color: ", xalign=0)
	labelbColor = Gtk.Label("Background color: ", xalign=0)
	labeldColor = Gtk.Label("Defect color: ", xalign=0)
	labelFolderPath = Gtk.Label("../img/simulation/", xalign=0)

	def __init__(self):
		super(SettingsTab, self).__init__(orientation=1, spacing=30)
		self.set_border_width(20)

		model = Gtk.ListStore(str, int)
		model.append(["1 pixel", 1])
		model.append(["2 pixels", 2])
		model.append(["5 pixels", 5])
		model.append(["10 pixels", 10])

		folderIcon = Gio.ThemedIcon(name="user-desktop")
		folder = Gtk.Image.new_from_gicon(folderIcon, Gtk.IconSize.BUTTON)
		self.folderButton.add(folder)
		self.comboCellSize = Gtk.ComboBox.new_with_model(model)
		renderer_text = Gtk.CellRendererText()
		self.comboCellSize.pack_start(renderer_text, True)
		self.comboCellSize.add_attribute(renderer_text, "text", 0)
		self.comboCellSize.set_active(0)

		self.bColor.set_use_alpha(False)
		self.s1Color.set_use_alpha(False)
		self.s0Color.set_use_alpha(False)
		self.dColor.set_use_alpha(False)
		self.bColor.set_rgba(Gdk.RGBA(0.62, 0.62, 0.62, 1))
		self.s0Color.set_rgba(Gdk.RGBA(1, 1, 1, 1))
		self.s1Color.set_rgba(Gdk.RGBA(0, 0, 0, 1))
		self.dColor.set_rgba(Gdk.RGBA(1, 0, 0, 1))

		listbox = Gtk.ListBox()
		listbox.set_selection_mode(0)
		vbox1 = Gtk.Box(orientation=1, spacing=10)
		vbox2 = Gtk.Box(orientation=1, spacing=10)
		hbox1 = Gtk.Box(orientation=0, spacing=50)
		row1 = Gtk.ListBoxRow()
		
		hbox1.pack_start(vbox1, 1, 1, 0)
		hbox1.pack_start(vbox2, 1, 1, 0)
		vbox1.pack_start(self.labelCellSize, 1, 1, 0)
		vbox1.pack_start(self.labels1Color, 1, 1, 0)
		vbox1.pack_start(self.labels0Color, 1, 1, 0)
		vbox1.pack_start(self.labelbColor, 1, 1, 0)
		vbox1.pack_start(self.labeldColor, 1, 1, 0)
		vbox1.pack_start(self.labelFolderPath, 1, 1, 0)
		vbox2.pack_start(self.comboCellSize, 1, 1, 0)
		vbox2.pack_start(self.s1Color, 1, 1, 0)
		vbox2.pack_start(self.s0Color, 1, 1, 0)
		vbox2.pack_start(self.bColor, 1, 1, 0)
		vbox2.pack_start(self.dColor, 1, 1, 0)
		vbox2.pack_start(self.folderButton, 1, 1, 0)
		
		row1.add(hbox1)
		listbox.add(row1)

		self.tab3Box.pack_start(listbox, 1, 0, 0)
		self.pack_start(self.tab3Box, 1, 0, 0)

	def getSize(self):
		treeIter = self.comboCellSize.get_active_iter()

		if(treeIter is not None):
			model = self.comboCellSize.get_model()
			return int(model[treeIter][1])
			
		else:
			return 1

	def getbColor(self):
		bColor = self.bColor.get_rgba
		return bColor
	
	def getdColor(self):
		dColor = self.dColor.get_rgba
		return dColor

	def gets1Color(self):
		s1Color = self.s1Color.get_rgba
		return s1Color

	def gets0Color(self):
		s0Color = self.s0Color.get_rgba
		return s0Color 