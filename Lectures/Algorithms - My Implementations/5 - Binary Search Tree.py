
#Do not use without altering, inefficient implementation.



#To makes these trees O(logn) we need balanced binary search trees, which I will learn about in a later lecture.


#This is my BST data structure. One note he made in class is that this code can be made more efficient recursively.
#For instance, the number incrementation of the subtrees need run through the tree a superfluous time to increment the data (when we know it passes the k invariant).
#With recursion we can go down to the last level before doing anything else to check this and do it all in one pass (would require largely rewriting my insertion code).

#To create a delete function I would only need to move pointers, however I'm not sure how to efficiently remove the old object.
    #In his implementation the BSTnode class does more.
    #I rely on a list system to keep all of the nodes, but his system simply has one node with left and right assignments.
    #These assignments will store the new node object, meaning that deletion truly is just reassigning pointers.
    #This makes my implementation comparatively inefficient in both runtime and memory usage, but writing it was a good exercise.

#My problem was visualization, I need the nodes in a list so I could convince myself they were still there,
#However them being stored as instance variables of the node object works identically to as if they were in a list in terms of storage.
#So a lesson from this implementation would be to trust my programming more, I don't need replicate storage just for reassurance.


class BSTnode(object):
    def __init__(self, value, parent = None, left = None, right = None):
        self._key = value
        self._left = left
        self._right = right
        self._parent = parent
        self._size = 1

    def getKey(self):
        return self._key

    def getLeft(self):
        return self._left

    def getRight(self):
        return self._right

    def getSize(self):
        return self._size

    def setRight(self, right):
        self._right = right

    def setLeft(self, left):
        self._left = left

    def setParent(self, parent):
        self._parent = parent

    def incrSize(self):
        self._size += 1

    def showTree(self):
        return str(self._parent) + ' -> ' + str(self._key) + ' --> L: ' + str(self._left) + ' R: ' + str(self._right)

    def __str__(self):
        return str(self._key)



class BST(object):

    def __init__(self, k, elements = None):
        self._BST = []
        if elements != None:
            self.buildBST(elements)
        self._k = k

    def setK(self, k):
        self._k = k

    def buildBST(self, A):
        """Takes an array and builds a binary search tree. The BSTnode objects keep track of the left/right/parent pointers.
        This will take O(n**2) time since it at the worst case (all ascending/descending order) need to check n elements n times."""
        for i in A:
            self._BST.append(BSTnode(i))
        for node in self._BST[1:]:
            toCheck = self._BST[0]

            while node._parent == None:

                if node.getKey() > toCheck.getKey():
                    if toCheck.getRight() == None:
                        toCheck.setRight(node)
                        node.setParent(toCheck)
                        self.incrSizes(node)

                    else:
                        toCheck = toCheck.getRight()
                else:
                    if toCheck.getLeft() == None:
                        toCheck.setLeft(node)
                        node.setParent(toCheck)
                        self.incrSizes(node)
                    else:
                        toCheck = toCheck.getLeft()

    def insertElement(self, el):
        """This insert element algorithm will take at worst O(n) time if all elements are in ascending/descending order.
        More generally, will insert and element in O(h) time, h being the height of the tree.
        Checks the k value with each node to ensure k constraints are met."""

        #If we are building the BST from scratch the first node starts here.
        if self._BST == []:
            self._BST.append(BSTnode(el))
            return None

        #Goes down the BST using the left/right pointers to find where the element should be inserted in the tree.
        toCheck = self._BST[0]
        while True:

            #Checks that the k value invariant is not violated
            if abs(el - toCheck.getKey()) < self._k:
                print '\nInput: ' + str(el) + ' is too close to ' + str(toCheck.getKey()) + '.\n'
                break

            #If the correct side already has a child, then that child is the next to be examined (moving down the tree).
            if el > toCheck.getKey():
                if toCheck.getRight() == None:
                    self._BST.append(BSTnode(el, toCheck))
                    toCheck.setRight(self._BST[-1])
                    self.incrSizes(el)
                    break
                else:
                    toCheck = toCheck.getRight()
            else:
                if toCheck.getLeft() == None:
                    self._BST.append(BSTnode(el, toCheck))
                    toCheck.setLeft(self._BST[-1])
                    node.setParent(toCheck)
                    self.incrSizes(el)
                    break
                else:
                    toCheck = toCheck.getLeft()

    def incrSizes(self, el):
        """Increments the size of each subtree associated with the newly added element, does so in O(h) time."""
        toCheck = self._BST[0]
        while True:

            if toCheck == None:
                break

            if el.getKey() == toCheck.getKey():
                break

            toCheck.incrSize()

            if el.getKey() > toCheck.getKey():
                toCheck = toCheck.getRight()
            else:
                toCheck = toCheck.getLeft()

    def rank(self, t):
        """Returns the number of nodes that have a value less than or equal t. Works in O(h) time."""
        toCheck = self._BST[0]
        r = 0
        while True:

            if toCheck == None:
                return 0

            if t == toCheck.getKey():
                r += 1
                try:
                    return r + toCheck.getLeft().getSize()
                except AttributeError:
                    return r

            if t > toCheck.getKey():
                try:
                    r += toCheck.getLeft().getSize() + 1
                    toCheck = toCheck.getRight()
                except AttributeError:
                    print str(t) + ' is not in the tree.'
                    return 0
            else:
                toCheck = toCheck.getLeft()

    def findMin(self):
        """Done in O(h) time."""
        start = self._BST[0]
        while True:
            if start.getLeft() != None:
                start = start.getLeft()
            else:
                return start

    def findMax(self):
        """Done in O(h) time."""
        start = self._BST[0]
        while True:
            if start.getRight() != None:
                start = start.getRight()
            else:
                return start

    def findNode(self, k):
        """Returns the node assigned to the given value in O(h) time."""
        toCheck = self._BST[0]
        while True:

            if toCheck == None:
                return None

            if toCheck.getKey() == k:
                return toCheck

            if k > toCheck.getKey():
                toCheck = toCheck.getRight()
            else:
                toCheck = toCheck.getLeft()

    def printTree(self):
        for i in self._BST:
            print i.showTree()

    def check_ri(self):
        """This algorithm type is one to use repeatedly for different data structures, raises an exception if RI does not hold.
        Idea is to run this while debugging, so complexity is less important, O(n)."""
        for i in self._BST:
            r = i.getRight()
            l = i.getLeft()
            if r != None:
                if r.getKey() < i.getKey():
                    raise ValueError('Node: ' + str(i) + ' does not hold ri, with right child: ' + str(r))
            if l != None:
                if l.getKey() > i.getKey():
                    raise ValueError('Node: ' + str(i) + ' does not hold ri, with left child: ' + str(l))




A = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
A = BST(3, A)
A.printTree()

# A.check_ri()

# print A.rank(49)

# c = A.findNode(83)
# print [c.getKey()]

# for i in A._BST:
#     print i._size, i

# A.printTree()

# A.insertElement(47)

# A.insertElement(100)

# A.printTree()

# print A.findMax()