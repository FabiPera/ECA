import sys, subprocess, os, json, base64

def openFile(fileName="../sim/simulation.png"):
	if(sys.platform.startswith("darwin")):
		subprocess.call(("open", fileName))
	elif(os.name == "nt"):
		os.startfile(fileName)
	elif(os.name == "posix"):
		subprocess.call(("xdg-open", fileName))

def writeJSON(fileName, data):
	filePath = fileName + ".json"
	with open(filePath, "w") as fp:
		json.dump(data, fp)
	
def imageToString(imageName):
	with open(imageName, "rb") as imageFile:
		base64Str = base64.b64encode(imageFile.read())

	return base64Str

def stringToImage(base64String, fileName):
	fh = open(fileName, "wb")
	fh.write(base64.b64decode(base64String))
	fh.close()

def loadSettings(fileName):
	name = fileName.split(".")[0] + ".png"
	with open(fileName) as json_file:
		data = json.load(json_file)

	b = data["img"].split("'")
	stringToImage(b[1], name)

	return data