

#This is an augmented version of my first implementation, further augmentation is needed to make the data structure specific to needs as they arise.


class Vertex(object):
    """Uses object oriented programming to store an adjacency list in neighbors for each vertice."""

    def __init__(self, pos):
        self.pos = pos
        self.inPr = False

    def inProcess(self):
        self.inPr = True

    def outProcess(self):
        self.inPr = False

    def status(self):
        return self.inPr

    def __eq__(self, other):
        return other == self.pos

    def __hash__(self):
        return hash(self.pos)

    def __repr__(self):
        return str(self.pos)


class Digraph(object):
    """A directed graph, storing nodes in a hash table for fast look up and also soring edges."""

    def __init__(self, file=None):
        self.nodes = {}

        if file != None:
            self.lFile(file)

    def vertices(self):
        return self.nodes

    def neighbors(self, n):
        return self.nodes[n]

    def insertNode(self, n):
        """Checks to see if the node is already present, if not inputs it."""
        if n not in self.nodes:
            self.nodes[Vertex(n)] = []

    def lFile(self, file):
        """Builds a directed graph from a file of the form: start edge > end edge \n start > end... etc

        Will use these data points to construct a graph of vertices bound to adjacency matrices."""
        file = open(file, 'r')
        for line in file:
            if line == '\n':
                continue

            try:
                a, b = line.split()
            except ValueError:
                self.insertNode(line)
                continue

            self.insertNode(a)
            self.insertNode(b)

            self.nodes[a].append(Vertex(b))






def DFSvisit(s, vertices, parent):
    """Sequentially visits every reachable node from the starting position s.
    Does not visit nodes that have previously been visited (avoiding infinite loops).

    A normal DFSvisit algorithm, will build a parent dictionary by visiting every node in the graph."""

    for v in vertices[s]:

        if v not in parent:
            parent[v] = s
            DFSvisit(v, vertices, parent)



def DFS(vertices, st):
    """Goes through every node in a digraph running DFSvisit iff the vertex has not already been visited.
    Begins the search at the starting node st."""

    for key in vertices:
        if key == st:
            st = key
            break
    else:
        raise ValueError("Key not in graph")

    parent = {st:None}
    DFSvisit(st, vertices, parent)

    for s in vertices:

        if s not in parent:
            parent[s] = None
            DFSvisit(s, vertices, parent)

    print parent



gr = Digraph('test1')
DFS(gr.vertices(), "a")



