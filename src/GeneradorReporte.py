import json 
import os

def writePrintable(tf,project, dict_evolucion):
  tf.write("\\documentclass[12pt, letterpaper]{article} \n ")
  tf.write("\\usepackage{graphicx} \n ")
  tf.write("\\usepackage{hyperref} \n ")
  tf.write("\\usepackage[utf8]{inputenc} \n ")
  tf.write("\\usepackage{float} \n ")
  tf.write("\\usepackage{geometry} \n ")
  tf.write("\\usepackage{enumitem, array} \n ")
  tf.write("\\usepackage{longtable} \n ")
  tf.write("\\usepackage{lscape} \n ")
  tf.write("\\usepackage[export]{adjustbox} \n ")
  tf.write("\\geometry{letterpaper,left=10mm,right=10mm,bottom=20mm,top=20mm} \n ")
  tf.write("\\graphicspath{ {./"+project+"/} } \n ")
  tf.write("\\renewcommand{\\rule}{Regla "+dict_evolucion["rule"]+"} \n ")
  tf.write("\\renewcommand{\\r}{"+dict_evolucion["rule"]+"} \n ")
  tf.write("\\title{ Reporte \\rule } \n ")
  tf.write("\\author{Fi App} \n ")
  tf.write("\\begin{document} \n ")
  tf.write("\\begin{titlepage} \n ")
  tf.write("\\maketitle \n ")
  tf.write("\\tableofcontents \n ")
  tf.write("\\end{titlepage} \n ")
  tf.write("\\clearpage \n ")
  tf.write("\\begin{figure}[H]\n")
  tf.write("  \\centering\n")
  tf.write("  \\includegraphics[height=200mm,width=200mm,keepaspectratio]{simAnalysis.png} \n")
  tf.write("   \\caption{Simulación de \\rule} \n")
  tf.write("\\end{figure}\n")
  tf.write("\\begin{table}[H]\n")
  tf.write("  \\centering\n")
  tf.write("  \\begin{tabular}{|c|c|c|c| }\n")
  tf.write("     \\hline Semilla-Densidad & Fill & Length & Steps  \\\\ \n")
  tf.write("      \\hline    "+dict_evolucion["seed"]+" & "+dict_evolucion["fill"]+" & "+dict_evolucion["length"]+" & "+dict_evolucion["steps"]+" \\\\ \n")
  tf.write("      \\hline \n")
  tf.write("       \\end{tabular} \n")
  tf.write("      \\caption{Datos de la simulación} \n")
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

    tf.write("  \\end{tabular}\n")
    tf.write("  \\caption{Datos de la gráfica del campo promedio}\n")
    tf.write("  \\end{table}\n")
    tf.write("  \\end{subsection}\n")
    tf.write("  \\clearpage\n")

  if dict_opc["attractor"]:
    tf.write("  \\clearpage\n")
    tf.write("  \\begin{subsection}{Campos de atractores}\n")
    tf.write("  \\begin{center}\n")
    tf.write("    \\begin{longtable}{|c|c|c|c||c|c||c|}\n")
    tf.write("  \\hline \n")
    tf.write("  Num & Ciclo & Altura &Nodos &  Atractor &  Jardin del edén  & Entropia \\\\ \\endhead \n")
    k = 1
    for i in dict_evolucion["attractor_json"]:
      with open(project+"/"+i, 'r') as f:
        datos = json.load(f)
        #atractor, entropy, jardin, max_level size_ring, size_tree
      tf.write("  \\hline \\hline    "+str(k)+" & "+str(datos["size_ring"])+" & "+
              str(datos["max_level"])+" & "+str(datos["size_tree"])+" & "+str(datos["atractor"])+"  & "+
              str(datos["jardin"])+" & "+str(datos["entropy"])[:8]+" \\\\ \\hline \n")
      k=k+1
      f.close()

    tf.write("  \\end{longtable} \n")
    tf.write("  \\end{center} \n")
    tf.write("  \\clearpage \n")
    
    tf.write("  \\begin{longtable}{|c|} \n")
    tf.write("  \\hline \n")
    k = 1
    for i in dict_evolucion["attractor_png"]:    
      tf.write("  \\includegraphics[width=.5\\textwidth ,keepaspectratio ]{"+i+"} \\\\ \n")
      tf.write("    "+str(k)+" \\\\ \\hline \n")
      k=k+1
    tf.write("  \\end{longtable}\n")
    tf.write("  \\end{subsection} \n")

  tf.write(" \\end{section} \n") 

def writeFenotipico(tf ,dict_opc, dict_evolucion, ):

  tf.write("\\begin{section}{Análisis Fenotípico} \n")
  ###### Densidad 
  if dict_opc["density"]: 
    tf.write("  \\begin{subsection}{Densidad} \n")
    tf.write("    \\begin{figure}[H] \n")
    tf.write("      \\centering \n")
    tf.write("       \\includegraphics[max width=200mm ,max height=200mm , keepaspectratio ]{SimDensity.png} \n")
    tf.write("       \\caption{Densidad de \\rule} \n")
    tf.write("    \\end{figure} \n")
    tf.write("  \\end{subsection} \n")
  ###### Entropia
  if dict_opc["entropy"]:
    tf.write("  \\begin{subsection}{Entropía} \n")
    tf.write("    \\begin{figure}[H] \n")
    tf.write("    \\centering \n")
    tf.write("    \\includegraphics[max width=200mm ,max height=200 mm , keepaspectratio ]{SimEntropy.png} \n")
    tf.write("    \\caption{Entropía de \\rule} \n")
    tf.write("    \\end{figure} \n")
    tf.write("    \\end{subsection}\n")
  ###### Exponente de Lyapunov
  if dict_opc["lyapunov"]:
    tf.write("    \\begin{subsection}{Exponentes de Lyapunov} \n")
    tf.write("    \\begin{figure}[H] \n")
    tf.write("    \\centering \n")
    tf.write("    \\includegraphics[max width=200mm ,max height=200 mm , keepaspectratio ]{SimDefects.png} \n")
    tf.write("    \\caption{Simulación de los defectos del Exponentes de Lyapunov \\rule} \n")
    tf.write("    \\end{figure} \n")
    tf.write("    \\end{subsection} \n")
    tf.write("    \\begin{table}[H] \n")
    tf.write("    \\centering \n")
    tf.write("    \\begin{tabular}{cc} \n")
    tf.write("    \\includegraphics[width=70mm ,max height=70 mm , keepaspectratio]{SimAnalysis.png} & \includegraphics[width=70mm ,max height=70 mm , keepaspectratio]{SimDefects.png} \\ \n")
    tf.write("    \\end{tabular} \n")
    tf.write("    \\caption{Simulación de la evolución original contra los defectos del Exponentes de Lyapunov \\rule} \n")
    tf.write("    \\end{table} \n")
    tf.write("    \\begin{table}[H] \n")
    tf.write("    \\centering \n")
    tf.write("    \\begin{tabular}{cc} \n")
    tf.write("    \\includegraphics[width=90mm ,max height=90mm , keepaspectratio]{LyapunovExp.png} & \includegraphics[width=90mm ,max height=90mm , keepaspectratio]{LyapunovExpNorm.png} \\ \n")
    tf.write("    \\end{tabular} \n")
    tf.write("    \\caption{Simulación original contra los defectos del Exponentes de Lyapunov \\rule} \n")
    tf.write("    \\end{table} \n")
    #tf.write("    \\end{subsection} \n")
  
  tf.write("    \\end{section} \n")
  tf.write("    \\clearpage \n")
  """
  seed = random (%) seed (0...)
  fill 

  """
def write( project, dict_opc, dict_evolucion ):
  tf = open(project+".tex", 'w')
  
  writePrintable(tf , project, dict_evolucion)
  writeFenotipico(tf, dict_opc, dict_evolucion)
  writeGenotipico(tf, project, dict_opc, dict_evolucion)
  tf.write("\\end{document}")
  tf.close()
  os.system('lualatex '+project+".tex")
  os.system("rm *.aux *.log *.out *.toc")



dict_opc = { "density": True , "entropy": True , "lyapunov":True , "meanfield":True, "attractor":True}
dict_evolucion = {"rule":"22", "seed":"50" , "fill":"0", "length":"256", "steps":"512",
    "attractor_json": ['22_16_s_t_11721s_r_1m_l_42atractor_0_.json', '22_16_s_t_550s_r_14m_l_12atractor_3_.json', '22_16_s_t_1510s_r_12m_l_29atractor_5_.json', '22_16_s_t_98s_r_12m_l_11atractor_32784_.json', '22_16_s_t_28s_r_6m_l_5atractor_33153_.json', '22_16_s_t_16s_r_4m_l_3atractor_1285_.json', '22_16_s_t_2s_r_2m_l_1atractor_13107_.json', '22_16_s_t_1s_r_1m_l_1atractor_21845_.json']
    ,"attractor_png":['22_16_s_t_11721s_r_1m_l_42atractor_0_.png', '22_16_s_t_550s_r_14m_l_12atractor_3_.png', '22_16_s_t_1510s_r_12m_l_29atractor_5_.png', '22_16_s_t_98s_r_12m_l_11atractor_32784_.png', '22_16_s_t_28s_r_6m_l_5atractor_33153_.png', '22_16_s_t_16s_r_4m_l_3atractor_1285_.png', '22_16_s_t_2s_r_2m_l_1atractor_13107_.png', '22_16_s_t_1s_r_1m_l_1atractor_21845_.png']
    }


project = "../img/simulation"
print(dict_evolucion)
write(project, dict_opc, dict_evolucion)

"""
[
  ['22_16_s_t_11721s_r_1m_l_42atractor_0_.json', '22_16_s_t_550s_r_14m_l_12atractor_3_.json', '22_16_s_t_1510s_r_12m_l_29atractor_5_.json', '22_16_s_t_98s_r_12m_l_11atractor_32784_.json', '22_16_s_t_28s_r_6m_l_5atractor_33153_.json', '22_16_s_t_16s_r_4m_l_3atractor_1285_.json', '22_16_s_t_2s_r_2m_l_1atractor_13107_.json', '22_16_s_t_1s_r_1m_l_1atractor_21845_.json'],
  ['22_16_s_t_11721s_r_1m_l_42atractor_0_.png', '22_16_s_t_550s_r_14m_l_12atractor_3_.png', '22_16_s_t_1510s_r_12m_l_29atractor_5_.png', '22_16_s_t_98s_r_12m_l_11atractor_32784_.png', '22_16_s_t_28s_r_6m_l_5atractor_33153_.png', '22_16_s_t_16s_r_4m_l_3atractor_1285_.png', '22_16_s_t_2s_r_2m_l_1atractor_13107_.png', '22_16_s_t_1s_r_1m_l_1atractor_21845_.png'],
  ['22_16_s_t_11721s_r_1m_l_42atractor_0_-histograma.png', '22_16_s_t_550s_r_14m_l_12atractor_3_-histograma.png', '22_16_s_t_1510s_r_12m_l_29atractor_5_-histograma.png', '22_16_s_t_98s_r_12m_l_11atractor_32784_-histograma.png', '22_16_s_t_28s_r_6m_l_5atractor_33153_-histograma.png', '22_16_s_t_16s_r_4m_l_3atractor_1285_-histograma.png', '22_16_s_t_2s_r_2m_l_1atractor_13107_-histograma.png', '22_16_s_t_1s_r_1m_l_1atractor_21845_-histograma.png']
]
"""