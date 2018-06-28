import sys, pygame, random, matplotlib.pyplot as plt, numpy as np
from pygame.locals import *

color_cell=(45,45,45)
color_background=(255,255,255)
sy=0

class celAut:

	rule=[]
	cells=0
	gens=0
	oFreq=0
	den=0

	def __init__(self, rule, cells, gens):
		self.rule=rule
		self.cells=cells
		self.gens=gens
		self.t0=[]
		self.t1=[]

	def setRandomFirstGen(self, dens):
		d=0
		for i in range(self.cells):
			n=random.randint(0, self.cells)
			x=n%2
			if x==1:
				self.t0.append(1)
				self.oFreq+=1
				d+=1
			else:
				self.t0.append(0)
				
		while self.oFreq>=dens:
			n=random.randint(0, self.cells-1)
			if self.t0[n]==1:
				self.t0[n]=0
				self.oFreq-=1
			
		print(self.oFreq)

	def setOneCellFirstGen(self):
		self.oFreq=1
		x=self.cells//2
		for i in range(self.cells):
			if i==x:
				self.t0.append(1)
			else:
				self.t0.append(0)

	def setStringFirstGen(self, s0):
		for x in range(len(s0)):
			if s0[x]=='1':
				self.t0.append(1)
				self.oFreq+=1
			else:
				self.t0.append(0)

	def getNextGen(self):
		self.oFreq=0
		for i in range(self.cells):
			d=(self.t0[((i-1)%self.cells)])*4+(self.t0[i])*2+(self.t0[((i+1)%self.cells)])
			nc=self.rule[d]
			if nc:
				self.oFreq+=1
			self.t1.append(nc)
		self.t0=self.t1
		self.t1=[]


def update_screen(gen):
	global sy
	x=0
	for elem in gen:
		if elem:
			screen.fill(color_cell, (x, sy, 5, 5))
		else:
			screen.fill(color_background, (x, sy, 5, 5))
		x+=5
	sy+=5

def init(rule, w, h):
	global background, screen
	pygame.init()
	screen=pygame.display.set_mode((w*5, h*5))
	pygame.display.set_caption("Regla "+str(rule))
	screen.fill(color_background)

def getRule(rule):
	b=[]
	for i in range(8):
		b.append(rule%2)
		rule=rule//2
	return b

def saveAut():
	pygame.image.save(screen, "evolution.png")
	print("Simulación guardada")

def showAut():
	while 1:
		for event in pygame.event.get():
			if event.type==pygame.QUIT:
				pygame.quit()
				sys.exit()
		pygame.display.flip()

def getAv(freq, gens):
	av=0
	for x in range(gens):
		av+=freq[x]
	av/=gens
	return av

def getVar(av, freq, gens):
	av2=0
	for x in range(gens):
		av2+=freq[x]**2
	av2/=gens
	var=av2-av**2
	return var

print("1 Random")
print("2 Una célula")
print("3 Cadena")
option=int(input())
print("Introduzca regla")
rule=int(input())
rulea=getRule(rule)
cells=0

if option==3:
	print("Introduzca cadena")
	firstGen=input()
	print("Cuantas generaciones?")
	gens=int(input())
	cells=len(firstGen)
	aut=celAut(rulea, cells, gens)
	aut.setStringFirstGen(firstGen)
else:
	print("Cuantas células?")
	cells=int(input())
	print("Cuantas generaciones?")
	gens=int(input())
	aut=celAut(rulea, cells, gens)

	if option==1:
		print("Introduzca su densidad")
		dens=int(input())
		densC=dens*aut.cells
		densC=densC//100
		aut.setRandomFirstGen(densC)
	elif option==2:
		aut.setOneCellFirstGen()
	else:
		print("Opción incorrecta")

init(rule, cells, gens)
avO=[]
print("Calculando evoluciones...")
for y in range(aut.gens):
	update_screen(aut.t0)
	aut.getNextGen()
	pygame.display.flip()
	avO.append(aut.oFreq)

saveAut()
"""	
plt.ion()
a=np.arange(gens)
plt.bar(a, height=avO)
gs=[str(x+1) for x in range(gens)]
plt.xticks(a, gs)
av=getAv(avO, gens)
print("Calculando media...")
print("Media=",av)
var=getVar(av, avO, gens)
print("Calculando varianza...")
print("Varianza=",var)
"""
showAut()

