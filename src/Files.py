import sys, subprocess, os, json, base64

def openFile(filePath="../img/", fileName="simulation.png"):
	path = filePath + fileName
	if(sys.platform.startswith("darwin")):
		subprocess.call(("open", path))
	elif(os.name == "nt"):
		os.startfile(path)
	elif(os.name == "posix"):
		subprocess.call(("xdg-open", path))

def writeJSON(fileName, data):
	filePath = fileName + ".json"
	with open(filePath, "w") as fp:
		json.dump(data, fp)
	
def imageToString(path, imageName):
	path += imageName
	with open(path, "rb") as imageFile:
		base64Str = base64.b64encode(imageFile.read())

	return base64Str

def stringToImage(base64String, path="../"):
	fh = open("test.png", "wb")
	fh.write(base64.b64decode(base64String))
	fh.close()