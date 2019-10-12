import sys, pygame, subprocess, os, json

def openFile(fileName):
	"""
		Opens a .png image.

		Parameters
		----------
			fileName : string
				Path of the file.
	"""
	if sys.platform.startswith("darwin"):
		subprocess.call(("open", fileName))
	elif os.name == "nt":
		os.startfile(fileName)
	elif os.name == "posix":
		subprocess.call(("xdg-open", fileName))

def writeJSON(fileName, data):
	filePath = fileName + ".json"
	with open(filePath, "w") as fp:
		json.dump(data, fp)