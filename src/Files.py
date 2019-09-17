import numpy as np, os
from pylatex import Document, Section, Subsection, Tabular, Math, TikZ, Axis, Plot, Figure, Matrix, Alignat
from pylatex.utils import italic

def createPDFReport(rule=90):
	geometry_options = {"left" : "1.5cm", "right" : "1.5cm", "top" : "2.5cm", "bottom" : "2.0cm"}
	doc = Document(documentclass="letterpaper", geometry_options=geometry_options)

	with doc.create(Section("Rule" + str(rule) + " simulation analysis"))

createPDFReport()