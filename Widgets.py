import gi, sys
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from gi.repository import Gio

class Widgets():
	mainLayout=Gtk.Box(1, 0)
	toolbarLayout=Gtk.Box(0, 0)
	toolbar=Gtk.Toolbar()
	tabView=Gtk.Notebook.new()
	tab1Layout=Gtk.Box(1, 0)
	tab2Layout=Gtk.Box(1, 0)
	layout11=Gtk.Box(0, 0)
	adjRule=Gtk.Adjustment.new(0, 0, 256, 1, 1, 1)
	entryRule=Gtk.SpinButton.new(adjRule, 1, 0)
	switch=Gtk.Switch.new()
	layout12=Gtk.Box(0, 0)
	layout13=Gtk.Box(0, 0)
	layout14=Gtk.Box(0, 0)
	layout15=Gtk.Box(0, 0)
	
	def __init__(self):
		self.createToolbar()
		self.createTabView()
		self.toolbarLayout.pack_start(self.toolbar, 0, 0, 0)
		self.mainLayout.pack_start(self.toolbarLayout, 0, 1, 0)
		self.mainLayout.pack_start(self.tabView, 0, 1, 0)

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

	def createTab1(self):
		labelRule=Gtk.Label.new("Rule: ")
		labelRandConf=Gtk.Label.new("Random configuration: ");
		labelConf=Gtk.Label.new("Configuration: ");
		labelSteps=Gtk.Label.new("Steps: ");
		labelCells=Gtk.Label.new("Cells: ");
		labelDens=Gtk.Label.new("Density (%): ");
		self.switch.setActive(False)
		self.layout11.pack_start(labelRule, 0, 1, 0)
		self.layout11.pack_start(self.entryRule, 0, 1, 0)
		self.layout11.pack_start(labelRandConf, 0, 1, 0)
		self.layout11.pack_start(self.switch, 0, 1, 0)
		self.tab1Layout.pack_start(self.layout11, 0, 1, 0)

	def createTab2(self):
		pass
	
	def createTabView(self):
		tabLabel1=Gtk.Label.new("Simulation Settings")
		tabLabel2=Gtk.Label.new("Analysis")
		self.tabView.append_page(self.tab1Layout, tabLabel1)
		
