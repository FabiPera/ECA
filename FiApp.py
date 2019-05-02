import gi, sys
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gio
from MainWin import MainWin

class FiApp(Gtk.Application):
	
	def __init__(self):
		super(FiApp, self).__init__()
	
	def do_activate(self):
		self.mainWindow=MainWin(self)
		self.mainWindow.show_all()

	def do_startup(self):
		Gtk.Application.do_startup(self)

app=FiApp()
app.run(sys.argv)
