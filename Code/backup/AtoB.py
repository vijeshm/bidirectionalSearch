import matplotlib.pyplot as plt
import random
import networkx as nx
import math
import numpy
import pdb
import pickle
import time 
import bisect
import sys
import copy

#Actual Algorithm starts here. Previous Modules are used for analysis purposes.

Degree_Node = None
NodeList = None

def removeCycles(Path):
	'''
	Given a path, this function removes all the cycles and returns the acyclic path
	'''
	i = 0 #i is the walker
	while i < len(Path): #the length of the path keeps on decreasing as the control flow of the program progresses
		for j in range(len(Path) - 1, i,-1): #move j from the last position to the (i+1)th position, when the path[i] and path[j] are the same, this indicates a cycle. Hence, remove the nodes in between them (inclusive of either end).
			if Path[j] == Path[i]:
				del(Path[i:j])
				break
		i += 1
	return Path

def createPath(pathA, pathB, hit):
	'''
	pathA: drunkard WALK starting from A
	pathB: drunkard WALK starting from B
	hit: the point at which hit has occured.
	Given two paths pathA and pathB and the intersection point hit, then this function integrates them into a path and returns the path. This path may contain cycles and must be removed.
	'''
	Path = []

	Path.extend(pathA[:pathA.index(hit)]) #calculate the index of the hit point and append the nodes in pathA to Path, excluding the hit point
	Path.extend(pathB[pathB.index(hit)::-1]) #calculate the index of the hit point and append the nodes in pathB to Path, including the hit point and IN REVERSE DIRECTION
	return Path

def createRealWorld(name):
	'''
	name: The name of the real world graph
	This function creates a .graph file from a .gml file, and runs the machine learning alogorithm on it.
	'''	
	print "Generating and Saving RealWorld Graph..."	
	G = nx.read_gml(name + ".gml")
	print name + ".gml" + " file read"
	StrMap = {}
	for node in G.nodes():
		StrMap[node] = str(node)
	G = nx.convert.relabel_nodes(G,StrMap)
	nx.write_gpickle(G,str(name) + '.gpickle')
	print "Successfully written into " + name

def createScaleFreeNetwork(numOfNodes, degree):
	'''
	numOfNodes: The number of nodes that the scale free network should have
	degree: The degree of the Scale Free Network
	This function creates a Scale Free Network containing 'numOfNodes' nodes, each of degree 'degree'
	It generates the required graph and saves it in a file. It runs the Reinforcement Algorithm to create a weightMatrix and an ordering of the vertices based on their importance by Flagging.
	'''
	print "Generating and Saving ScaleFree Network..."	
	G = nx.barabasi_albert_graph(numOfNodes, degree) #Create a Scale Free Network of the given number of nodes and degree
	StrMap = {}
	for node in G.nodes():
		StrMap[node] = str(node)
	G = nx.convert.relabel_nodes(G,StrMap)
	filename = "SFN_" + str(numOfNodes) + "_" + str(degree) + '.gpickle' 
	nx.write_gpickle(G,filename) #generate a gpickle file of the learnt graph.
	print "Successfully written into " + filename

def createErdos(numOfNodes, edgeProb):
	'''
	numOfNodes: The number of nodes that the Eldish graph will have
	edgeProb: The probability of existance of an edge between any two vertices
	This function creates an Erdos Graph containing 'numOfNodes' nodes, with the probability of an edge existing between any two vertices being 'edgeProb'
	It generates the required graph and saves it in a file. It runs the Reinforcement Algorithm to create a weightMatrix and an ordering of the vertices based on their importance.
	'''
	print "Generating and Saving Erdos Network..."	
	G = nx.erdos_renyi_graph(numOfNodes, edgeProb) #Creates an Eldish Graph of the given number of nodes and edge Probability
	if nx.is_connected(G):
		StrMap = {}
		for node in G.nodes():
			StrMap[node] = str(node)
		G = nx.convert.relabel_nodes(G,StrMap)

		filename = "EG_" + str(numOfNodes) + "_" + str(edgeProb) + ".gpickle"
		nx.write_gpickle(G,filename) #generate a gpickle file of the learnt graph.
		print "Successfully written into " + filename
		

def createBridge(numOfNodes, edgeProb, bridgeNodes):
	'''
	numOfNodes: Number of nodes in the clustered part of the Bridge Graph
	edgeProb: Probability of existance of an edge between any two vertices.
	bridgeNodes: Number of nodes in the bridge
	This function creates a Bridge Graph with 2 main clusters connected by a bridge.
	'''	
	print "Generating and Saving Bridge Network..."	
	G1 = nx.erdos_renyi_graph(2*numOfNodes + bridgeNodes, edgeProb) #Create an ER graph with number of vertices equal to twice the number of vertices in the clusters plus the number of bridge nodes.
	G = nx.Graph() #Create an empty graph so that it can be filled with the required components from G1
	G.add_edges_from(G1.subgraph(range(numOfNodes)).edges()) #Generate an induced subgraph of the nodes, ranging from 0 to numOfNodes, from G1 and add it to G
	G.add_edges_from(G1.subgraph(range(numOfNodes + bridgeNodes,2*numOfNodes + bridgeNodes)).edges()) #Generate an induced subgraph of the nodes, ranging from (numOfNodes + bridgeNodes) to (2*numOfNodes + bridgeNodes)

	A = random.randrange(numOfNodes) #Choose a random vertex from the first component
	B = random.randrange(numOfNodes + bridgeNodes,2*numOfNodes + bridgeNodes) #Choose a random vertex from the second component

	prev = A #creating a connection from A to B via the bridge nodes
	for i in range(numOfNodes, numOfNodes + bridgeNodes):
		G.add_edge(prev, i)
		prev = i
	G.add_edge(i, B)
	
	StrMap = {}
	for node in G.nodes():
		StrMap[node] = str(node)
	G = nx.convert.relabel_nodes(G,StrMap)
	filename = "BG_" + str(numOfNodes) + "_" + str(edgeProb) + "_" + str(bridgeNodes) + ".gpickle"
	nx.write_gpickle(G,filename)#generate a gpickle file of the learnt graph.
	print "Successfully written into " + filename

def simple_query(GLearnt):
	i = 1
	
	global Degree_Node
	global NodeList

	G = nx.Graph(GLearnt)
	Degree_Node = G.degree()
	NodeList = G.nodes()

	for i in NodeList:
		Degree_Node[i] = [Degree_Node[i], GLearnt.neighbors(i)]

	PlainAdamicFullPaths = []

	djk_time = 0
	PlainAdamic_time = 0
	
	total = len(NodeList) * ( len(NodeList) - 1 )/2


	count = 0
	for A in NodeList:
		for B in NodeList[NodeList.index(A):]:
		    if A != B :	
			src = A #raw_input("Enter source name:")
			dstn = B #raw_input("Enter destination name:")

			start = time.time()
			PlainAdamicFullPath = TwoWayAdamicWalk(G,src,dstn)
			finish = time.time()
			PlainAdamic_time+=(finish-start)

			start = time.time()
			ShortestPath = nx.shortest_path(GLearnt, src, dstn)
			finish = time.time()
			djk_time+=finish-start

			PlainAdamicFullPaths.append(float(len(PlainAdamicFullPath))/len(ShortestPath))

			count += 1
	                sys.stdout.write("\b"*50) 
			sys.stdout.write( "Progress: " + str(float(count)/total))
	                
	print "\nAvg of PlainAdamicFullPaths :" , numpy.average(PlainAdamicFullPaths)
	print "adamic time : " ,PlainAdamic_time
	
	print "djk time : ",djk_time
	print "PlainAdamic_time/djk_time:", PlainAdamic_time / djk_time
	

def comparison_query(GLearnt):
	i = 1
	
	global Degree_Node
	global NodeList

	G = nx.Graph(GLearnt)
	Degree_Node = G.degree()
	NodeList = G.nodes()

	for i in NodeList:
		Degree_Node[i] = [Degree_Node[i],GLearnt.neighbors(i)]	

	RandomWalk_OneWay_Paths = []
	RandomWalk_TwoWay_Paths = []
	PlainAdamic_OneWay_Paths = []
	PlainAdamic_TwoWay_Paths = []

	RandomWalk_OneWay_time = 0
	RandomWalk_TwoWay_time = 0
	PlainAdamic_OneWay_time = 0
	PlainAdamic_TwoWay_time = 0

	djk_time = 0

	total = (len(NodeList) * (len(NodeList)-1))/2
	
	average_twowaywalk = 0
	average_onewaywalk = 0
	
	count = 0
	for A in NodeList:
		for B in NodeList[NodeList.index(A):]:
		    if(A!=B):
			src = A#raw_input("Enter source name:")
			dstn = B#raw_input("Enter destination name:")

			start = time.time()
			RandomWalk_OneWay = OneWayRandomWalk(G,src,dstn)
			finish = time.time()
			RandomWalk_OneWay_time+=(finish-start)

			start = time.time()
			RandomWalk_TwoWay = TwoWayRandomWalk(G,src,dstn)
			finish = time.time()
			RandomWalk_TwoWay_time+=(finish-start)
			

			start = time.time()
			PlainAdamic_OneWay = OneWayAdamicWalk(G,src,dstn)
			average_onewaywalk+=len(PlainAdamic_OneWay)
			finish = time.time()
			PlainAdamic_OneWay_time+=(finish-start)

			start = time.time()
			PlainAdamic_TwoWay = TwoWayAdamicWalk(G,src,dstn)
			average_twowaywalk+=len(PlainAdamic_TwoWay)
			finish = time.time()
			PlainAdamic_TwoWay_time+=(finish-start)


			start = time.time()
			ShortestPath = nx.shortest_path(G, src, dstn)
			finish = time.time()
			djk_time+=finish-start

			RandomWalk_OneWay_Paths.append(float(len(RandomWalk_OneWay))/len(ShortestPath))
			RandomWalk_TwoWay_Paths.append(float(len(RandomWalk_TwoWay))/len(ShortestPath))
			PlainAdamic_OneWay_Paths.append(float(len(PlainAdamic_OneWay))/len(ShortestPath))			
			PlainAdamic_TwoWay_Paths.append(float(len(PlainAdamic_TwoWay))/len(ShortestPath))
			count+=1
	                sys.stdout.write("\b"*50) 
			sys.stdout.write( "Progress: " + str(float(count)/total))
	                
	print "\nAvg of One way Random Walk to Shortest Path :" , numpy.average(RandomWalk_OneWay_Paths)	
	print "Avg of Two way Random Walk to Shortest Path :" , numpy.average(RandomWalk_TwoWay_Paths)
	print "Avg of One way Degree Based walk to Shortest Path :" , numpy.average(PlainAdamic_OneWay_Paths)
	print "Avg of Two way Degree based walk to Shortest Path :" , numpy.average(PlainAdamic_TwoWay_Paths)
			
	print "\nOne Way Random Walk time : " , RandomWalk_OneWay_time
	print "Two Way Random Walk time : " , RandomWalk_TwoWay_time 
        print "One Way Degree based Walk time : " , PlainAdamic_OneWay_time
	print "Two Way Degree based Walk time : " , PlainAdamic_TwoWay_time
	print "djk time : ",djk_time
	
	print "\nPerformance: One Way Random Walk time : " , 1 / (numpy.average(RandomWalk_OneWay_Paths) * RandomWalk_OneWay_time)
	print "Performance: Two Way Random Walk time : " , 1 / (numpy.average(RandomWalk_TwoWay_Paths) * RandomWalk_TwoWay_time)
        print "Performance: One Way Degree based Walk time : " , 1 / (numpy.average(PlainAdamic_OneWay_Paths) * PlainAdamic_OneWay_time)
	print "Performance: Two Way Degree based Walk time : " , 1 / (numpy.average(PlainAdamic_TwoWay_Paths) * PlainAdamic_TwoWay_time)
	print "djk time : ",djk_time
	
	print "Average of one way adamic walk : ", average_onewaywalk*1.0/total
	print "Average of two way adamic walk : ", average_twowaywalk*1.0/total
	
	#return (numpy.average(RandomWalk_OneWay_Paths),numpy.average(RandomWalk_TwoWay_Paths), numpy.average(PlainAdamic_OneWay_Paths), numpy.average(PlainAdamic_TwoWay_Paths))
	return (RandomWalk_OneWay_time, RandomWalk_TwoWay_time, PlainAdamic_OneWay_time, PlainAdamic_TwoWay_time)
	
#---------------------------------------------------------------------------------------------------------------------------------------------------
def OneWayRandomWalk(G,src,dstn):
	walker = src #walkers(robots) that take a random walk from given vertices
	path = []
	path.append(src) #actual paths that the walkers take

	while( True ):
		walkerAdj = G.neighbors(walker) #Adjacent vertices for current vertex
		rand = random.choice(walkerAdj) #select one node from the set of neighbors of walkerA and walkerB and assign them 
		path.append(rand) #add the randomly selected edge to the set
		walker = rand

		if dstn == rand :
			#path = removeCycles(path)
			return path
			
#--------------------------------------------------------------------------------------------------------------------------------------------------

def findHit(G, A, B, pathA, pathB):
	'''
	G: Graph which is undergoing machine learning
	A: Vertex #1
	B: Vertex #2
	pathA: contains the drunkard walk starting from A
	pathB: contains the drunkard walk starting from B
	Takes 2 vertices A and B from a graph G. Takes a random walk starting from A and takes another random walk starting from B and simultaneously builds the paths. If an intersection is found, the path is established and the corresponding intersection is returned. pathA and pathB are also dynamically updated.
	'''
	walkerA = A #walkers(robots) that take a random walk from given vertices
	walkerB = B

	pathA.append(A) #actual paths that the walkers take
	pathB.append(B)

	while( True ):
		walkerAAdj = G.neighbors(walkerA) #Adjacent vertices for current vertex
		
		walkerBAdj = G.neighbors(walkerB)
		
		randA = random.choice(walkerAAdj) #select one node from the set of neighbors of walkerA and walkerB and assign them to randA and randB respectively
		randB = random.choice(walkerBAdj)
		
		pathA.append(randA) #add the randomly selected edge to the set
		if randA not in pathB: #if randA is already in pathB, then the intersection has occured and there is no need to append randB to pathB. If we append randB to pathB, then there is a chance that we might get two intersection points if randB is also in pathA.
			pathB.append(randB)

		if (randA not in pathB and randB not in pathA): #If the sets are disjoint, then there is no common point that both the walkers now. So, proceed one step further for the next loop
			walkerA = randA
			walkerB = randB
		else:
			break #this implies that the intersection has occured and the infinite while loop should exit. Now, pathA and pathB are the components of the 2-Raw Random Walk

	if pathA[-1] in pathB: #if the last element of pathA is in pathB, then randA must have been the intersection point. Hence, set hit = randA = pathA[-1]
		hit = pathA[-1]
	else:
		hit = pathB[-1] #if the last element of pathB is in pathA, then randB must have been the intersection point. Hence, set hit = randB = pathB[-1]

	return hit

def createPath(pathA, pathB, hit):
	'''
	pathA: drunkard WALK starting from A
	pathB: drunkard WALK starting from B
	hit: the point at which hit has occured.
	Given two paths pathA and pathB and the intersection point hit, then this function integrates them into a path and returns the path. This path may contain cycles and must be removed.
	'''
	Path = []

	Path.extend(pathA[:pathA.index(hit)]) #calculate the index of the hit point and append the nodes in pathA to Path, excluding the hit point
	Path.extend(pathB[pathB.index(hit)::-1]) #calculate the index of the hit point and append the nodes in pathB to Path, including the hit point and IN REVERSE DIRECTION
	return Path

def TwoWayRandomWalk(G,A,B):
	'''
	A: Vertex #1
	B: Vertex #2
	This function takes in 2 vertices A and B in a graph G. It finds a path from A to B through the method of random walks. It returns the path and the intersection node of the random walk. 
	'''
	pathA = []
	pathB = []
	hit = findHit(G, A, B, pathA, pathB) #Take a random walk and stop when an intersection occurs. Return the intersection point.
	Path = createPath(pathA, pathB, hit) #Create a path from A to B. This path may contain cycles too.
	#Path = removeCycles(Path) #Remove all the cycles from the current path.
	return Path
#---------------------------------------------------------------------------------------------------------------------------------------------------

def OneWayAdamicWalk(G,src,dstn):
	path = []
	global Degree_Node

	Flagger = {}
	path.append(src)
	a = src

	while True :
		maxdegree = -1
		maxnode = None
		neighbors = G.neighbors(a)#copy.deepcopy(Degree_Node[a][1])
		i = None		
		for i in neighbors:
			if(maxdegree<Degree_Node[i][0]):
				maxdegree=Degree_Node[i][0]
				maxnode=i
		i = maxnode
		while Flagger.has_key(maxnode):
			try:
				maxnode = neighbors.pop() #the neighbor with the next highest degree is NOT being chosen here.
			except IndexError:
				maxnode = i
				k_hop = 2	
				while k_hop > 0:
					neighbors = G.neighbors(maxnode)#copy.deepcopy(Degree_Node[maxnode][1])
					maxnode = random.choice(neighbors)
					path.append(maxnode)
					k_hop-=1
					if (k_hop == 0) :
						if (Flagger.has_key(maxnode)):
							k_hop = 2		
				path.pop()

		path.append(maxnode)
		Flagger[maxnode] = 1 
		a = maxnode
		if Flagger.has_key(dstn):
			return path
	
#---------------------------------------------------------------------------------------------------------------------------------------------------

def TwoWayAdamicWalk(G,a,b):
	path_a = []
	path_b = []
	hit = adamicwalk(G,a,b,path_a,path_b)
	return createPath(path_a, path_b, hit)		
		
def adamicwalk(G,a,b,path_a,path_b):
	global Degree_Node	

	path_a.append(a)
	path_b.append(b)		

	Flagger_a = {}
	Flagger_a[a]=1

	Flagger_b= {} 
	Flagger_b[b]=1 

	while True :
		maxdegree = -1
		maxnode = None
		neighbors_a = G.neighbors(a)#copy.deepcopy(Degree_Node[a][1])
		i = None
		for i in neighbors_a:
			if(maxdegree<Degree_Node[i][0]):
				maxdegree=Degree_Node[i][0]
				maxnode=i
		i = maxnode
		while Flagger_a.has_key(maxnode):
			try:
				maxnode = neighbors_a.pop() #the neighbor with the next highest degree is NOT being chosen here.
			except IndexError:
				maxnode = i
				k_hop = 2	
				while k_hop > 0 : 
					neighbors_a = G.neighbors(maxnode)#copy.deepcopy(Degree_Node[maxnode][1])
					maxnode = random.choice(neighbors_a)
					path_a.append(maxnode)
					k_hop-=1
					if (k_hop == 0) :
						if (Flagger_a.has_key(maxnode)):
							k_hop = 2			
				path_a.pop()
		path_a.append(maxnode)
		Flagger_a[maxnode] = 1 
		
		if Flagger_b.has_key(maxnode):
			return maxnode

		a = maxnode

		neighbors_b = G.neighbors(b)#copy.deepcopy(Degree_Node[b][1])
		maxdegree = -1
		maxnode = None	
		i =None		
		for i in neighbors_b:
			if(maxdegree<Degree_Node[i][0]):
				maxdegree=Degree_Node[i][0]
				maxnode=i
		i = maxnode
		while Flagger_b.has_key(maxnode):
			try:
				maxnode = neighbors_b.pop() #the neighbor with the next highest degree is NOT being chosen here.
			except IndexError:
				maxnode = i
				k_hop = 2
				while k_hop > 0:
					neighbors_b = G.neighbors(maxnode)#copy.deepcopy(Degree_Node[maxnode][1])
					maxnode = random.choice(neighbors_b)
					path_b.append(maxnode)
					if (k_hop == 0) :
						if (Flagger_b.has_key(maxnode)):
							k_hop = 2			
				path_b.pop()
		path_b.append(maxnode)
		Flagger_b[maxnode] = 1
		
		if Flagger_a.has_key(maxnode):
			return maxnode
		b = maxnode
