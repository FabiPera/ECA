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

def writePrintable(tf, project, dict_evolucion):
	tf.write("\\documentclass[12pt, letterpaper]{article} \n")
	tf.write("\\usepackage{graphicx} \n")
	tf.write("\\usepackage{hyperref} \n")
	tf.write("\\usepackage[utf8]{inputenc} \n")
	tf.write("\\usepackage{float} \n")
	tf.write("\\usepackage{geometry} \n")
	tf.write("\\usepackage{enumitem, array} \n")
	tf.write("\\usepackage{longtable} \n")
	tf.write("\\usepackage{lscape} \n")
	tf.write("\\usepackage[export]{adjustbox} \n")
	tf.write("\\geometry{letterpaper, left=10mm, right=10mm, bottom=20mm, top=20mm} \n")
	# tf.write("\\graphicspath{ {./" + project + "/} } \n")
	tf.write("\\graphicspath{ {" + project + "} } \n")
	tf.write("\\renewcommand{\\rule}{Rule " + dict_evolucion["rule"] + "} \n")
	tf.write("\\renewcommand{\\r}{" + dict_evolucion["rule"] + "} \n")
	tf.write("\\title{ \\rule report} \n")
	tf.write("\\author{Fi } \n")
	tf.write("\\begin{document} \n")
	tf.write("\\begin{titlepage} \n")
	tf.write("\\maketitle \n")
	tf.write("\\tableofcontents \n")
	tf.write("\\end{titlepage} \n")
	tf.write("\\clearpage \n")
	tf.write("\\begin{figure}[H]\n")
	tf.write("  \\centering\n")
	tf.write("  \\includegraphics[height=200mm, width=200mm, keepaspectratio]{simAnalysis.png} \n")
	tf.write("   \\caption{\\rule evolution} \n")
	tf.write("\\end{figure}\n")
	tf.write("\\begin{table}[H]\n")
	tf.write("  \\centering\n")
	tf.write("  \\begin{tabular}{|c|c|c|c| }\n")
	tf.write("     \\hline Seed-Density & Fill & Length & Steps \\\\ \n")
	tf.write("      \\hline " + dict_evolucion["seed"] + " & " + dict_evolucion["fill"] + " & " + dict_evolucion["length"] + " & " + dict_evolucion["steps"] + " \\\\ \n")
	tf.write("      \\hline \n")
	tf.write("       \\end{tabular} \n")
	tf.write("      \\caption{Simulation data} \n")
	tf.write("    \\end{table} \n")

def writeGenotipico(tf, project, dict_opc , dict_evolucion):
	tf.write("  \\begin{section}{Análisis Genotípico} \n")
	if dict_opc["meanfield"]:
		with open("../img/MeanField/Regla"+dict_evolucion["rule"]+".json", 'r') as f:
			datos = json.load(f)
		f.close()
		tf.write("  \\begin{subsection}{Teorìa del Campo Promedio}\n")
		tf.write("  \\begin{figure}[H]\n")
		tf.write("  \\centering\n")
		tf.write("  \\includegraphics[max width=200mm ,max height=200 mm , keepaspectratio ]{../img/MeanField/Plot\\r.png}\n")
		tf.write("  \\caption{Gráfica del polinomio del campo promedio \\rule  }\n")
		tf.write("  \\end{figure}\n")
		tf.write("  \\begin{table}[H]\n")
		tf.write("  \\centering\n")
		tf.write("  \\begin{tabular}{|c|c|c|c|}\n")
		tf.write("  \\hline Regla & Polinomio  & Punto fijo &Derivada \\\\ \n")
		#', '.join(a)
		tf.write("  \\hline $\\r$ & $"+datos["Pol0"]+"$  &  $"+datos["Punto"]+"$  & $"+datos["Derivada"]+"$ \\\\  \\hline \n")

def generateReport(path, sr, rule, analysisOp):
	pass