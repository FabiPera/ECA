import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from gi.repository import Gio
from gi.repository import Gdk
from ECA import ECA
from Simulation import Simulation
from PhenAnalyzer import PhenAnalyzer

class SimSettingsWindow():
	
	cellPixelSize=2
	cell1Color=(0.0, 0.0, 0.0)
	cell0Color=(1.0, 1.0, 1.0)
	bckgColor=(0.6, 0.6, 0.6)
	dfctColor=(1.0, 1.0, 1.0)
	mainLayout=Gtk.Box(orientation=1)
	layout1=Gtk.Box(orientation=1, spacing=30)
	layout11=Gtk.Box(orientation=0)
	layout12=Gtk.Box(orientation=0)
	layout13=Gtk.Box(orientation=0)
	header=Gtk.HeaderBar.new()
	pixelAdj=Gtk.Adjustment.new(0, 1, 5, 1, 1, 1)
	pixelScale=Gtk.Scale.new(0, pixelAdj)
	cell1Button=Gtk.ColorButton.new_with_color(Gdk.Color.from_floats(0.0, 0.0, 0.0))
	cell0Button=Gtk.ColorButton.new_with_color(Gdk.Color.from_floats(1.0, 1.0, 1.0))
	bckgButton=Gtk.ColorButton.new_with_color(Gdk.Color.from_floats(0.6, 0.6, 0.6))
	dfctButton=Gtk.ColorButton.new_with_color(Gdk.Color.from_floats(1.0, 0.0, 0.0))

	def __init__(self):
		self.createLayout()
		self.mainLayout.pack_start(self.layout1, 1, 0 ,0)

	def createLayout(self):
		self.header.set_show_close_button(True)
		self.header.props.title="HeaderBar example"
		labelCellSize=Gtk.Label.new("Cell size(in Pixels): ")
		labelCell1=Gtk.Label.new("Cell 1 color: ")
		labelCell0=Gtk.Label.new("Cell 0 color: ")
		labelDfct=Gtk.Label.new("Defect color: ")
		labelBckg=Gtk.Label.new("Background color: ")

		self.layout11.set_halign(0)
		self.layout12.set_halign(0)
		self.layout13.set_halign(0)

		self.layout11.pack_start(labelCellSize, 1, 0, 10)
		self.layout11.pack_start(self.pixelScale, 1, 0, 10)
		self.layout12.pack_start(labelCell1, 1, 0, 10)
		self.layout12.pack_start(self.cell1Button, 1, 0, 10)
		self.layout12.pack_start(labelCell0, 1, 0, 10)
		self.layout12.pack_start(self.cell0Button, 1, 0, 10)
		self.layout12.pack_start(labelDfct, 1, 0, 10)
		self.layout12.pack_start(self.dfctButton, 1, 0, 10)
		self.layout12.pack_start(labelBckg, 1, 0, 10)
		self.layout12.pack_start(self.bckgButton, 1, 0, 10)

		self.layout1.pack_start(self.layout11, 1, 0, 0)
		self.layout1.pack_start(self.layout12, 1, 0, 0)