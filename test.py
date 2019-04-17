import numpy as np
from numba import vectorize, int32
from timeit import default_timer as timer
from BitString import BitString
from ECA import ECA

"""
@vectorize([int32(int32, int32)], target="parallel")
def f(x, y):
    #for i in range(a.size):
    #    c[i]=x[i] + y[i]
    return x + y

a=np.ones(50000, dtype=np.int32)
b=np.ones(50000, dtype=np.int32)
#c=np.zeros(10000, dtype=np.int32)

#f(a, b, c)
c=f(a, b)
start=timer()
vt=timer() - start

print(c[0])
print(str(vt)+" seconds")

"""
#BitString test
print("Create BitString")
bitS=BitString(32)
print(bitS.bits)
print("Set BitString int value")
bitS.bsFromInt(36271939)
print(bitS.bits)
print(bitS.binToInt())

config=BitString(50)
dens=(50 * 50) // 100
config.bsFromRandomVal(dens)
print(config.bits)

configStr=BitString(10)
configStr.bsFromString("0111101010")
print(configStr.bits)

print("Create BitString")
bitS=BitString(32)

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