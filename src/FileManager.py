import sys, pygame, subprocess, os, json

def openFile(self, filePath="../img/", fileName="simulation.png"):
	path = filePath + fileName
	if sys.platform.startswith("darwin"):
		subprocess.call(("open", path))
	elif os.name == "nt":
		os.startfile(path)
	elif os.name == "posix":
		subprocess.call(("xdg-open", path))

def writeJSON(fileName, data):
	filePath=fileName + ".json"
	with open(filePath, "w") as fp:
		json.dump(data, fp)