


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

class Vertex(object):
    """Uses object oriented programming to store an adjacency list in neighbors for each vertice.

    Creates false nodes for any weighted edge greater than one. Does not deal with negative weights.
    False nodes in the adjacency list are of the form: nodeGoingTo+counter.
    When the counter reaches 1 the original node will be placed in the final adjacency list.

    This allows us to us a BFS to find the shortest path for a weighted graph."""

    def __init__(self, pos):
        self.pos = pos

        self.neighbors = []

    def addNeighbor(self, n, w):
        assert w > 0

        if w > 1:
            nil = Vertex(str(n) + str(w))
            self.neighbors.append(nil)
            nil.addNeighbor(n, w - 1)
        else:
            self.neighbors.append(n)

    def __hash__(self):
        return hash(self.pos)

    def __eq__(self, other):
        return other == self.pos

    def __repr__(self):
        return str(self.pos)

class Graph(object):
    """A undirected graph, storing vertices in a hash table for fast look up.
    Neighbors are stored in adjacency lists as instance variables of vertices and accounts for weighted input.."""

    def __init__(self, file=None):
        self.nodes = HashTable()

        if file != None:
            self.lFile(file)

    def insertNode(self, n):
        """Checks to see if the node is already present, if not inputs it."""
        if self.nodes.find(n) == None:
            self.nodes.insert(Vertex(n))

    def lFile(self, file):
        """Builds the Graph from a file with lines of the form: start edge, end edge, weight.
        Will use these data points to construct a graph of vertices storing adjacency lists and weights."""
        file = open(file, 'r')
        for line in file:
            fr, to, w = line.split()
            self.insertNode(fr)
            self.insertNode(to)

            w = int(w)

            fr = self.nodes.find(fr)
            to = self.nodes.find(to)

            fr.addNeighbor(to, w)
            to.addNeighbor(fr, w)

    def find(self, n):
        return self.nodes.find(n)



def shortestPathBFS(graph, start, finish):
    """"Uses a BFS to find the shortest path from start to finish of weighted bidirectional graph.
    Returns a sting consisting of the vertices that must be traversed in reverse order, omitting the superfluous vertices added.

    BFS operates in O(V + E), and if W represents the maximum weight of an edge, this will operate in O(V + WE) time.
    Therefore if W is sufficiently small (W < lgV), this algorithm will have a comparable speed to the Dijkstra algorithm."""

    start = graph.find(start)
    level = {start: 0}
    parent = {start: None}
    i = 1
    frontier = [start]


    while frontier:
        nxt = []
        for u in frontier:
            for v in u.neighbors:
                if v not in level:
                    level[v] = i
                    parent[v] = u
                    nxt.append(v)
        frontier = nxt
        i += 1

    nxt = graph.find(finish)
    pth = str(nxt)
    while parent[nxt] != None:
        try:
            if str(parent[nxt])[1].isdigit():
                nxt = parent[nxt]
        except IndexError:
            pth += " " + str(parent[nxt])
            nxt = parent[nxt]

    return pth

q = Graph('test1')
print shortestPathBFS(q, 'a', 'e')