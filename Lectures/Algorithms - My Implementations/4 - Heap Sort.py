


#The height of this tree is bounded by log(n) since it will always nearly form a binary tree.
#max_heapify is O(logn)
#build_max_heaps has O(nlogn) at first glance but upon more careful examination it actually will have O(n) complexity.
    #This is because at the n/2 level of leaves you are only performing one maxheapify.
    #At the higher levels you may perform more maxheapify operations, however the number of nodes decreases.
    #The only node that has a logarithmic number of operations is the root node
#Heap_sort has a complexity O(nlogn) since it must max_heapify (O(logn)) n times. It sorts a list in descending order.



import math, random


class maxHeap(object):
    """Provides the functions necessary for building and maintaining a max heap."""

    def __init__(self, arr):
        self.array = arr
        self.buildMaxHeap()


    def buildMaxHeap(self):
        """Builds a max heap from an unsorted array."""
        for i in xrange(len(self.array)/2, -1, -1):
            self.maxHeapify(i)


    def maxHeapify(self, i):
        """Runs through an array starting at position i ensuring the max heap property of this subtree is maintained."""
        l = 2*i + 1
        r = 2*i + 2
        heap_size = len(self.array)

        if l >= heap_size:
            return

        if l < heap_size and self.array[l] > self.array[i]:
            largest = l
        else:
            largest = i

        if r < heap_size and self.array[r] > self.array[largest]:
            largest = r

        if largest != i:
            self.array[i], self.array[largest] = self.array[largest], self.array[i]
        else:
            return

        self.maxHeapify(largest)


    def maxHeapSort(self):
        """Assumes the max heapify property is satisfied for every node except the parent of the last node.
        Inserts the last node properly into the max heap."""

        if len(self.array) > 1:

            self.array[0], self.array[-1] = self.array[-1], self.array[0]
            pos = len(self.array) - 1

            while self.parent(pos) != None:
                pos = self.parent(pos)
                self.maxHeapify(pos)


    def insert(self, i):
        """Inserts and element, i, into a heap and sorts it accordingly."""
        i = len(self.array)
        self.array.append(key)
        par = self.parent(i)

        last = False

        while self.array[i] > self.array[par]:

            self.array[i], self.array[par] = self.array[par], self.array[i]
            i = par
            par = self.parent(par)

            if last:
                break
            if par == 0:
                last = True


    def child(self, pos, left=True):
        """Returns the position of a child in a heap."""
        if left:
            return pos*2 + 1
        else:
            return pos*2 + 2


    def parent(self, pos):
        """Returns the position of a parent of a node."""
        if pos == 0:
            return None
        return int(math.ceil(pos/2.0) - 1)


    def checkMaxHeapRI(self):
        """Notifies the positions of violations of the max heap property in the max heap."""
        p = 0
        while True:
            l, r = self.child(p), self.child(p, False)

            try:
                if self.array[l] > self.array[p]:
                    print "Position " + str(l) + " does not hold, value: " + str(A[l])
                if self.array[r] > self.array[p]:
                    print "Position " + str(r) + " does not hold, value: " + str(A[r])
            except IndexError:
                print "Max heap RI holds."
                return
            p += 1


    def findMax(self):
        """Returns and removes the maximum element from the heap."""
        maxValue = self.array[0]
        self.array[0] = self.array[-1]
        self.array.pop(-1)
        self.maxHeapify(0)
        return maxValue


    def __str__(self):
        toStr = ''
        for i in self.array:
            toStr += str(i) + ' '
        return toStr





class minHeap(object):
    """Provides the functions necessary for building and maintaining a min heap."""

    def __init__(self, arr):
        self.array = arr
        self.buildMinHeap()


    def buildMinHeap(self):
        """Builds a min heap from an unsorted array."""
        for i in xrange(len(self.array)/2, -1, -1):
            self.minHeapify(i)


    def minHeapify(self, i):
        """Runs through an array starting at position i ensuring the min heap property of this subtree is maintained."""
        l = 2 * i + 1
        r = 2 * i + 2
        heap_size = len(self.array)

        if l >= heap_size:
            return

        if self.array[l] < self.array[i]:
            smallest = l
        else:
            smallest = i

        if r < heap_size and self.array[r] < self.array[smallest]:
            smallest = r

        if smallest != i:
            self.array[i], self.array[smallest] = self.array[smallest], self.array[i]
        else:
            return

        self.minHeapify(smallest)


    def minHeapSort(self):
        """Assumes the min heapify property is satisfied for every node except the parent of the last node.
        Inserts the last node properly into the min heap."""

        self.array[0], self.array[-1] = self.array[-1], self.array[0]
        pos = len(self.array) - 1
        while self.parent(pos) != None:
            pos = self.parent(pos)
            self.minHeapify(pos)


    def insert(self, key):
        """Inserts and element, i, into a heap and sorts it accordingly."""
        i = len(self.array)
        self.array.append(key)
        par = self.parent(i)


        last = False

        while self.array[i] < self.array[par]:

            self.array[i], self.array[par] = self.array[par], self.array[i]
            i = par
            par = self.parent(par)

            if last:
                break
            if par == 0:
                last = True


    def child(self, pos, left=True):
        """Returns the position of a child in a heap."""
        if left:
            return pos*2 + 1
        else:
            return pos*2 + 2


    def parent(self, pos):
        """Returns the position of a parent of a node."""
        if pos == 0:
            return None
        return int(math.ceil(pos/2.0) - 1)


    def checkMinHeapRI(self):
        """Notifies the positions of violations of the min heap property in the min heap."""
        p = 0
        t = False
        while True:
            l, r = self.child(p), self.child(p, False)

            try:
                if self.array[l] < self.array[p]:
                    print "Position " + str(l) + " does not hold, value: " + str(self.array[l])
                    t = True
                if self.array[r] < self.array[p]:
                    print "Position " + str(r) + " does not hold, value: " + str(self.array[r])
                    t = True
            except IndexError:
                if not t:
                    print "Min heap RI holds."
                else:
                    print "Min heap RI does not hold."
                return
            p += 1


    def findMin(self):
        """Returns and removes the minimum element from the heap.
        Takes O(lg n) time """
        minValue = self.array[0]
        self.array[0] = self.array[-1]
        self.array.pop(-1)
        self.minHeapify(0)
        return minValue


    def __str__(self):
        toStr = ''
        for i in self.array:
            toStr += str(i) + ' '
        return toStr




def testHeaps():
    x = []
    for i in xrange(1000):
        x.append(int(random.uniform(0, 5000)))

    maxH = maxHeap(x[:])
    minH = minHeap(x)

    maxH.insert(-1)
    minH.insert(-1)

    maxH.insert(60)
    minH.insert(60)

    maxH.insert(400)
    minH.insert(400)

    print minH.array

    maxH.checkMaxHeapRI()
    minH.checkMinHeapRI()

# testHeaps()
