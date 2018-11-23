import gi, sys
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from gi.repository import Gio
from Widgets import Widgets

class Window(Gtk.ApplicationWindow):
	def __init__(self, app):
		super(Window, self).__init__(title="ECA", application=app)
		widgets=Widgets()
		self.set_default_size(500, 300)
		self.set_resizable(False)
		#toolbar=widgets.toolbar
		grid = Gtk.Grid()
		'''
		fmi = Gtk.MenuItem.new_with_label("File")
		
		emi = Gtk.MenuItem.new_with_label("Exit") 
		emi.connect("activate", self.quitApp)
		'''
		
		self.add(widgets.mainLayout)
		
	def quitApp(self, par):
		app.quit()

class Application(Gtk.Application):
	def __init__(self):
		super(Application, self).__init__()
	
	def do_activate(self):
		self.win=Window(self)
		self.win.show_all()

	def do_startup(self):
		Gtk.Application.do_startup(self)

app=Application()
app.run(sys.argv)
