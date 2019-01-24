import subprocess, os, sys

filepath="Simulation.png"
if sys.platform.startswith("darwin"):
	subprocess.call(("open", filepath))
elif os.name == "nt": # For Windows
	os.startfile(filepath)
elif os.name == "posix": # For Linux, Mac, etc.
	subprocess.call(("xdg-open", filepath))