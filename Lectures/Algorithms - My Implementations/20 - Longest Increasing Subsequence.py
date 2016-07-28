

def BFSubSeq(seq):
    """This is going to take O(n) time, I don't see how DP would be able to accomplish this faster.

    This is CONSECUTIVE subsequence, which is not the quesiton."""

    longest = None

    m = 1
    for i in xrange(len(seq) - 1):
        if seq[i + 1] > seq[i]:
            m += 1

        elif longest == None or longest < m:
            longest = m
            m = 1

    print longest






def longestSubSeq(seq, i, memo):

    choices = [1]

    for j in xrange(i + 1, len(seq)):

        if seq[j] <= seq[i]:                                #Check to ensure sequence is increasing
            continue

        elif j in memo:                                     #Reduce having to do work we have already done by memo look up
            choices.append(memo[j] + 1)

        else:
            choices.append(longestSubSeq(seq, j, memo) + 1)

    return max(choices)



def solveUsingMemo():

    x = [8, 3, 5, 2, 4, 9, 2.5, 2.6, 2.7, 2.8, 2.9, 3, 7, 11]*300
    memo = {}
    options = []
    for i in xrange(len(x) - 1, -1, -1):                    #Topological sort
        options.append(longestSubSeq(x, i, memo))
        memo[i] = options[-1]

    print options
    print max(options)


solveUsingMemo()

