#!/usr/bin/env python2.7

import unittest
from dnaseqlib import *

### Utility classes ###





# Maps integer keys to a set of arbitrary values.
class Multidict:
    # Initializes a new multi-value dictionary, and adds any key-value 2-tuples in the iterable sequence pairs to the data structure.
    def __init__(self, pairs=[]):
        self.multiD = {}


    # Associates the value v with the key k.
    def put(self, k, v):
        if k not in self.multiD:
            self.multiD[k] = []
        self.multiD[k].append(v)

    # Gets any values that have been associated with the key k; or, if
    # none have been, returns an empty sequence.
    def get(self, k):
        try:
            return self.multiD[k]
        except KeyError:
            return []





# Given a sequence of nucleotides, return all k-length subsequences
# and their hashes.  (What else do you need to know about each
# subsequence?) >> Need to know it's position in the sequence
def subsequenceHashes(seq, k):
    """Generates subsequence hashes of the form:
    [ (subsequence, position), hash ]"""
    toHash = RollingHash(seq[:k])
    # toHash = RollingHash(seq.seq[:k])

    # yield [(seq.seq[0:k], 0), toHash.current_hash()]
    yield [(seq[0:k], 0), toHash.current_hash()]
    for i in xrange(0, len(seq) - k):
    # for i in xrange(0, len(seq) - k):
    #     toHash.slide(seq.seq[i], seq.seq[i + k])
        toHash.slide(seq[i], seq[i + k])
        # yield [(seq.seq[i + 1:i+k + 1], i + 1), toHash.current_hash()]
        yield [(seq[i + 1:i+k + 1], i + 1), toHash.current_hash()]





# Similar to subsequenceHashes(), but returns one k-length subsequence
# every m nucleotides.  (This will be useful when you try to use two
# whole data files.)
def intervalSubsequenceHashes(seq, k, m):
    # start = ''
    # for i in xrange(k):
    #     start += next(seq)
    # toHash = RollingHash(start)

    toHash = RollingHash(seq[:k])

    # yield [(start, 0), toHash.current_hash()]
    yield [(seq[0:k], 0), toHash.current_hash()]
    for i in xrange(0, len(seq) - k, m):

        # try:
        #     start += next(seq)

        toHash.slide(start[i], start[i + k])

        toHash.slide(seq[i], seq[i + k])
        yield [(seq[i + 1:i + k + 1], i + 1), toHash.current_hash()]

        #     yield [(start[i + 1:i + k + 1], i + 1), toHash.current_hash()]
        # except IndexError:
        #     break



# Searches for commonalities between sequences a and b by comparing
# subsequences of length k.  The sequences a and b should be iterators
# that return nucleotides.  The table is built by computing one hash

    #Ignore m for now.
# every m nucleotides (for m >= k).


#Needs to return a tuple (x, y) corresponding the position of subsequence matche sin two different sequences.


def getExactSubmatches(a, b, k, m):
    multiD = Multidict()
    # aGen = subsequenceHashes(a, k)                   #(c)
    aGen = intervalSubsequenceHashes(a, k, m)          #(d), using intervals
    for i in aGen:
        multiD.put(i[1], i[0])
    bGen = subsequenceHashes(b, k)
    for i in bGen:
        temp = multiD.get(i[1])
        if temp != []:
            for j in temp:
                if j[0] == i[0][0]:
                    yield ((j[1], i[0][1]))



def test_one():
    foo = 'yabcabcabcz'
    bar = 'xxabcxxxx'
    matches = list(getExactSubmatches(foo, bar, 3, 1))
    correct = [(1, 2), (4, 2), (7, 2)]
    print (len(matches) == len(correct))
    for x in correct:
        print(x in matches)


compareSequences(getExactSubmatches, 'test1', (500,500), '/Users/paulsalvatore57/PycharmProjects/MIT 6.006/Assignments/PS4/data/fchimp0.fa', '/Users/paulsalvatore57/PycharmProjects/MIT 6.006/Assignments/PS4/data/fdog0.fa', 8, 100)



if __name__ == '__main__':
    if len(sys.argv) != 4:
        print 'Usage: {0} [file_a.fa] [file_b.fa] [output.png]'.format(sys.argv[0])
        sys.exit(1)

    # The arguments are, in order: 1) Your getExactSubmatches
    # function, 2) the filename to which the image should be written,
    # 3) a tuple giving the width and height of the image, 4) the
    # filename of sequence A, 5) the filename of sequence B, 6) k, the
    # subsequence size, and 7) m, the sampling interval for sequence
    # A.

