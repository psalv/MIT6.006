


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
    def __init__(self, From, To, w):
        self.From = From
        self.To = To
        self.w = w

    def __repr__(self):
        return self.From + " -> " + self.To + " : " + str(self.w)


class Vertex(object):
    """Uses object oriented programming to store a list of inbound and outbound neighbors for each vertice."""

    def __init__(self, pos):
        self.pos = pos
        self.InEdges = []
        self.OutEdges = {}

    def addInEdge(self, e):
        self.InEdges.append(e)

    def addOutEdge(self, to, w):
        self.OutEdges[to] = w

    def __hash__(self):
        return hash(self.pos)

    def __eq__(self, other):
        return self.pos == other

    def __repr__(self):
        return str(self.pos)


class Digraph(object):
    """A directed graph, storing nodes in a hash table for fast look up."""

    def __init__(self, file=None):
        self.nodes = HashTable()
        self.V = []

        if file != None:
            self.lFile(file)

    def vertices(self):
        """Used to iterate through every element in a hash table.
        Alternatively could iterate through self.V but this is much faster."""
        for i in self.nodes.hashed:
            if i == []:
                continue
            else:
                for j in i:
                    yield j[1]

    def insertNode(self, n):
        """Checks to see if the node is already present, if not inputs it."""
        if self.nodes.find(n) == None:
            v = Vertex(n)
            self.V.append(v)
            self.nodes.insert(v)


    def lFile(self, file):
        """Builds the unGraph from a file of the form: start edge > end edge \n start > end... etc
        Will use these data points to construct a graph of vertices and a corresponding adjacency matrix bound to the vertex objects."""
        file = open(file, 'r')
        for line in file:
            if line == '\n':
                continue


            try:
                a, b, w = line.split()
            except ValueError:
                self.insertNode(line)
                continue

            e = Edge(a, b, int(w))

            self.insertNode(a)
            self.insertNode(b)

            self.nodes.find(a).addOutEdge(self.find(b), int(w))
            self.nodes.find(b).addInEdge(e)


    def find(self, n):
        return self.nodes.find(n)





def findShortestPath(graph, start, v, memo):
    """Once the memo is built finding shortest paths to different vertices becomes trivial look ups.

    One problem is that this algorithm is infinite time on cyclic graphs.
    On DAGS it will run in O(V + E)."""

    if start == v:
        return 0

    if v in memo:
        return memo[v]

    low = None

    for i in graph.find(v).InEdges:

        if (start, v) == (i.From, i.To):

            if low == None:
                low = i.w
            elif i.w < low:
                low = i.w

        else:

            path = findShortestPath(graph, start, i.From, memo)

            if path != None:

                if path + i.w < low or low == None:
                    low = path + i.w

    if v not in memo:
        memo[v] = low

    return memo[v]





def testShortestPath(start):
    graph = Digraph("test1")
    memo = {}

    for i in "abcdef":
        print "Shortest path from " + start + " to " + i + ": ", findShortestPath(graph, "a", i, memo)




testShortestPath("a")