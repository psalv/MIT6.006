

#ITERATORS:
#Iterators are good for memory management (don't eed to store everything at once).
#next() returns the next element in the sequence we are iterating over or it will raise StopIteration.
#iter() returns an iterator, so if you have a list you can call iter on it:

    # l = [1, 2, 3, 4]
    # l = l.__iter__()
    # for i in xrange(4):
    #     print l.next()



#FASTA files for DNA sequences contain too much information to store in memory all at once.
#Instead, it is prudent to use an iterator to look at the sequence one character at a time.

class FASTASequence:

    def __init__(self, filename):
        self.f = open(filename, 'r')
        self.buf = ''
        self.info = self.f.readline()    #Reads the first line of the FASTA file, containing ID and such.
        self.pos = 0

    def __iter__(self):
        """This makes it so I can call for i in (FASTASequence object) and it will return an instance of next for each call.
        Does so until StopIteration is raised."""
        return self

    def next(self):

        #Reads the next line of the file, if the next line contains nothing than iteration is stopped (the sequence is finished).
        while '' == self.buf:
            self.buf = self.f.readline()
            if '' == self.buf:
                self.f.close()
                raise StopIteration
            self.buf = self.buf.strip()

        #Takes the first character and gets rid of the rest of it.
        #This continues until self.buf is empty, at which point a new line is read and the process repeats.


        nextchar = self.buf[0]
        self.buf = self.buf[1:]
        self.pos += 1
        return nextchar

        # Debunked, the following is wrong:
            # One problem I see with this is that building self.buf[1:] is a lengthy process.
            # I think it would be faster to keep a self variable with the length of the current line and our position.
            # This means that the line would not shrink (slightly more memory intensive) but I think the speed gain would out-weight this.





#So after doing speed tests it appears that neither code is significantly faster (it appears mine may actually be very very slightly slower),
#Therefore their code is more favorable due to it's lower memory cost and slight speed advantage (all around better)..
#I think because lines cannot be longer than 120 characters in FASTA format, rebuilding the string is not strenuous
class myFASTASequence:

    def __init__(self, filename):
        self.f = open(filename, 'r')
        self.buf = ''
        self.info = self.f.readline()
        self.pos = 0

        self.bufLength = None
        self.iterPos = None

    def __iter__(self):
        return self

    def next(self):
        """I've implemented next such that it need not rebuild a list every iteration, but rather will be slightly more memory intensive."""

        while '' == self.buf:
            self.buf = self.f.readline()
            if '' == self.buf:
                self.f.close()
                raise StopIteration
            self.buf = self.buf.strip()
            self.bufLength = len(self.buf)
            self.iterPos = 0

        if self.iterPos < self.bufLength:
            nextchar = self.buf[self.iterPos]
            self.iterPos += 1
            self.pos += 1
            return nextchar

        else:
            self.buf = ''
            return self.next()




import time, math

def speedtest(times = 10):

    speedMy = []
    speedTheir = []


    for j in xrange(times):

        theirs = FASTASequence("fdog0.fa")

        start_time = time.time()
        for i in theirs:
            i.upper()
        x = time.time() - start_time

        speedTheir.append(x)

    for j in xrange(times):

        my = myFASTASequence("fdog0.fa")

        start_time = time.time()
        for i in my:
            i.upper()
        y = time.time() - start_time

        speedMy.append(y)

    print 'their: ', sum(speedTheir)/float(times)
    print 'my: ', sum(speedMy)/float(times)

# speedtest(30)


