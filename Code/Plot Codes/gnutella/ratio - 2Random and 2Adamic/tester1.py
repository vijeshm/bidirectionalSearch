import numpy
import math
import AtoB
import matplotlib.pyplot as plt
import random
import networkx as nx
import pdb
import pickle

name = "gnutella"
trials = 100000

G = nx.read_gpickle(str(name) + ".gpickle")
result = AtoB.simple_query(G, trials)

print "The ratio of path lengths for Two-way Random walk and Two-way Adamic walk is " + str(float(result[0])/result[1])
print "Hence, Two-way Random walk is faster than Two-way Adamic walk by a factor of " + str(float(result[1])/result[0])

ind = numpy.arange(2)
width = 0.15
plt.bar(ind, (result[0], result[1]), width)
plt.xticks(ind+width/2., ('Two-way Random walk', 'Two-way Adamic walk') )

plt.xlabel("Number of Nodes")
plt.ylabel("Average of (length of approx path / length of shortest path) over nC2 pairs")
#plt.title("Average time taken to compute the approximate shortest path for all the nC2 pairs")
plt.show()



#AtoB.createRealWorld(name)
#G = nx.read_gpickle(str(name) + ".gpickle")

#AtoB.simple_query(G)
#AtoB.comparison_query(G)
