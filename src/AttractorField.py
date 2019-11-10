import collections, math, json, sys, os, os.path  
import graph_tool.all as gt, matplotlib.pyplot as plt
from ECA import ECA
from Bitstring import Bitstring

class Attractor:

	"""
	Clase que almacena un atractores y los atributos de este atractor.

	...

	Attributes
	----------
	entropy : float
			Entropia de los nodos de los trees
	frecuency : List [int, int]
			Lista de la frecuensia de la densidad de ancentros de cada nodo
			[d(numAncestros), freciencia]
	size_tree : int
			Total de nodos del arbol

	size_ring : int
			Longitud del atractor
	max_level : int 
			Nivel de la rama maxima

	atractor : List [ int : List[ int ] ]
	"""

	def __init__(self, tree=[], entropy=0.0, size_tree=0, size_ring=0, max_level=0 , frecuency={}):
		self.entropy = entropy
		self.size_tree = size_tree
		self.size_ring = size_ring
		self.max_level = max_level
		self.frecuency = frecuency
		self.tree = tree

	def __hash__(self):
		return hash((self.size_tree, self.size_ring, self.max_level))

	def __eq__(self, other):
		return self.size_tree == other.size_tree and self.size_ring == other.size_ring and self.max_level == self.max_level

	def __str__(self):
		return "s_t_" + str(self.size_tree) + "s_r_" + str(self.size_ring) + "m_l_" + str(self.max_level)

	def toJSON(self):
		return json.dumps(self, default=lambda o: o.__dict__,  sort_keys=True)


class Basin:
	"""
	Clase que almacena los campos de atractores de una regla y una longitud de anillo.

	1 ) Genera todas las evoluciones a -> b [b, a]
	...

	Attributes
	----------
	field : List [Atractor]
			Lista de los atractores de la regla
	evoluciones : List [ List [int, int] ]
			Pareja de todas las evoluciones N_a -> N_b [ [a,b] ]    rule : int
			Regla ECA
	ring : int 
			Longitud de Anillo
	eca : ECA 
			Objeto eca que nos permite evolucionar las configuraciones

	"""

	def __init__ (self, eca, rule):
		self.eca = eca
		self.rule = rule
		self.ring = eca.x.length
		self.evolutions = {}
		self.field = []

	def getEvolutions(self):
		evolutions = {}
		t0 = Bitstring(self.ring)
		for i in range(2 ** self.ring):
			t0.bsFromInt(i)
			t1 = self.eca.evolve(t0)
			j = t1.binToInt()
			if j in evolutions:
				evolutions[j].append(i)
			else : 
				evolutions[j] = [i]
		evolutions = collections.OrderedDict(sorted(evolutions.items()))
		
		return evolutions

	def getSeedTree(self, seed):
		self.evolutions = self.getEvolutions()
		# print("1")
		auxTree = self.getTree(seed)
		fileName = self.save_dot(auxTree)
		return auxTree, fileName

	def getTreeSet(self):
		self.evolutions = self.getEvolutions()
		dots=[]
		# print("1")
		i = 0

		try:
			while True:
				i = next(iter(self.evolutions.keys()))
				auxTree = self.getTree(i)
				if auxTree not in self.field:
					self.field.append(auxTree)
					dots.append(self.save_dot(auxTree) )      

		except StopIteration:
			pass
		print("Total trees: ", len(self.field))
		
		return self.field, dots 


    # Metodo que obtiene el arbol de una configuracion
    # 1 ) Obtiene el atractor 
    # 2 ) Recorre todos los nodos del atractor
    #   2.0 ) Obtiene las preimagenes de cada nodo
    #   2.1 ) Recorre todos los nodos de las preimagenes  
    #       2.2 ) Agrega la preimagen al arbol
    #       2.3 ) Suma a la altura 1 
	def getTree(self, configuracion):
		# Bandera para mostrar si hay ancestros por visitar
		flag = True
		#Indice que nos permite buscar los nodos no visitados
		i_k = 0
		#Indice que nos permite buscar el primer nodo del ultimo nivel
		_i_k = 0
		entropy = 0.0
		size_tree = 0
		size_ring = 0
		max_level = 0 
		frecuency = {}
		df = 0

		# 1 ) Obtiene el atractor 
		attractor = self.getAttractor(configuracion)
		size_ring = len(attractor)
		trees = []
		# 2 ) Recorre todos los nodos del atractor para agregarlos al arbol, 
		for _n_attractor in attractor:
			#   2.0 ) Obtiene las preimagenes de cada nodo        
			preimages = self.evolutions[_n_attractor]
			# Eliminar el elemento en el espacio de evoluciones
			del self.evolutions[_n_attractor]
			trees.append([_n_attractor, preimages])
			# Agrega la densidad del nodo a la frecuencia
			df = len(preimages)
			if df in frecuency:
				frecuency[df] = frecuency[df] + 1
			else:
				frecuency[df] = 1

		while flag:
			max_level += 1
			flag = False
			limit = len(trees)
			# Igualamos el indice _i_k y el _i_k, como al final no entra el ciclo _i_k obtiene el ultimo nivel 
			_i_k = i_k
			for i in range (i_k, limit):
				# Obtiene el nodo del arbol a aprtir del indice que se esta recorriendo
				node = trees [i]
				# recorre las preimagenes de ese nodo
				for _n_attractor in node[1] :
					# Busca si aun no se ha visitado. 
					if _n_attractor in self.evolutions:
						preimages  = self.evolutions[_n_attractor]
						del self.evolutions[_n_attractor]
						df = len(preimages)

						if df != 0 :
							flag = True
							if df in frecuency:
								frecuency[df]=frecuency[df]+1
							else :
								frecuency[df]=1

						trees.append([_n_attractor, preimages])
				# aumenta el indice a buscar 
				i_k +=1
        
        # Tamanio del arbol, que es el numero de nodos mas numero de hojas
        # Si nunca se movio el indice auxiliar significa que se ha encontrado un anoillo
		if _i_k == 0:
			size_tree = i_k
		else:
			df = self.getLenGarden(trees, _i_k) 
			size_tree = i_k + df
			max_level += 1
			frecuency[0] = df

		entropy = self.getEntropy(frecuency,size_tree)
		frecuency = dict(collections.OrderedDict(sorted(frecuency.items())))
		r = Attractor(trees, entropy, size_tree, size_ring, max_level, frecuency)

		return r

	# Metodo que devuelve una lista de nodos que al que converge el nodo
	def getAttractor(self, i):
		attractor = []
		t0 = Bitstring(self.ring)
		# convierte i a Bitstring 
		t0.bsFromInt(i)
		# Evoluciona la configuracion t0
		t1 = self.eca.evolve(t0)
		# Convierte el resultado a int 
		j = t1.binToInt()
		"Si el numero evoluciona a si mismo el ciclo es de longitud 0 "
		attractor.append (i)
		if(i == j):
			return attractor
		else :
			# Mientras la evolucion siguiente no este en el arreglo
			while j not in attractor:
				attractor.append(j)
				# convierte j en i para hacer la siguiente evolucion
				i = j
				# convierte i a Bitstring 
				t0.bsFromInt(i)
				# Evoluciona la configuracion t0
				t1 = self.eca.evolve(t0)
				# Convierte el resultado a int 
				j = t1.binToInt()
            # Obtener el indice donde esta el primer elemento del anilllo
			k = attractor.index(j)
			
			return attractor[k:]

	def getGarden(self, tree, k):
		gardens = []
		for i in range(k, len(tree)):
			gardens += tree[i][1]
		
		return gardens

	def getLenGarden(self, tree, k):
		gardens = 0
		for i in range(k, len(tree)):
			gardens += len(tree[i][1])
		
		return gardens

	def getEntropy(self, frequency, size):
		entropy = 0.0
		p = 0.0
		for f in frequency:
			p = frequency[f] / size
			entropy += p * math.log2(p)

		return -1 * (entropy)

	def save_dot(self, tree):
		data = tree.tree
		name = "../img/simulation/" + str(self.rule) + "_" + str(self.ring) + "_" + str(tree) + ".dot"
		tf = open(name, 'w')
		tf.write("graph G {\n")
		for e in data:
			i = e[0]
			tf.write(str(i) + ";\n")
		for e in data :
			i = e[0]
			for j in e[1]:
				tf.write(str(i) + "--" + str(j) + ";\n")
		
		tf.write("\n}")
		tf.close()
		return name

"""
fractales = [26,94,154,164, 18,22,60,90, 122, 126, 105, 146, 150,106]
for i in fractales:
    b = basin (i,16)
    b.getSeedTree(1)
print("--- %s seconds ---" % (time.time() - start_time))
"""

def Attractor_All(eca):
	b = Basin (eca)
	trees, files = b.getTreeSet()
	for i in range(len(trees)):
		auxTree = trees[i]
		file_name = files[i]
		g2 = gt.load_graph(file_name)
		graph_name = file_name[:-3] + "png"
		json_name = file_name[:-3] + "json"


def AttractorFromSeed(eca, r, seed = None):
	jsons = []
	graph = []
	hist = []
	b = Basin(eca, r)

	if(seed == None):
		trees, files = b.getTreeSet()
	else :
		trees= []
		files = []
		auxTree, file_name = b.getSeedTree(seed)
		trees.append(auxTree)
		files.append(file_name)

	for i in range(len(trees)):
		auxTree = trees[i]
		file_name = files[i]

		g2 = gt.load_graph(file_name)
		graph_name = file_name[:-3]+"png"
		json_name = file_name[:-3]+"json"
		
		if(auxTree.size_ring <= 3):
			vertex_basin = g2.vertex(0)
			pos = gt.radial_tree_layout(g2, vertex_basin , weighted=True)
			#pos =  gt.fruchterman_reingold_layout(g2, n_iter=100)
		else:
			pos = gt.sfdp_layout(g2, multilevel=True, max_level =auxTree.max_level)
			gt.graph_draw(g2, pos=pos,  output=graph_name)

		#make json
		f = open(json_name, 'w')
		f.write(auxTree.toJSON())
		f.close()

		#Make Histograma

		#fig, ax = plt.subplots()
		#keys = list(map (int, auxTree.frecuency.keys() ))
		#ax.bar(keys, list(auxTree.frecuency.values()) )
		#fig.savefig(hist_name)

		jsons.append(json_name)
		graph.append(graph_name)
		#hist.append(hist_name)

	return jsons, graph

fractales = [105]    
for f in fractales:
	#eca = None
	eca = ECA(f, length=20)
	#jsons, graph = AttractorFromSeed(eca, f, 1)
	jsons, graph = AttractorFromSeed(eca, f)
	print(jsons, graph)