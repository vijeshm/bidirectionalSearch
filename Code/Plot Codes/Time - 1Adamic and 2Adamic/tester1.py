import numpy
import math
import AtoB
import matplotlib.pyplot as plt
import random
import networkx as nx
import pdb
import pickle

#n = 200
edgeProb = 0.3
degree = 3

#name = "gnutella"
#trials = 10000

start = 100
end = 401
step = 20

x = []
plainAdamic = []
twoWayAdamic = []
for n in range(start, end, step):
	AtoB.createScaleFreeNetwork(n, degree)	
	G = nx.read_gpickle("SFN_" + str(n) + "_" + str(degree) + ".gpickle")

	result = AtoB.simple_query(G)
	plainAdamic.append(result[0])
	twoWayAdamic.append(result[1])
	x.append(n)

plt.plot(x, plainAdamic)
plt.plot(x, twoWayAdamic)
plt.xlabel("Number of Nodes")
plt.ylabel("Time Taken")
plt.title("Average time taken to compute the approximate shortest path for all the nC2 pairs")
plt.show()

#AtoB.createErdos(n,edgeProb)
#G = nx.read_gpickle("EG_" + str(n) + "_" + str(edgeProb) + ".gpickle")

#AtoB.createRealWorld(name)
#G = nx.read_gpickle(str(name) + ".gpickle")

#AtoB.simple_query(G)
#AtoB.comparison_query(G)
