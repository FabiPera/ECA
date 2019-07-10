import gi, sys
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gio
from FiGUI import *

class FiApp(Gtk.Application):
	
	def __init__(self):
		super(FiApp, self).__init__()
	
	def do_activate(self):
		self.mainWindow=MainWindow(self)
		
		self.mainWindow.tab1Layout.switchRandConf.connect("notify::active", self.switchRandActivate)
		self.mainWindow.tab1Layout.switchStr.connect("notify::active", self.switchConfActivate)
		self.mainWindow.tab1Layout.adjWidth.connect("value_changed", self.changeStepWidth)
		self.mainWindow.tab1Layout.adjHeigth.connect("value_changed", self.changeStepHeigth)
		self.mainWindow.tab1Layout.scaleRule.connect("value_changed", self.changeRuleImg)
		self.mainWindow.tab2Layout.adjStrLenght.connect("value_changed", self.changeStrLenght)
		
		self.mainWindow.show_all()

	def do_startup(self):
		Gtk.Application.do_startup(self)

	def switchRandActivate(self, switchRandConf, active):
		if(switchRandConf.get_active()):
			self.mainWindow.tab1Layout.entrySeed.set_sensitive(False)
			self.mainWindow.tab1Layout.switchStr.set_sensitive(False)
			self.mainWindow.tab1Layout.scaleDens.set_sensitive(True)
			self.mainWindow.tab1Layout.switchRandValue = 1
		else:
			self.mainWindow.tab1Layout.entrySeed.set_sensitive(True)
			self.mainWindow.tab1Layout.switchStr.set_sensitive(True)
			self.mainWindow.tab1Layout.scaleDens.set_sensitive(False)
			self.mainWindow.tab1Layout.switchRandValue = 0
		
	def switchConfActivate(self, switchStr, active):
		label = self.mainWindow.tab1Layout.tab1Grid.get_child_at(0, 1)
		if(switchStr.get_active()):
			self.mainWindow.tab1Layout.switchConfValue = 1
			label.set_text("Fill w/1")
		else:
			self.mainWindow.tab1Layout.switchConfValue = 0
			label.set_text("Fill w/0")

	def changeRuleImg(self, widget):
		label = self.mainWindow.tab1Layout.tab1Grid.get_child_at(2, 0)
		val = int(self.mainWindow.tab1Layout.scaleRule.get_value())
		label.set_text("Rule "+str(val)+" icon")
		self.mainWindow.tab1Layout.ruleImage.set_from_file("../img/rule"+str(val)+".png")

	def changeStepWidth(self, widget):
		val = self.mainWindow.tab1Layout.adjWidth.get_value()
		self.mainWindow.tab2Layout.adjDfctPos.set_upper(val)
		self.mainWindow.tab2Layout.adjDfctPos.set_value((val // 2) - 1)
		if(val):
			self.mainWindow.tab1Layout.adjWidth.set_step_increment(val)
		else:
			self.mainWindow.tab1Layout.adjWidth.set_step_increment(8)

	def changeStepHeigth(self, widget):
		val = self.mainWindow.tab1Layout.adjHeigth.get_value()
		if(val):
			self.mainWindow.tab1Layout.adjHeigth.set_step_increment(val)
		else:
			self.mainWindow.tab1Layout.adjHeigth.set_step_increment(8)

	def changeStrLenght(self, widget):
		val = self.mainWindow.tab2Layout.adjStrLenght.get_value()
		if(val):
			self.mainWindow.tab2Layout.adjStrLenght.set_step_increment(val)
		else:
			self.mainWindow.tab2Layout.adjStrLenght.set_step_increment(8)

app=FiApp()
app.run(sys.argv)
