import numpy as np, copy, math, matplotlib.pyplot as plt, csv
from BitString import BitString
from ECA import ECA

def getStrProb(strl, eca):
	numOfStr=2 ** strl
	ad=[]
	bs=BitString(strl)
	for i in range(numOfStr):
		node=[]
		node.append(str(i))
		bs.bsFromInt(i)
		bs=eca.evolve(bs)
		nextState=bs.binToInt()
		node.append(str(nextState))
		ad.append(node)

	with open("graph.csv", "w") as csvfile:
		filewriter=csv.writer(csvfile, delimiter=",", quotechar="|", quoting=csv.QUOTE_MINIMAL)
		filewriter.writerow(['From', 'To'])
		for x in range(numOfStr):
			filewriter.writerow(ad[x])
    

eca=ECA(90, 20)
getStrProb(20, eca)