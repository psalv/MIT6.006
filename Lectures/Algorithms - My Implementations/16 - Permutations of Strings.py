


def mergeSort(listOf, merge):

    n = len(listOf)
    if n == 1:
        return listOf
    new1 = mergeSort(listOf[0:n / 2], merge)
    new2 = mergeSort(listOf[n / 2:], merge)
    return merge(new1, new2)

def merge1(l1, l2):
    """Based on the FIRST element of a tuple."""
    ans = []
    n1, n2 = len(l1), len(l2)

    i, j = 0, 0
    while len(ans) < n1 + n2:

        if j == n2:
            ans += l1[i:]
            return ans
        if i == n1:
            ans += l2[j:]
            return ans

        if l1[i][0] >= l2[j][0]:
            ans.append(l2[j])
            j += 1
        else:
            ans.append(l1[i])
            i += 1

def merge2(l1, l2):
    """Based on the SECOND element of a tuple."""
    ans = []
    n1, n2 = len(l1), len(l2)

    i, j = 0, 0
    while len(ans) < n1 + n2:

        if j == n2:
            ans += l1[i:]
            return ans
        if i == n1:
            ans += l2[j:]
            return ans

        if l1[i][1] >= l2[j][1]:
            ans.append(l2[j])
            j += 1
        else:
            ans.append(l1[i])
            i += 1




def buildPermutation(file):
    """Loads a file from of permutations of the form:   place in queue        which string character to place.
      Returns a list of tuples representing (position in queue, permutation to do)."""
    file = open(file, 'r')
    perm = []
    for line in file:
        a, b = line.split()
        perm.append((int(a) - 1, int(b) - 1))
    return perm

def buildInverse(perm):
    """Builds a tuple list inverse to the permutation list and returns a sorted copy.
    Alternatively I could resort the list using the second """
    inv = []
    for i in perm:
        inv.append((i[1], i[0]))
    return mergeSort(inv, merge1)

def permutateString(file, string="abcde"):
    """Builds a permutator from a file and permutates a string, and then reassembles it using it's inverse."""
    perm = buildPermutation(file)
    new = ''
    for i in mergeSort(perm, merge1):
        new += string[i[1]]
    print "Permutated:", new

    #Can build an entirely new list from the already sorted array and resort the list.
    bck = ''
    for i in buildInverse(perm):
        bck += new[i[1]]
    print "Returned:  ", bck

    #Alternatively I can just change how I sort rather than building a new list (this is the clearly better method).
    bck = ''
    for i in mergeSort(perm, merge2):
        bck += new[i[0]]
    print "Returned2: ", bck

permutateString('test1')