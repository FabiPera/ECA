import numpy as np, math
from BitString import BitString
from ECA import ECA
from Simulation import Simulation

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

rule = 90
eca = ECA(rule, 2048)
eca.setInitConf("1", 0)

sim = Simulation(1024, eca)
sim.run()