import numpy as np, math, cairo, copy
from Bitstring import Bitstring
from Simulation import *
from Analysis import *
#from Plotter import *

"""
#Bitstring test
print("Create Bitstring")
bitS=Bitstring(32)
print(bitS.bits)
print("Set Bitstring int value")
bitS.bsFromInt(36271939)
print(bitS.bits)
print(bitS.binToInt())

config=Bitstring(50)
dens=(50 * 50) // 100
config.bsFromRandomVal(dens)
print(config.bits)

configStr=Bitstring(10)
configStr.bsFromString("0111101010")
print(configStr.bits)

print("Create Bitstring")
bitS=Bitstring(32)
"""

"""
#ECA test
print("Create ECA")
eca=ECA(94, 512, 1024)
eca.setT0("11111", 0)
print(eca.seedConfig)
eca.dmgPos=511
#eca.dmgPos=510
#eca.dmgPos=511
#eca.dmgPos=512
#eca.dmgPos=513
#eca.setDamage()
print(eca.rule)
#eca.createSimScreen(eca.seedConfig.length*2, eca.steps*2)
for i in range(eca.steps):
	for j in range(eca.t0.length):
		if (eca.t0.bits[j] ^ eca.tDam.bits[j]):
			eca.damageFreq[j] += 1
	
	#if (i > 0):
	#	lyapN=eca.countDefects()
	#	lyapExp=eca.getLyapunovExp(1, lyapN)
		#print(lyapExp)

	eca.drawConfiguration(y=i, bitStr=eca.t0, dmgBitstr=eca.tDam)
	#eca.getTopEntropy(3)
	#print(eca.tDam)
	eca.t0=copy.deepcopy(eca.evolve(eca.t0))
	eca.tDam=copy.deepcopy(eca.evolve(eca.tDam))
	#print(eca.hX)

eca.saveToPNG("Simulation18Dam5.png")
"""
"""
def trinomialValue(n, k): 
	if(n == 0 and k == 0): 
		return 1
		
	if(k < -n or k > n): 
		return 0
	
	return(trinomialValue (n - 1, k - 1) + trinomialValue (n - 1, k) + trinomialValue (n - 1, k + 1))

def trinomial(kn, prev=np.ones(1, dtype=int)):
	if(len(prev) == 1):
		return np.ones(3, dtype=int)
	
	else:
		current=np.ones((len(prev) + 2), dtype=np.uint)
		currentmid=len(current) // 2
		prevmid=len(prev) // 2
		for i in range(kn):
			pointer1=prevmid - i
			pointer2=prevmid + i
			if(pointer1 == pointer2):
				current[currentmid]=prev[prevmid - 1] + prev[prevmid] + prev[prevmid + 1]
			else:
				if((pointer1 - 1) >= 0):
					current[currentmid - i]=prev[prevmid - i - 1] + prev[prevmid - i] + prev[prevmid - i + 1]
					current[currentmid + i]=current[currentmid - i]
				else:
					current[currentmid - i]=prev[prevmid - i] + prev[prevmid - i + 1]
					current[currentmid + i]=current[currentmid - i]
		return current

row=np.ones(1, dtype=np.uint)
n=input()
print(row)
for i in range(int(n)):
	row=trinomial((i + 1), row)
	print(row)

mid=len(row) // 2
print(row[mid])
print((1 / (int(n) - 1)) * (math.log(row[mid])))
#print(trinomialValue(63, 0))
"""
"""
bs=Bitstring(8)
bs.bsFromInt(10)
print(bs.binToInt())
"""

"""
pixels = 1
width = 1001
height = 500

eca = ECA(90, width)
eca.setConf("1", 0)
xp = Bitstring(1001)
sim = Simulation(eca, 500)
sim.runSimulation(xp)
"""

"""
t = copy.deepcopy(eca.x)

surface = cairo.ImageSurface(cairo.FORMAT_RGB24, width, height)
context = cairo.Context(surface)
context.rectangle(0, 0, width, height)
context.set_source_rgb(0.62, 0.62, 0.62)
context.fill()

x = pixels
y = pixels

for i in range(height):
	for j in range(width):
		if(t.bits[j]):
			context.rectangle(x, y, pixels, pixels)
			context.set_source_rgb(0, 0, 0)
			context.fill()
		else:
			context.rectangle(x, y, pixels, pixels)
			context.set_source_rgb(1, 1, 1)
			context.fill()
		x += pixels
	x = pixels
	y += pixels
	t = copy.deepcopy(eca.evolve(t))
	
surface.write_to_png("../img/preview.png")

"""

"""
while(y < (height - pixels)):
	while(x < (width - pixels)):
		if(x < (width - pixels)):
			context.rectangle(x, y, pixels, pixels)
			context.set_source_rgb(0, 0, 0)
			context.fill()
			x += pixels
		else:
			break
		if(x < (width - pixels)):
			context.rectangle(x, y, pixels, pixels)
			context.set_source_rgb(1, 1, 1)
			context.fill()
			x += pixels
		else:
			break
		if(x < (width - pixels)):
			context.rectangle(x, y, pixels, pixels)
			context.set_source_rgb(1, 0, 0)
			context.fill()
			x += pixels
		else:
			break

	x = pixels
	y += (2 * pixels)
"""

"""
for i in range(75):
	for j in range(150):
		if(x.bits[j]):
			context.rectangle(j, i, 1, 1)
			context.set_source_rgb(0, 0, 0)
			context.fill()
		else:
			context.rectangle(j, i, 1, 1)
			context.set_source_rgb(1, 1, 1)
			context.fill()
	x = copy.deepcopy(eca.evolve(x))

#context.rectangle(60, 179, 10, 10)
#context.set_source_rgb(1, 0, 0)
#context.fill()

"""
"""
width = 1001
height = 500

eca = ECA(90, width)
eca.setConf("1", 0)
settings = SimSettings()

simulation = Simulation(eca)

simulation.runSimulation()
"""

analysis = Analysis()
for i in range(32):
	print((len(analysis.ttrow) * 2) - 1)
	analysis.getTrinomialRow(analysis.ttrow)

analysis.getTrinomialRow(analysis.ttrow)
x = (1 / 33) * (math.log(analysis.ttrow[0]))	
print(x)