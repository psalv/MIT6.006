
#O(nlogn)

#A disadvantage of merge sort when compared to insertion sort is that it requires O(n) auxiliary space,
#That is to say it creates copies and takes up more space, while insertion sort works within the same list and O(1) auxiliary space.



#The merge sort algorithm uses the principle that a list of length one is sorted.
#Therefore by recursively dividing the list until it becomes a list of length one we sort the list.
#The merge function than does the work in taking the elements of the two list and joining them in a way that maintains sorting.
#At first I popped the first element from the list, but I realized this shifts elements down therein adding superfluous work.

import time
start_time = time.time()



def mergeSort(listOf):

    n = len(listOf)

    if n == 1:
        return listOf

    new1 = mergeSort(listOf[0:n / 2])
    new2 = mergeSort(listOf[n / 2:])

    return merge(new1, new2)



def merge(l1, l2):
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

        if l1[i] >= l2[j]:
            ans.append(l2[j])
            j += 1
        else:
            ans.append(l1[i])
            i += 1



# print recSort([324,232,32,5457,234,32,6,75,45,534,234,23,2]*5527)

# print '\n', ("--- %s seconds ---" % (time.time() - start_time))



