import numpy as np, os
from pylatex import Document, Section, Subsection, Head, Math, PageStyle, Axis, Plot, Figure, Matrix, Alignat, MiniPage, NoEscape, LargeText, LineBreak, basic
from pylatex.utils import bold

def createPDFReport(rule=90):
	geometry_options = {"left" : "1.5cm", "right" : "1.5cm", "top" : "2.5cm", "bottom" : "2.0cm"}
	doc = Document(geometry_options=geometry_options)
	first_page = PageStyle("firstpage")

	with first_page.create(Head("C")) as title_header:
		with title_header.create(MiniPage(width=NoEscape(r"0.49\textwidth"), pos='c', align='r')) as title_wrapper:
			title_wrapper.append(LargeText(bold("Rule" + str(rule) + " simulation analysis")))
			title_wrapper.append(LineBreak())
			#title_wrapper.append(MediumText(bold("Date")))

	with doc.create(Section("Simulation")):
		with doc.create(Figure(position='h!')) as sim_pic:
			sim_pic.add_image("../img/simulation.png", width="200px")
			#sim_pic.add_caption('Look it\'s on its back')

	with doc.create(Section("Damage spreading")):
		with doc.create(Figure(position='h!')) as sim_pic:
			sim_pic.add_image("../img/dsimulation.png", width="200px")
			#sim_pic.add_caption('Look it\'s on its back')

	with doc.create(Section("Density")):
		with doc.create(Figure(position='h!')) as sim_pic:
			sim_pic.add_image("../img/Density.png", width="200px")
			#sim_pic.add_caption('Look it\'s on its back')

	basic.NewPage()

	with doc.create(Section("Entropy")):
		with doc.create(Figure(position='h!')) as sim_pic:
			sim_pic.add_image("../img/Entropy.png", width="200px")
			#sim_pic.add_caption('Look it\'s on its back')

	with doc.create(Section("Lyapunov Exponents")):
		with doc.create(Figure(position='h!')) as sim_pic:
			sim_pic.add_image("../img/LyapunovExp.png", width="200px")
			#sim_pic.add_caption('Look it\'s on its back')

	doc.generate_pdf('full', clean_tex=False)

createPDFReport()