import numpy
import math
import AtoB
import matplotlib.pyplot as plt
import random
import networkx as nx
import pdb
import pickle

name = "gnutella"
trials = 10000

G = nx.read_gpickle(str(name) + ".gpickle")
result = AtoB.simple_query(G, trials)

print "The ratio of the time intervals taken to perform One-way Adamic walk and Two-way Adamic walk is " + str(float(result[0])/result[1])
print "Hence, Two-way Adamic walk is faster than One-way Adamic walk by a factor of " + str(float(result[1])/result[0])

ind = numpy.arange(2)
width = 0.15
plt.bar(ind, (result[0], result[1]), width)
plt.xticks(ind+width/2., ('One-way Adamic', 'Two-way Adamic') )

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
