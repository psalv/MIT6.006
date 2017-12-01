

#The fastest run time for Dijkstra is O(VlgV + E) accomplished using a Fibonacci heap.
#In this implementation a min-heap will be used achieving O(VlgV + ElgV), where V is num vertices, E is num edges.
import random

x = random.ra
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
    """Uses object oriented programming to store an adjacency list in neighbors for each vertex.
    Modified for use in a shortest path algorithm storing d (the best current weight value to get to this vertex) and pi (it's predecessor)."""

    def __init__(self, pos):
        self.pos = pos
        self.neighbors = {}

        self.d = 1073741824     #  "infinity"
        self.pi = None

    def addNeighbor(self, n, w):
        assert n not in self.neighbors
        self.neighbors[n] = w

    def __hash__(self):
        return hash(self.pos)

    def __eq__(self, other):
        return other == self.pos

    def __repr__(self):
        return str(self.pos)

    def __str__(self):
        return str(self.pos)


class Digraph(object):
    """A undirected graph, storing vertices in a hash table for fast look up.
    Neighbors are stored in adjacency lists as instance variables of vertices and accounts for weighted input."""

    def __init__(self, file=None):
        self.nodes = HashTable()
        self.V = []

        if file != None:
            self.lFile(file)

    def insertNode(self, n):
        """Checks to see if the node is already present, if not inputs it."""
        if self.nodes.find(n) == None:
            to = Vertex(n)
            self.nodes.insert(to)
            self.V.append(to)

    def lFile(self, file):
        """Builds the Digraph from a file with lines of the form: start edge, end edge, weight.
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

    def find(self, n):
        return self.nodes.find(n)


def relax(u, edge):
    """Relaxes a neighbor of the the vertex u."""

    if edge.d > u.neighbors[edge] + u.d:
        edge.d = u.neighbors[edge] + u.d
        edge.pi = u


def BellmanFord(graph, start):
    """Solves shortest path problems in O(VE) time, recall that E = O(V**2)

    Identifies unreachable vertices as well as negative cycles."""

    #Due to the way relax works setting start.d = 0 means that this will in fact be the start point for the relaxation.
    graph.find(start).d = 0
    for i in xrange(len(graph.V) - 1):

        for vert in graph.V:
            for edg in vert.neighbors:
                relax(vert, edg)

    for vert in graph.V:

        if vert.d == 1073741824:
            print "Unreachable vertex: ", vert
            continue

        for edg in vert.neighbors:

            if edg.d > vert.d + vert.neighbors[edg]:
                print "Negative cycle from:", vert, "to", edg



def testBellmanFord():
    graph = Digraph('test1')
    BellmanFord(graph, "s")


testBellmanFord()

