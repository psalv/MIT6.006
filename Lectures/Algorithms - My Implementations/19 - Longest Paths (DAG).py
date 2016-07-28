

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
        self.inPr = False

        self.d = None
        self.pi = None

    def addNeighbor(self, n, w):
        assert n not in self.neighbors
        self.neighbors[n] = w

    def inProcess(self):
        self.inPr = True

    def outProcess(self):
        self.inPr = False

    def status(self):
        return self.inPr

    def D(self):
        if self.d == None:
            return 0
        return self.d

    def __hash__(self):
        return hash(self.pos)

    def __eq__(self, other):
        return other == self.pos

    def __repr__(self):
        return str(self.pos)

class Digraph(object):
    """A undirected graph, storing vertices in a hash table for fast look up.
    Neighbors are stored in adjacency lists as instance variables of vertices and accounts for weighted input.."""

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

            # w = -(int(w))
            w = int(w)

            fr = self.nodes.find(fr)
            to = self.nodes.find(to)

            fr.addNeighbor(to, -w)

    def find(self, n):
        return self.nodes.find(n)



def DFSvisit(s, parent, finish):
    """Sequentially visits every reachable node from the starting position s.
    Does not visit nodes that have previously been visited (avoiding infinite loops).

    Adds items that have finished to the finish list, creating a reverse topologically sorted list.
    Uses back edge identification to find any loops in the graph, for which we assume there are not in a topological sort.

    Will look at every neighbor exactly once so takes O(E) time."""
    s.inProcess()
    for v in s.neighbors:

        if v.status():
            s.neighbors[v] = "back"
            print "Back edge:", v, " -> ", s
            raise ValueError("Topological sort requires an acyclic graph.")

        if v not in parent:
            parent[v] = s
            DFSvisit(v, parent, finish)

            if finish != None:
                finish.append(v)
    s.outProcess()



def topoDFS(vertices):
    """Goes through every node in a digraph running DFSvisit iff the vertex has not already been visited.
    Returns a topologically sorted list of the vertices

    O(V + E) time."""
    parent = {}
    finish = []

    for s in vertices:
        if s not in parent:
            parent[s] = None
            DFSvisit(s, parent, finish)

            finish.append(s)

    #Reverses the list.
    finish = finish[::-1]

    return finish



def relax(u):
    """Relaxes every neighbor of the the vertex u."""
    for edge in u.neighbors:
        if edge.d == None:
            edge.d = u.neighbors[edge]
            edge.pi = u
            continue

        try:
            if edge.d > u.neighbors[edge] + u.d:
                if u.d == None:
                    edge.d = u.neighbors[edge]
                else:
                    edge.d = u.neighbors[edge] + u.d
                edge.pi = u
        except:
            if edge.d > u.neighbors[edge]:
                if u.d == None:
                    edge.d = u.neighbors[edge]
                else:
                    edge.d = u.neighbors[edge] + u.d
                edge.pi = u


def shortestPathDAG(graph, start, end, memo, topo):
    """Uses a topologically sorted directed acyclic graph to determine the shortest path from start > end.
    Operates in O(V + E) time."""

    go = False
    for vertex in topo:

        if vertex == start:
            go = True

        #These nodes have already been fully relaxed.
        if vertex in memo:
            continue
        elif go:
            relax(vertex)


    for i in topo:
        print i, i.d

    memo[end] = graph.find(end).d
    return memo[end]



def findLongestPath(start):
    """Finds the longest path from the start to any other node in the graph.

    Topological sort takes O(E + V) time, as does the DAG shortest path algorithm.

    So the memo isn't actually used, since we only need to do one iteration (everything relaxes properly)."""
    
    memo = {}
    gr = Digraph('test1')

    order = topoDFS(gr.V)

    shortestPathDAG(gr, start, order[-1], memo, order)

    longest = min(order, key=lambda x: x.D())

    print "Longest path (length, position): ", (-longest.D(), longest)


findLongestPath("s")




