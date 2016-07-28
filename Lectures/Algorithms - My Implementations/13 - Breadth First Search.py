

#Uses the neighbors of vertices in a graph to determine all reachable states from a given position.
#This implementation uses an object-oriented approach.

#An alternative would be storing neighbors in a secondary hash table, each position corresponding with a vertex and listing it's neighbors.
#The advantage to this alternative is that multiple sets of neighbors (multiple graph) can be mapped to the same vertices.
#Note that python dictionaries are implemented as hash table, therefore they allow for constant time look up.

class HashTable(object):
    """Creates a has table to attempt to create a data structure with O(1) insertion, deletion, and look up.
    Methods have been altered for the values of a graph, to be used as  look up table for vertices (and possibly edges).."""

    def __init__(self, vals=None):
        """If there are no vals given as arguments, then will create an empty hash table of size 8,
        otherwise will create a hash table twice as big as the number of vals inputted."""

        if vals != None:
            m = 2*len(vals)
        else:
            m = 13

        self.hashed = []
        self.m = m
        self.n = 0
        self._updateM()

        if vals != None:
            self.insert(vals)

    def _updateM(self):
        """Creates a new hash table depending on the current size of m, and rehashes all of the old items into the new table."""
        new = []
        items = []
        for i in xrange(self.m):
            try:
                if self.hashed[i] != []:
                    for i in self.hashed[i]:
                        items.append(i[1])
                else:
                    new.append([])
            except IndexError:
                new.append([])

        self.hashed = new
        self.insert(items, True)

    def _divisionHash(self, x):
        """Uses division hashing to hash the val.
        The value given will be dependent on the type of __hash__ function that the item has specified.
        Note that this is an inefficient hashing method and multiplication or universal hashing would be much more effective (albeit more difficult to implement)"""
        return hash(x) % self.m

    def insert(self, vals, update=False):
        """Inserts either a single value or a list of values into the has table.
        If the n value exceeds to m value, will create a larger hash table and rehash all of the values."""
        if not update:
            if type(vals) != list:
                self.n += 1
            else:
                self.n += len(vals)

        if self.n > self.m:
            self.m *= 2
            self._updateM()

        toInsert = []
        if type(vals) != list:
            toInsert.append((self._divisionHash(vals), vals))

        else:
            for i in vals:
                toInsert.append((self._divisionHash(i), i))

        for i in toInsert:
            self.hashed[i[0]].append(i)

    def find(self, val, delete=False):
        """Finds the given item (identified by it's position (value) within the graph) in the hash table (if it exists).
        If delete, will remove the item from the has table.

        Returns the object in the hash table."""
        key = self._divisionHash(val)
        index = -1
        for i in self.hashed[key]:
            index += 1
            if i[1].pos == val:
                if delete:
                    self.n -= 1
                    self.hashed[key].pop(index)
                    return
                else:
                    return i[1]                     #Here is where the change was made to just return the vertex object.
        return None

    def delete(self, val):
        """Removes the given item from the has table.
        If the number of items, n, falls below 1/4 the m value, will rehash the table with m = m/2."""
        self.find(val, True)
        if self.m > 4 * self.n:
            self.m /= 2
            self._updateM()


class Edge(object):

    def __init__(self, frm, to):
        self.frm = frm
        self.to = to

    def __str__(self):
        return str(self.frm) + ' > ' + str(self.to)

class Vertex(object):
    """Uses object oriented programming to store an adjacency list in neighbors for each vertice."""

    def __init__(self, pos):
        self.pos = pos

        #Serves as the adjacency list for the vertexes, in an object oriented manner.
        self.neighbors = []

    def addNeighbor(self, n):
        self.neighbors.append(n)

    def __hash__(self):
        return hash(self.pos)

    def printNeighbors(self):
        toStr = str(self.pos) + ' > '
        for i in self.neighbors:
            toStr += str(i) + ', '
        return toStr

    def __repr__(self):
        return str(self.pos)

class unGraph(object):
    """A undirected graph, storing nodes in a hash table for fast look up and also soring edges.
    Note: for the sole purpose of neighbor look up storing edges is a wsate of space."""

    def __init__(self, file=None):
        self.nodes = HashTable()
        self.edges = []

        if file != None:
            self.lFile(file)

    def insertNode(self, n):
        """Checks to see if the node is already present, if not inputs it."""
        if self.nodes.find(n) == None:
            self.nodes.insert(Vertex(n))

    def lFile(self, file):
        """Builds the unGraph from a file of the form: start edge > end edge \n start > end... etc
        Will use these data points to construct a graph of vertices and edges (keeps track of neighbors for simple BFS)."""
        file = open(file, 'r')
        for line in file:
            a, b = line.split()
            self.insertNode(a)
            self.insertNode(b)

            #This part will change for a digraph.
            a = self.nodes.find(a)
            b = self.nodes.find(b)

            #I don't think that this is necessary if each vertex has an adjacency list (waste of storage).
            #May be useful for other graphing purposes but not for that of a BFS.
            self.edges.append(Edge(a, b))
            self.edges.append(Edge(b, a))

            #Builds the adjacency list in a object-oriented way (instance variables of each vertex).
            a.addNeighbor(b)
            b.addNeighbor(a)

    def find(self, n):
        return self.nodes.find(n)

    def __str__(self):
        """This is a poor way to represent a string."""
        for e in self.edges:
            print e
        return ''

def BFS(graph, start, pathTo=None):
    """"Finds all of the possible states from the starting point start.
    If toPath, returns the shortest path from start to toPath.

    Stores the level (the path length) to each node from the start in level.
    Stores the parent of each node in parent."""
    start = graph.find(start)
    level = {start: 0}
    parent = {start: None}
    i = 1
    frontier = [start]

    while frontier:                  #Terminates when frontier is empty.
        print frontier
        nxt = []
        for u in frontier:
            for v in u.neighbors:
                if v not in level:
                    level[v] = i
                    parent[v] = u
                    nxt.append(v)
        frontier = nxt
        i += 1

    if pathTo != None:
        nxt = graph.find(pathTo)
        pth = str(nxt)
        while parent[nxt] != None:
            pth += " " + str(parent[nxt])
            nxt = parent[nxt]

        return pth

q = unGraph('test1')
print BFS(q, 'a', 'e')