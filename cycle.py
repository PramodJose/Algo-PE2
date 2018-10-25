import collections
INP_FILE = "cyclicgraph.dat"   # the file name where the graph information is stored.
NUM_OF_VERTICES = 5             # the total number of vertices in the graph
'''
    NOTE:   The input file should contain (at least) NUM_OF_VERTICES lines which represents a graph.
            Each line should provide information to construct the adjacency list for vertex v, v= 1, 2, 3, 4, 5, 6, 7.
            The first integer on a line indicates the number of vertices adjacent to v. The remaining pairs of integers
            on that line indicate an adjacent vertex (w) and the weight of the edge (v, w).
'''

'''
    The Vertex class defines a blueprint of a node in a graph. Contains instance variables like name, status, indegree
    and a list (array) of object references to the adjacent vertices of a particular vertex.
    The class variable count automatically assigns names to each vertex starting from 'A'. Caveat: It is assumed that
    the graph does not have more than 26 vertices; otherwise the alphabets run out and vertices above 26 may have special
    characters in their names.
'''
class Vertex:
    count = 0

    def __init__(self):
        self.name = chr(ord('A') + Vertex.count)
        Vertex.count += 1
        self.status = None
        self.adjVertices = []
        self.indegree = 0

'''
    The Edge class contains a blueprint of an edge in a graph. Contains instance variables like label, src (source),
    dest (destination), weight. The class variable count automatically assigns labels to each edge starting from 1.
'''
class Edge:
    count = 1
    def __init__(self):
        self.label = Edge.count
        Edge.count += 1
        self.src = None
        self.dest = None
        self.weight = None

'''
    The Graph class defines a blueprint for a graph object. It contains instance variables like vertices, edges and
    vertexCount.
        -> vertexCount contains the number of vertices in the graph.
        -> vertices is an array which contains object references to Vertex objects. So, vertices[0] indicates the first
        vertex and vertices[vertexCount -1] would be the last vertex of the graph.
        -> edges is a dictionary (hashtable) where the key is a tuple of the source and destination vertices. The value
        is an Edge object which stores the information about the edge. 
'''
class Graph:
    def __init__(self, fileName, vertexCount):      # The filename and number of vertices in the graph should be passed
                                                    # as argument.
        self.vertices = []
        self.edges = {}
        self.vertexCount = vertexCount
        fin = open(fileName, "r")

        for i in range(vertexCount):            # Creating Vertex objects.
            self.vertices.append(Vertex())

        for vertex in self.vertices:
            line = fin.readline().split()       # Read a line from file, convert it into an array (list) based on whitespaces.
            countAdjVertices = int(line[0])     # The first int on a line is the number of adjacent vertices.
            line = line[1:]                     # Delete the first element in the list as it is no linger required.

            for j in range(countAdjVertices):   # countAdjVertices pairs of integers follow
                neighbour = self.vertices[int(line[j*2]) - 1]   # the first integer in a pair is the index of the
                                                            # neighbour. Using that, we find out who the neighbour is.
                neighbour.indegree += 1     # since there is an edge to the neighbour, increment neighbour's indegree by 1/

                weight = int(line[j*2 + 1])     # the second integer in a pair is the weight of the edge.
                newEdge = Edge()                # create a new Edge object..
                newEdge.weight = weight         # assign it all the properties of that edge.
                newEdge.src = vertex
                newEdge.dest = neighbour

                vertex.adjVertices.append(neighbour)    # add the neighbour to the list of adjacent vertices.
                self.edges[(vertex, neighbour)] = newEdge   # add the Edge object to the hashtable.

        fin.close()

    def display(self):  # Displays the graph.
        print("The graph is:-")

        for vertex in self.vertices:
            print(vertex.name, "-->  ", end="")

            for neighbour in vertex.adjVertices:
                print(neighbour.name + "(" + str(self.edges[(vertex, neighbour)].weight) + ")  ", end="")
            print()     # Adding a newline between each vertex's output line
        print()         # Adding a newline at the very end to make the output look neater.

'''
    isCyclic() is a modified Topological Sort function. Takes a Graph object as input.
    Returns True if there is at least one cycle in the graph; else returns False.
'''
def isCyclic(graph):
    Q = collections.deque()     # create an empty queue.
    topologicalNum = 0          # will be used later to identify whether there are cycles in the graph or not.

    for vertex in graph.vertices:   # traverse through the list of all the vertices...
        if vertex.indegree == 0:    # ..and if the indegree of that vertex is 0...
            Q.append(vertex)        # ..then add it to the queue..
            vertex.status = "Added to Queue"    # ..and change its status to "Added to Queue".

    while len(Q) > 0:       # while queue is not empty
        vertex = Q.popleft()    # dequeue the queue to obtain a vertex with indegree = 0...
        topologicalNum += 1     # ..give that vertex a topological number..
        vertex.status = "Visited"   # and change its status to "Visited"; to indicate that the node has been
                                    # deleted from the graph.

        for neighbour in vertex.adjVertices:    # Traverse through all the adjacent vertices of the current vertex...
            neighbour.indegree -= 1             # Decrement the indegree of the neighbouring node.
            if neighbour.indegree == 0:         # if the indegree of the neihgbour becomes 0..
                Q.append(neighbour)             # then add it to the queue.

    if topologicalNum != graph.vertexCount:     # At the end, if topologicalNum is not equal to the number of vertices
        return True                             # in the graph, it indicates that there was a cycle. So return True...
    else:
        return False                            # else return False.


g = Graph(INP_FILE, NUM_OF_VERTICES)            # Build a Graph from the information given in the file INP_FILE.
                                                # The number of vertices in the graph is NUM_OF_VERTICES
g.display()                                     # Display the graph.
print(isCyclic(g))                              # Print whether the graph is cyclic or not.
