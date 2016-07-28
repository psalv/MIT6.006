
#Uses digraph and vertex classes to construct a graph from a file.
#Vertexes are stored twice, once in a self.V parameter such that all vertexs can be examined at once.
    #Alternatively if I had a way to iterate through every element of a hash table I would be able ot free up this waste of memory of the scale O(|V|)

#The DFSvisit algorithm is currently set up to find back edges which indicate cycles in the graph.



#An alternative way to store the vertices is in a dictionary where the values contain the adjacency lists.
#Instead I've made the adjacency list apart of the vertex class.



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
    """Uses object oriented programming to store an adjacency list in neighbors for each vertice."""

    def __init__(self, pos):
        self.pos = pos
        self.neighbors = {}
        self.inPr = False

    def addNeighbor(self, n):
        self.neighbors[n] = None

    def inProcess(self):
        self.inPr = True

    def outProcess(self):
        self.inPr = False

    def status(self):
        return self.inPr

    def __hash__(self):
        return hash(self.pos)

    def printNeighbors(self):
        toStr = str(self.pos) + ' > '
        for i in self.neighbors:
            toStr += str(i) + ', '
        return toStr

    def __repr__(self):
        return str(self.pos)

class Digraph(object):
    """A directed graph, storing nodes in a hash table for fast look up and also soring edges."""

    def __init__(self, file=None):
        self.nodes = HashTable()

        if file != None:
            self.lFile(file)

    def vertices(self):
        """Used to iterate through every element in a hash table.
        This will take a longer time to iterate than just collecting the vertices in a self.V instance variable.
        The trade off is this method is memory efficient while the other is speed efficient.

        I think the speed is a better deal then using the superfluous memory
        My reason is that the memory is always there but the hash table is iterated through only once for each vertices call."""
        for i in self.nodes.hashed:
            if i == []:
                continue
            else:
                for j in i:
                    yield j[1]

    def insertNode(self, n):
        """Checks to see if the node is already present, if not inputs it."""
        if self.nodes.find(n) == None:
            self.nodes.insert(Vertex(n))

    def lFile(self, file):
        """Builds the unGraph from a file of the form: start edge > end edge \n start > end... etc
        Will use these data points to construct a graph of vertices and a corresponding adjacency matrix bound to the vertex objects."""
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

            a = self.nodes.find(a)
            b = self.nodes.find(b)

            #Because this graph is directed, only the a > b edge is made, not the b > a.
            a.addNeighbor(b)

    def find(self, n):
        return self.nodes.find(n)





def backDFSvisit(s, parent):
    """Sequentially visits every reachable node from the starting position s.
    Does not visit nodes that have previously been visited (avoiding infinite loops).

    Will identify back edges based on if the neighbors of the current node are in the recursion stack.

    Note: Utilizes a regular DFS algorithm however remember to change DFS to use this DFSvisit algorithm"""
    s.inProcess()
    for v in s.neighbors:

        #Use the inProcess parameter to tell what is currently in the stack.
        #A back edge indicates a cycle so this method can be used for cyclic identification.
        #Note that a bidirectional graph cannot have back edges by their definition.
        if v.status():
            s.neighbors[v] = "back"
            print "Back edge:", s, " -> ", v

        if v not in parent:
            parent[v] = s
            backDFSvisit(v, parent)
    s.outProcess()





def fcbDFSvisit(s, parent, c):
    """Sequentially visits every reachable node from the starting position s.
    Does not visit nodes that have previously been visited (avoiding infinite loops).

    Will identify forward and cross edges (but not distinguish between the two) by using a counter for tree position.
    Requires an altered DFS algorithm wherein parent keeps track of c, the position within the tree."""
    c += 1
    for v in s.neighbors:

        if v not in parent:
            parent[v] = (s, c)
            fcbDFSvisit(v, parent, c)

        elif parent[v][1] >= parent[s][1]:
            s.neighbors[v] = "forward or cross"
            # print "Forward or cross edge:", s, " -> ", v

        else:
            s.neighbors[v] = "back"
            # print "Back:", v, " -> ", s

def fcbDFS(vertices):
    """Goes through every node in a digraph running DFSvisit iff the vertex has not already been visited.
    Has been modified to find forward and cross edges however would work with a regular DFSvisit algorithm."""
    parent = {}

    for s in vertices:
        c = 0
        if s not in parent:
            parent[s] = (None, c)
            fcbDFSvisit(s, parent, c)





def DFSvisit(s, parent):
    """Sequentially visits every reachable node from the starting position s.
    Does not visit nodes that have previously been visited (avoiding infinite loops).

    A normal DFSvisit algorithm, will build a parent dictionary by visiting every node in the graph."""
    for v in s.neighbors:
        if v not in parent:
            parent[v] = s
            DFSvisit(v, parent)

def DFS(vertices):
    """Goes through every node in a digraph running DFSvisit iff the vertex has not already been visited.

    Need to remember that a DFS just works to visit every edge in a network, it does not elucidate any path from one to another (many parents will be None)."""
    parent = {}

    for s in vertices:

        if s not in parent:
            parent[s] = None
            DFSvisit(s, parent)





gr = Digraph('test1')
# DFS(gr.vertices())
fcbDFS(gr.vertices())



