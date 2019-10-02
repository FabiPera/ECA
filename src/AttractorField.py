#sys.path.append('/usr/local/Cellar/graph-tool/2.27_6/lib/python3.7/site-packages/graph_tool/')
import time
import gc 
from ECA import ECA
from Bitstring import Bitstring
import collections
import math
import json
import sys, os, os.path
import graph_tool.all as gt
import matplotlib.pyplot as plt

#import graph_tool.all as gt
#from graph_tool.all import *

# Nos permite crear data clases (strcut)
from dataclasses import dataclass

'''
@dataclass
class Atractor:
    """
    Clase que almacena un atractores y los atributos de este atractor.
    """
    entropy : float
    size_ring : int
    max_level : int


'''
class Atractor :
    """
    Clase que almacena un atractores y los atributos de este atractor.

    ...

    Attributes
    ----------
    entropy : float
        Entropia de los nodos de los arboles
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
    def __init__(self, arbol=[],entropy=0.,size_tree=0,size_ring=0, max_level = 0 , frecuency = {} ):
        self.entropy = entropy
        self.size_tree = size_tree
        self.size_ring = size_ring
        self.max_level = max_level
        self.frecuency = frecuency
        self.arbol = arbol
    def __hash__(self):
        return hash((self.size_tree,self.size_ring,self.max_level))
    def __eq__(self, other):
        return self.size_tree == other.size_tree and self.size_ring == other.size_ring and self.max_level == self.max_level
    def __str__(self):
        return "s_t_"+str(self.size_tree)+"s_r_"+str(self.size_ring)+"m_l_"+str(self.max_level)
    def toJSON(self):
        """
        data = {}
        data["entropy"] =self.entropy
        data ["size_tree"] = self.size_tree 
        data ["size_ring"]= self.size_ring
        data ["max_level"]=self.max_level
        data ["frecuency"]=self.frecuency
        data ["arbol"]=self.arbol
        return json.dumps()
        """
        return json.dumps(self, default=lambda o: o.__dict__,  sort_keys=True)


class basin :
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
    def __init__ (self, eca):
        self.eca = eca
        #self.rule = rule
        self.anillo = eca.l 
        self.evoluciones = {}
        self.field = []
        #Genera todas las evoluciones a -> b [b, a]
        
        #self.obtener_conjunto_arboles()
        '''
        arbol = self.obtener_arbol(1)
        #self.save_dot(arbol)
        
        
        self.field.append(arbol)
        self.evoluciones = self.generar_evoluciones()
        print("1\n")
        arbol2 = self.obtener_arbol(0)
        print(hash(arbol), hash(arbol2))
        print(arbol in self.field)
        print(arbol2 not in self.field)
        '''
        #print("arbol",arbol)

    """ Metodo que obtiene todo el espacio de evoluciones 
    """
    def generar_evoluciones(self):
        evoluciones = {}
        t0 = Bitstring( self.anillo )
        # 1.1 Recprre todas las posibles configuraciones [0, 2^anillo]
        for i in range(2**self.anillo):
            # convierte i a Bitstring 
            t0.bsFromInt(i)
            # Evoluciona la configuracion t0
            t1 = self.eca.evolve(t0)
            # Convierte el resultado a int 
            j = t1.binToInt()
            if j in evoluciones:
                evoluciones[j].append(i)
            else : 
                evoluciones[j]=[i]
            #evoluciones.append([j,i])
        evoluciones = collections.OrderedDict(sorted(evoluciones.items()))
        return evoluciones 
    def obtener_arbol_semilla(self,semilla):
        self.evoluciones = self.generar_evoluciones()
        print("1")
        arbol_aux = self.obtener_arbol(semilla)
        name_file = self.save_dot(arbol_aux)
        return arbol_aux , name_file

    def obtener_arbol_conjunto(self):
        self.evoluciones = self.generar_evoluciones()
        dots=[]
        print("1")
        
        #print( ( next(iter( self.evoluciones.keys())) )) 
        
        i = 0
        
        try:
            while True:

                #i = iterador.__next__()
                i = next(iter( self.evoluciones.keys() ) ) 
                #Como se eliminan los elementos, cada elemento en la
                # siguiente iteracion en el espacio pertenece a diferente arbol
                arbol_aux = self.obtener_arbol(i)
                # Verifica si el arbol no esta en el campo de atractores
                if arbol_aux not in  self.field:
                    self.field.append(arbol_aux)
                    dots.append(self.save_dot(arbol_aux) )      

        except StopIteration:
            pass
            #print("Se ha alcanzado el final de la lista")
        print("Total de arboles : ",len(self.field))
        return self.field , dots 

    # Metodo que obtiene el arbol de una configuracion
    # 1 ) Obtiene el atractor 
    # 2 ) Recorre todos los nodos del atractor
    #   2.0 ) Obtiene las preimagenes de cada nodo
    #   2.1 ) Recorre todos los nodos de las preimagenes  
    #       2.2 ) Agrega la preimagen al arbol
    #       2.3 ) Suma a la altura 1 
    def obtener_arbol(self, configuracion):
        
        # Bandera para mostrar si hay ancestros por visitat
        flag = True
        #Indoce que nos permite buscar los nodos no visitados
        i_k = 0
        # Indice que nos permite buscar el primer nodo del ultimo nivel
        _i_k = 0
        entropy = 0.0
        size_tree = 0
        size_ring = 0
        max_level = 0 
        frecuency = {}
        df = 0
        #arbol = arbol

        # 1 ) Obtiene el atractor 
        atractor = self.obtener_atractor(configuracion)
        
        # Guarda el tamanio del atractor 
        size_ring = len(atractor)
        #print(atractor)
        ##print(atractor)
        ##arboles = {}
        arboles = []
        # 2 ) Recorre todos los nodos del atractor para agregarlos al arbol, 
        for _n_atractor in atractor :
        #   2.0 ) Obtiene las preimagenes de cada nodo        
            preimagenes = self.evoluciones[_n_atractor]
            # Eliminar el elemento en el espacio de evoluciones
            del self.evoluciones [_n_atractor]
            
            
            ###preimagenes = self.obtener_preimagenes(_n_atractor)
            
            #agrega el elemento al arbol
            ##arboles[_n_atractor]= preimagenes
            arboles.append( [ _n_atractor, preimagenes])
            # Agrega la densidad del nodo a la frecuencia
            df = len(preimagenes)
            if df in frecuency:
                frecuency[df]=frecuency[df]+1
            else :
                frecuency[df]=1
            

        #print(arboles)
        #while true :
        #print(" Atractor : ",arboles)
        while flag:
            max_level += 1
            # Bandera que nos permite saber si al menos un nodo tiene una preimagen
            flag = False
            # Como se pueden agregar nuevos nodos se establece el limite actual 
            limite = len(arboles)
            ##keys = list(arboles.keys())
            #print(keys)
            # Igualamos el indice _i_k y el _i_k, como al final no entra el ciclo _i_k obtiene el ultimo nivel 
            _i_k = i_k
            for i in range (i_k, limite):
                # Obtiene el nodo del arbol a aprtir del indice que se esta recorriendo
                ##nodo = arboles[ keys[i] ]
                nodo = arboles [i]
                #print( "Nodo ", nodo)
                # recorre las preimagenes de ese nodo
                for _n_atractor in nodo[1] :
                    #print(" :",_n_atractor)
                    #####TEST
                    # Busca si aun no se ha visitado. 
                    #print(_n_atractor, atractor )
                    if _n_atractor in self.evoluciones :
                    #if _n_atractor not in atractor:    
                ####if self.buscar_espacio(_n_atractor) :
                        preimagenes  = self.evoluciones[_n_atractor]
                        del self.evoluciones[_n_atractor]
                        ###preimagenes = self.obtener_preimagenes(_n_atractor)
                        df = len(preimagenes)

                        if df != 0 :
                            flag = True
                            if df in frecuency:
                                frecuency[df]=frecuency[df]+1
                            else :
                                frecuency[df]=1
                            ##arboles[_n_atractor]= preimagenes
                        arboles.append( [_n_atractor, preimagenes] )
            # aumenta el indice a buscar 
                i_k +=1
            
            #gc.collect()
        #print(arboles)
        #hojas = self.obtener_jardin(arboles,_i_k)
        
        # Tamanio del arbol, que es el numero de nodos mas numero de hojas
        # Si nunca se movio el indice auxiliar significa que se ha encontrado un anoillo
        if _i_k == 0:
            size_tree = i_k
        else:
            df = self.obtener_len_jardin(arboles,_i_k) 
            size_tree = i_k+df
            max_level +=1
            frecuency[0]=df
        entropy = self.obtener_entropia(frecuency,size_tree)
        #frecuency = map(lambda x : x/size_tree, frecuency)
        #frecuency = list( map(lambda x : (x/size_tree)*math.log2(x/size_tree) , frecuency))
        '''
        print("size_ring",size_ring)
        print("size", size_tree)
        print("max_level",max_level)
        print("frecuency", frecuency)
        print("entropy",entropy)
        #print("Longitud", len(arboles))
        '''
        frecuency = dict(collections.OrderedDict(sorted(frecuency.items())))
        r = Atractor(arboles,entropy,size_tree, size_ring, max_level, frecuency)
        return r


    # Metodo que devuelve una lista de nodos que al que converge el nodo
    def obtener_atractor(self, i):
        atractor = []
        
        t0 = Bitstring(self.anillo)
        # convierte i a Bitstring 
        t0.bsFromInt(i)
        # Evoluciona la configuracion t0
        t1 = self.eca.evolve(t0)
        # Convierte el resultado a int 
        j = t1.binToInt()
        "Si el numero evoluciona a si mismo el ciclo es de longitud 0 "
        atractor.append (i)
        if (i == j):
            return atractor
        else :
            # Mientras la evolucion siguiente no este en el arreglo
            while j not in atractor :
                atractor.append(j)
                # convierte j en i para hacer la siguiente evolucion
                i = j
                # convierte i a Bitstring 
                t0.bsFromInt(i)
                # Evoluciona la configuracion t0
                t1 = self.eca.evolve(t0)
                # Convierte el resultado a int 
                j = t1.binToInt()
            # Obtener el indice donde esta el primer elemento del anilllo
            k = atractor.index(j)
            return atractor[k:]

    def obtener_jardin(self, arbol, k):
        jardines =  []
        for i in range (k, len(arbol)):
            jardines+=arbol[i][1]
        return jardines
    def obtener_len_jardin(self, arbol, k):
        jardines =  0
        for i in range (k, len(arbol)):
            jardines+=len(arbol[i][1])
        return jardines

    def obtener_entropia(self, frecuencia, size):
        entropy = 0.
        p = 0.
        for f in frecuencia:
            p = frecuencia[f]/size
            entropy+= p*math.log2(p)
        return -1*(entropy)
    "Metodo que guarda el arbol en archivo dot"
    def save_dot (self, arbol):
        data = arbol.arbol
        name = str(self.eca.r)+"_"+str(self.anillo)+"_"+str(arbol)+".dot"
        tf = open(name, 'w')
        tf.write("graph G {\n")
        for e in data:
            i = e[0]
            tf.write(str(i)+ ";\n" )
        for e in data :
            i = e[0]
            for j in e[1]:
                tf.write(str(i)+"--"+str(j)+";\n" )
    
        tf.write("\n}")
        tf.close()
        return name

"""
fractales = [26,94,154,164, 18,22,60,90, 122, 126, 105, 146, 150,106]
for i in fractales:
    b = basin (i,16)
    b.obtener_arbol_semilla(1)
print("--- %s seconds ---" % (time.time() - start_time))
"""
def Atractor_all(eca):
    b = basin (eca)
    arboles, files = b.obtener_arbol_conjunto()
    for i in range(len(arboles)):
        arbol_aux = arboles[i]
        file_name = files[i]
        g2 = gt.load_graph(file_name)
        graph_name = file_name[:-3]+"png"
        json_name = file_name[:-3]+"json"


def AtractorFromSeed(eca, seed = None ):
    
    jsons = []
    graph = []
    hist = []
    b = basin (eca)
    
    if seed == None :
        arboles, files = b.obtener_arbol_conjunto()
    else :
        arboles= []
        files = []
        arbol_aux , file_name = b.obtener_arbol_semilla(seed)
        arboles.append(arbol_aux)
        files.append(file_name)

    for i in range(len(arboles)):
        arbol_aux = arboles[i]
        file_name = files[i]
        
        g2 = gt.load_graph(file_name)
        graph_name = file_name[:-3]+"png"
        json_name = file_name[:-3]+"json"
        hist_name = file_name[:-4]+"-histograma.png"
        #make graph
        if arbol_aux.size_ring <= 3:
            vertex_basin = g2.vertex(0)
            pos = gt.radial_tree_layout( g2, vertex_basin , weighted=True)
            #pos =  gt.fruchterman_reingold_layout(g2, n_iter=100)
        else :
            pos = gt.sfdp_layout(g2,multilevel = True, max_level =arbol_aux.max_level )
        
        gt.graph_draw( g2 , pos = pos ,  output = graph_name)
        
        #make json
        f = open(json_name, 'w')
        f.write(arbol_aux.toJSON())
        f.close()

        #Make Histograma
        fig, ax = plt.subplots()
        keys = list(map (int, arbol_aux.frecuency.keys() ))
        ax.bar(keys, list(arbol_aux.frecuency.values()) )
        fig.savefig(hist_name)
        jsons.append(json_name)
        graph.append(graph_name)
        hist.append(hist_name)

        
    return jsons, graph, hist
fractales = [26,94,154,164, 18,22,60,90, 122, 126, 105, 146, 150,106]
for f in fractales:
    eca = None
    eca = ECA(f, l = 16)
    jsons, graph, hist = AtractorFromSeed(eca,1)
    print(jsons, graph, hist)