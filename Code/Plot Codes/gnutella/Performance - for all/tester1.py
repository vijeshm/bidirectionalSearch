import numpy
import math
import AtoB
import matplotlib.pyplot as plt
import random
import networkx as nx
import pdb
import pickle

name = "gnutella"
trials = 100

G = nx.read_gpickle(str(name) + ".gpickle")
result = AtoB.comparison_query(G, trials)

ind = numpy.arange(4)
width = 0.15
plt.bar(ind, (result[0], result[1], result[2], result[3]), width)
plt.xticks(ind+width/2., ('One-way Random walk', 'Two-way Random walk', 'One-way Adamic walk', 'Two-way Adamic walk') )

plt.xlabel("Number of Nodes")
plt.ylabel("Average of (length of approx path / length of shortest path) over nC2 pairs")
#plt.title("Average time taken to compute the approximate shortest path for all the nC2 pairs")
plt.show()

#AtoB.createRealWorld(name)
#G = nx.read_gpickle(str(name) + ".gpickle")

#AtoB.simple_query(G)
#AtoB.comparison_query(G)
