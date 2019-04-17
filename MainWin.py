import gi, FileManager as fileMan
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gio
from ECA import ECA
from Simulation import Simulation
from PhenAnalyzer import PhenAnalyzer

class MainWin(Gtk.ApplicationWindow):

	mainGrid=Gtk.Grid()
	tab1Layout=Gtk.Box(orientation=1, spacing=30)
	tab2Layout=Gtk.Box(orientation=1, spacing=30)
	tab1=Gtk.Grid()
	tab2=Gtk.Grid()
	tabView=Gtk.Notebook.new()
	toolbar=Gtk.Toolbar()
	adjRule=Gtk.Adjustment.new(0, 0, 256, 1, 1, 1)
	adjDens=Gtk.Adjustment.new(50, 0, 100, 1, 1, 1)
	adjWidth=Gtk.Adjustment.new(0, 0, 8192, 8, 1, 1)
	adjHeigth=Gtk.Adjustment.new(0, 0, 8192, 8, 1, 1)
	switchRandConf=Gtk.Switch.new()
	switchStr=Gtk.Switch.new()
	scaleRule=Gtk.Scale.new(0, adjRule)
	scaleDens=Gtk.Scale.new(0, adjDens)
	entryRule=Gtk.SpinButton.new(adjRule, 1, 0)
	entrySeed=Gtk.Entry.new()
	entrySteps=Gtk.SpinButton.new(adjHeigth, 8, 0)
	entryCells=Gtk.SpinButton.new(adjWidth, 8, 0)
	entryPer=Gtk.Entry.new()
	entryDefect=Gtk.Entry.new()
	entryStrLength=Gtk.Entry.new()
	imageLayout=Gtk.Box(orientation=0, spacing=50)
	image=Gtk.Image.new_from_file("./Rules/rule0.png")
	switchRandValue=0
	switchConfValue=0
	
	def __init__(self, app):
		super(MainWin, self).__init__(title="ECA", application=app)
		self.set_default_size(500, 250)
		self.set_resizable(False)
		self.createToolbar()
		self.createTabView()
		self.add(self.mainGrid)

	def createToolbar(self):
		#"help-faq"
		#"applications-graphics"
		#"applications-science"
		#"preferences-desktop"
		imgExit=Gtk.Image.new_from_icon_name("application-exit", 0)
		imgLoad=Gtk.Image.new_from_icon_name("document-open", 0)
		imgSave=Gtk.Image.new_from_icon_name("media-floppy", 0)
		imgRun=Gtk.Image.new_from_icon_name("media-playback-start", 0)
		imgAnalysis=Gtk.Image.new_from_icon_name("edit-find", 0)
		imgSimSettings=Gtk.Image.new_from_icon_name("preferences-desktop-theme", 0)

		exitApp=Gtk.ToolButton.new(imgExit, "Exit")
		load=Gtk.ToolButton.new(imgLoad, "Load settings")
		save=Gtk.ToolButton.new(imgSave, "Save settings")
		run=Gtk.ToolButton.new(imgRun, "Run simulation")
		analysis=Gtk.ToolButton.new(imgAnalysis, "Run analysis")
		simSettings=Gtk.ToolButton.new(imgSimSettings, "Simulation settings")

		self.toolbar.insert(exitApp, -1)
		self.toolbar.insert(load, -1)
		self.toolbar.insert(save, -1)
		self.toolbar.insert(run, -1)
		self.toolbar.insert(analysis, -1)
		self.toolbar.insert(simSettings, -1)
		
		self.mainGrid.attach(self.toolbar, 0, 0, 6, 1)

	def createTab1(self):
		labelRule=Gtk.Label.new("Rule: ")
		labelRandConf=Gtk.Label.new("Random conf: ")
		labelConf=Gtk.Label.new("Seed: ")
		labelStr0=Gtk.Label.new("Fill 0:")
		labelStr1=Gtk.Label.new("1")
		labelSteps=Gtk.Label.new("Steps: ")
		labelCells=Gtk.Label.new("Cells: ")
		labelDens=Gtk.Label.new("Density (%): ")
		
		self.switchStr.set_active(False)
		self.switchRandConf.set_active(False)
		self.scaleRule.set_digits(0)
		self.scaleDens.set_sensitive(False)
		self.entrySeed.set_width_chars(20)
		self.entrySteps.set_width_chars(5)
		self.entryCells.set_width_chars(5)
		#self.entryPer.set_width_chars(5)

		self.tab1.attach(labelRandConf, 0, 0, 1, 1)
		self.tab1.attach(self.switchRandConf, 1, 0, 1, 1)
		self.tab1.attach(labelStr0, 0, 1, 1, 1)
		self.tab1.attach(self.switchStr, 1, 1, 1, 1)
		#self.tab1.attach(labelStr1, 4, 0, 1, 1)
		self.tab1.attach(labelRule, 0, 2, 1, 1)
		self.tab1.attach(self.scaleRule, 1, 2, 1, 1)
		self.tab1.attach(labelConf, 0, 3, 1, 1)
		self.tab1.attach(self.entrySeed, 1, 3, 1, 1)
		self.tab1.attach(labelSteps, 0, 4, 1, 1)
		self.tab1.attach(self.entrySteps, 1, 4, 1, 1)
		self.tab1.attach(labelCells, 0, 5, 1, 1)
		self.tab1.attach(self.entryCells, 1, 5, 1, 1)
		self.tab1.attach(labelDens, 0, 6, 1, 1)
		self.tab1.attach(self.scaleDens, 1, 6, 1, 1)
		self.tab1.attach(self.imageLayout, 2, 0, 3, 5)
		self.imageLayout.pack_start(self.image, 1, 0, 0)

		self.switchRandConf.connect("notify::active", self.switchRandActivate)
		self.switchStr.connect("notify::active", self.switchConfActivate)
		self.adjWidth.connect("value_changed", self.changeStepWidth)
		self.adjHeigth.connect("value_changed", self.changeStepHeigth)
		self.scaleRule.connect("value_changed", self.changeRuleImg)
		self.tab1Layout.set_border_width(20)
		self.tab1.set_row_spacing(5)
		self.tab1.set_column_spacing(10)
		self.tab1.set_column_homogeneous(False)
		self.tab1Layout.pack_start(self.tab1, 1, 0, 0)

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
		self.createTab1()
		#self.createTab2()
		self.tabView.append_page(self.tab1Layout, tabLabel1)
		self.mainGrid.attach(self.tabView, 0, 1, 6, 3)
		#self.tabView.append_page(self.tab2Layout, tabLabel2)
		#self.tabViewLayout.pack_start(self.tabView, 0, 0, 0)

	def showSimSettings(self, widget):
		self.simSettingsWindow.show_all()

	def quitApp(self, par):
		self.destroy()
		#self.app.quit()

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
		if(switchStr.get_active()):
			self.switchConfValue=1
		else:
			self.switchConfValue=0

	def changeRuleImg(self, widget):
		val=int(self.scaleRule.get_value())
		self.image.set_from_file("./Rules/rule"+str(val)+".png")
		#self.imageLayout.pack_start(self.image, 1, 0, 0)

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

	def saveSettings(self, button):
		dialog=Gtk.FileChooserDialog("Save settings", None, Gtk.FileChooserAction.SAVE, (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_SAVE, Gtk.ResponseType.OK))
		response=dialog.run()
		if(response == Gtk.ResponseType.OK):
			rule=self.entryRule.get_value_as_int()
			steps=self.getIntValue(self.entrySteps)
			cells=self.getIntValue(self.entryCells)
			
			if(self.switchRandValue):
				dens=self.getIntValue(self.entryPer)
			else:
				seed=self.getStringValue(self.entrySeed)
			data={}
			data["rule"]=str(rule)
			data["seed"]=seed
			data["steps"]=str(steps)
			data["cells"]=str(cells)
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
			print("Settings load")
			print("File selected: " + dialog.get_filename())
		elif(response == Gtk.ResponseType.CANCEL):
			print("Cancel clicked")
		dialog.destroy()