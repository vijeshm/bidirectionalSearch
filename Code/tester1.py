import numpy
import math
import AtoB
import matplotlib.pyplot as plt
import random
import networkx as nx
import pdb
import pickle

n = 200
edgeProb = 0.3
degree = 3

name = "gnutella"
trials = 10000

#AtoB.createErdos(n,edgeProb)
#G = nx.read_gpickle("EG_" + str(n) + "_" + str(edgeProb) + ".gpickle")

#AtoB.createScaleFreeNetwork(n, degree)	
#G = nx.read_gpickle("SFN_" + str(n) + "_" + str(degree) + ".gpickle")

#AtoB.createRealWorld(name)
G = nx.read_gpickle(str(name) + ".gpickle")

AtoB.simple_query(G, trials)
#AtoB.comparison_query(G)
