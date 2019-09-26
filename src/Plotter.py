import numpy as np, matplotlib.pyplot as plt, copy, math


def plotDensity(dens, strLength):
	plt.figure("Density")
	plt.title("Density")
	plt.ylabel("Cells with state 1")
	plt.xlabel("Step of time")
	plt.axis([0, len(dens), 0, 100])
	plt.plot(dens, "m,-")
	plt.savefig("../sim/SimDensity.png")
	plt.clf()

def plotEntropy(entropy):
	plt.figure("Entropy")
	plt.title("Entropy")
	plt.ylabel("Topological Entropy")
	plt.xlabel("Step of time")
	plt.axis([0, len(entropy), 0, 1])
	plt.plot(entropy, "m,-")
	plt.savefig("../sim/SimEntropy.png")
	plt.clf()