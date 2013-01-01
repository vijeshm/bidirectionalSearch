import networkx as nx
import pickle

G = nx.Graph()

fin = open("p2p-Gnutella08.txt")
lines = fin.readlines()
lines.pop(0)
lines.pop(0)
lines.pop(0)
lines.pop(0)
print len(lines)
for line in lines:
	nodes = line.rsplit("\t")
	nodes[1] = nodes[1][:-2]
	G.add_edge(nodes[0], nodes[1])

print "Writing into file"
print G.number_of_nodes()
print G.number_of_edges()
string = pickle.dumps(G)
fout = open('gnutella.graph', 'w')
fout.write(string)
fout.close()
