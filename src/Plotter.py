import numpy as np, matplotlib.pyplot as plt, copy, math


def plotDensity(dens, strLength, path):
	plt.figure("Density")
	plt.title("Density")
	plt.ylabel("% of cells with state 1")
	plt.xlabel("Step of time")
	plt.axis([0, len(dens), 0, 100])
	plt.yticks(np.arange(0, 110, 10))
	plt.plot(dens, "m,-")
	plt.savefig(path + "SimDensity.png")
	plt.clf()

def plotEntropy(entropy, path):
	plt.figure("Entropy")
	plt.title("Entropy")
	plt.ylabel("Topological Entropy")
	plt.xlabel("Step of time")
	plt.axis([0, len(entropy), 0, 1])
	plt.yticks(np.arange(0, 1.1, 0.1))
	plt.plot(entropy, "m,-")
	plt.savefig(path + "SimEntropy.png")
	plt.clf()