import igraph, cairocffi, random

class attractor:

	rule=[]
	sSize=0
	ad=[]
	gardens=[]

	def __init__(self, rule, sSize):
		self.rule=rule
		self.sSize=sSize
	
	def getNext(self, t0):
		t1=[]
		for x in range(self.sSize):
			neighbours=(t0[((x-1)%self.sSize)])*4+(t0[x])*2+(t0[((x+1)%self.sSize)])
			nextc=self.rule[neighbours]
			t1.append(nextc)
		return t1

	def setAd(self, t0, t1):
		t=(t0, t1)
		self.ad.append(t)

	def printAd(self):
		NewArchive=open("graph.txt", "w+")
		for y in range(len(self.ad)):
			row=self.ad[y]
			s=str(binToInt(row[0]))
			s+=" "
			s+=str(binToInt(row[1]))
			if y!=len(self.ad)-1:
				s+="\n"
			NewArchive.write(s)
		NewArchive.close()

	def plotGraph(self):
		vs=10
		if self.sSize>9:
			vs=2
		g=igraph.Graph.Read_Ncol("graph.txt", directed=False)
		igraph.plot(g, vertex_label=None, vertex_size=vs, width=5000, height=5000, target="graph.svg")

	def getGardens(self):
		for x in range(0, 2**sSize):
			n=intToBin(x, sSize)
			for y in range(len(self.ad)):
				garden=True
				if n==self.ad[y][1]:
					garden=False
					#print(n,"<->",self.ad[y][1])
					break
			if garden:
				print(n)
				self.gardens.append(n)

	def printGardens(self):
		if len(self.gardens)==0:
			print("No hay Jardines del Edén")
		else:
			for x in range(len(self.gardens)):
				print(self.gardens[x])


def listToString(li):
	string=""
	for x in range(len(li)):
		string+=str(li[x])
	return string

def intToBin(num, sSize):
	b=[]
	for i in range(sSize):
		b.append(num%2)
		num=num//2
	b.reverse()
	return b

def binToInt(num):
	num.reverse()
	n=0
	for x in range(len(num)):
		if num[x]==1:
			n+=2**x
	return n

def getRule(rule):
	b=[]
	for i in range(8):
		b.append(rule%2)
		rule=rule//2
	return b

print("Introduzca la regla: ")
rule=int(input())
print("Introduzca el tamaño de las cadenas: ")
sSize=int(input())
rule=getRule(rule)
att=attractor(rule, sSize)
for x in range(0, 2**sSize):
	n=intToBin(x, sSize)
	n1=att.getNext(n)
	att.setAd(n, n1)
print("Calculando atractor...")
att.printAd()
print("Graficando atractor...")
att.plotGraph()

