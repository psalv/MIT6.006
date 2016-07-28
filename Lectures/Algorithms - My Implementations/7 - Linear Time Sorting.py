

def countSort1(A, k):
    """Sorts a list of ints, A, with a maximum value of k.
    Does so in O(n), without comparisons.
    This algorithm ONLY sorts integers, and nothing else."""
    array = [0] * k

    for i in A:
        array[i] += 1

    sortedArray = []
    for i in xrange(k):
        sortedArray.extend([i] * array[i])
    return sortedArray


def key(A, j):
    """This is a helper function, at this point in time it is very simple.
    Each element in A may be different than it's associated value (or key) therefore this function will change appropriately."""
    return A[j]


def countSort2(A, k):
    """Sorts a list of items with associated integer values (with a maximum value of k).
    Does so in O(n + k), without comparisons."""
    L = []
    for i in xrange(k):
        L.append([])

    for j in xrange(len(A)):
        L[key(A, j)].append(A[j])

    output = []
    for i in xrange(k):
        output.extend(L[i])
    return output


