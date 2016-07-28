




def kShiftBinarySearch(arr, e):
    """Returns the index of an element e in the array arr.
    The array array may be comprised of two, non-overlapping, lists that are in order:
    ex. the list: [4, 5, 6, 1, 2, 3] would be searchable by this function."""

    global y

    arr.append(None)
    second = False
    if e < arr[0]:
        second = True

    m = 2
    n = len(arr)/2 - 1
    q = 2*n

    while arr[n] != e:

        change = q / m
        if change == 0:
            y += 1
            change = 1

        if second:


            if arr[n] > arr[0]:
                n += change
                m *= 2

            elif arr[n] > e:
                n -= change
                m *= 2

            else:
                n += change
                m *= 2


        else:

            if arr[n] < arr[0]:
                n -= change
                m *= 2

            elif arr[n] > e:
                n -= change
                m *= 2

            else:
                n += change
                m *= 2

    arr.pop(-1)
    return n


def testKSearch():

    #Tests how many times the += 1 call is called for numbers up to 100000
    global y
    max = (0, 0)

    arr = []
    for i in xrange(100000):
        arr.append(i)
    for i in xrange(100000 - 1):

        kShiftBinarySearch(arr, i)

        if y > max[1]:
            max = (i, y)

        y = 0

    print "Max number of calls for += 1 (number, calls): ", max



    arr = [2, 2 ,3 ,4, 5, 23, 1]*1000
    arr.append(100)
    if arr[kShiftBinarySearch(arr, 100)] == 100:
        print "\nLast element bigger than everything pass.\n"


    print "Standard check:"
    arr = [5, 6, 7, 8, 20, 33, 1, 2, 3]
    for i in arr:
        print i, arr[kShiftBinarySearch(arr, i)] == i


y = 0
# testKSearch()









