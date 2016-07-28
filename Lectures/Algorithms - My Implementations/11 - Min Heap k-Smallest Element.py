


#This method works by the principle of creating a heap and building a max heap from the first k elements.
#If the element to be looked at is smaller than the first element of the max heap, it belongs in the new classification of the k smallest.
#This continues until all elements have been looked at.



execfile("/Users/paulsalvatore57/PycharmProjects/MIT 6.006/Lectures/Algorithms - My Implementations/4 - Heap Sort.py")

def findKSmallest1(arr, k):
    """Takes a heap and returns the k smallest element, O(n log k)."""
    tempMaxHeap = maxHeap(arr.array[:k][:])
    for i in arr.array[k:]:
        if i < tempMaxHeap.array[0]:
            tempMaxHeap.findMax()
            tempMaxHeap.append(i)
    return tempMaxHeap.array[0]



def findKSmallest2(arr, k):
    """Takes a heap and returns the k smallest element, altering the original heap.
    Done in time: O(k log n)"""
    sm = None
    for i in xrange(k):
        sm = arr._findMin()
    return sm




#If you are looking for the kth smallest element, it cannot possibly be below the kth level of a min heap.
#Therefore we can reduce the heap to a much smaller size.

#You need to look at the children of the current k smallest and see how the compare to the current k smallest.

import math

class numWithInfo(object):
    """A class to store a number along with it's position in an array (specifically oriented for heaps)"""
    def __init__(self, num, pos):
        self.num = num
        self.pos = pos

    def __repr__(self):
        return str(self.num)

    def __lt__(self, other):
        return self.num < other

    def __gt__(self, other):
        return self.num > other

    def hChildren(self):
        """Returns the positions of the children of this element in a heap."""
        return (self.pos * 2 + 1, self.pos * 2 + 2)

    def hParent(self):
        """Returns the position of a parent of a this element in a a heap."""
        if self.pos == 0:
            return None
        return int(math.ceil(self.pos / 2.0) - 1)


def findKSmallest3(arr, k):
    """Uses the fact that the kth smallest element must be a child of the (k-1)th smallest element to return the kth smallest element.

    Works in O(k log k) time
    Operations are done on tempMinHeap which will have at most k elements (two added and one removed each time, so net gain of 1)."""

    tempMinHeap = minHeap([])
    tempMinHeap.append(numWithInfo(arr.array[0], 0))

    for i in xrange(k + 1):
        curMin = tempMinHeap._findMin()
        if i == k - 1:
            return curMin.num

        try:
            for i in curMin.hChildren():
                tempMinHeap.append(numWithInfo(arr.array[i], i))
        except IndexError:
            continue




arr = minHeap([5, 6, 7, 8, 9, 1])
# print findKSmallest1(arr, 3)
# print findKSmallest2(arr, 3)      #Mutates the list via findMin
# print arr.array
# print findKSmallest3(arr, 3)      #Mutates the list via findMin