class Graph:
	n = 0 # number of vertices
	g =[[0 for x in range(10)] for y in range(10)] # adjacency matrix

	def __init__(self, x):
		self.n = x
		for i in range(0, self.n):
			for j in range(0, self.n):
				self.g[i][j]= 0 # initializing each element of the adjacency matrix to zero

	def displayAdjacencyMatrix(self):
		for i in range(0, self.n):
			print()
			for j in range(0, self.n):
				print("", self.g[i][j], end ="")
		print()

	def addEdge(self, x, y):
		if(x>= self.n) or (y >= self.n): # checks if the vertex exists in the graph
			print("Vertex does not exists !")
		if(x == y): # checks if the vertex is connecting to itself
			print("Same Vertex !")
		else: # connecting the vertices
			self.g[y][x]= 1
			self.g[x][y]= 1

	def addVertex(self):
		# increasing the number of vertices
		self.n = self.n + 1;
		# initializing the new elements to 0
		for i in range(0, self.n):
			self.g[i][self.n-1]= 0
			self.g[self.n-1][i]= 0

# creating objects of class Graph
obj = Graph(10);

obj.addEdge(0,9);
obj.addEdge(0,4);
obj.addEdge(1,5);
obj.addEdge(1,9);
obj.addEdge(2,7);
obj.addEdge(3,6);
obj.addEdge(3,8);
obj.addEdge(4,5);
obj.addEdge(6,7);
obj.addEdge(7,8);

obj.displayAdjacencyMatrix();
