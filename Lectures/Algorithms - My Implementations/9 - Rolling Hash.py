

###IF FILE IS BIG:
#Implementing rolling hash to accommodate iterators would be prudent for dealing with large text files
    #This class I currently have relies on storing the entire text in memory which is very inefficient.




###IMP. PROCESS
#After many hour sof trying to implement RollingHash from the in-class notes I found a Rabin-Karp algorithm on stack exchange.
#I believe my problem was with initialization, as my skip and append functions remained unchanged.
#The now working code uses skip before append, which should alter the value of magic but not the result.

#I think the real discrepancy comes in two places:
    #1) There is a clever check of adding the (u + prime) % prime, to ensure the value is positive.
    #2) The substring is built up on piece at a time using append, as is the first window frame.

#I'm not totally clear still while my code did not work.
#1 is not essential for finding the correct answer, therefore I must assume that 2 is a vital I was missing.




###USEFUL FACTS
# To get the ASCII digit code for a character use the order:        ord('a') = 97
# Alternatively you can get a character in the following manner:    chr(69)  = E


class RollingHash(object):
    """Maintains a rolling hash for a window of a loaded text, based on a substring we desire to locate.
    Expected to take amortized O(n) time to scan the entirety of the text.
    Uses the Rabin-Karp algorithm for rolling hash maintenance.

    Note: 4294967291 is the closest prime number to 2**32, or the amount of memory in one 32-bit cell.
    Note: there are 256 characters in the ASCII dictionary."""

    def __init__(self, base=256, p=4294967291):
        self.p = p
        self.base = base

        self.u = 0
        self.s = 0

        self.magic = None
        self.substring = None
        self.text = None
        self.wnd = None

        self.found = []


    def append(self, c):
        """Appends the rolling hash to include the character c."""
        self.u = (self.u * self.base + ord(c)) % self.p


    def skip(self, c):
        """Skip is to be performed before append.
        Removes the character c from the rolling hash."""
        self.u = (self.u - ord(c) * self.magic) % self.p


    def loadText(self, file, f=True):
        """Loads all of the text from a file (or a string) into a single string, removes newline characters."""
        if f:
            file = open(file, 'r')
            self.text = ''
            for line in file:
                self.text += line.strip()
        else:
            self.text = file

        self.textLen = len(self.text)


    def setSubstring(self, subs):
        """Stores the substring and it's length as instance variables.."""
        self.substring = subs
        self.wnd = len(subs)


    def initializeValues(self):
        """Raises an exception unless both a substring and text have been specified.
        Initializes s, the hash value of the substring that we are looking for.
        Initializes t, the hash value of the first window frame of the text
        Initializes magic, a constant which will speed up the skip operation

        Note: if you want to skip after appending the -1 in the self.magic initialization need change to a zero."""
        if self.substring == None or self.text == None:
            raise ValueError("Need to initialize inputs.")

        for i in xrange(self.wnd):
            self.u = (self.u * self.base + ord(self.text[i])) % self.p
            self.s = (self.s * self.base + ord(self.substring[i])) % self.p

        self.magic = pow(self.base, self.wnd - 1) % self.p



    def checkCorrect(self, pos):
        """Checks if a presumptive positive is a true positive O(len(substring)).
        False positives should occur 1/p times, so with a large p value they will not affect the amortized runtime."""
        if self.u != self.s:
            return False
        elif self.text[pos:pos + self.wnd] == self.substring:
            return True
        else:
            return False


    def findInstances(self, toPrint=True):
        """Finds and prints (if True) all instances of the substring in the text."""
        self.initializeValues()

        for s in xrange(self.textLen - self.wnd + 1):

            if self.checkCorrect(s):
                self.found.append(s)

            if s < self.textLen - self.wnd:
                self.skip(self.text[s])
                self.append(self.text[s + self.wnd])
                self.u = (self.u + self.p) % self.p

        if toPrint:
            print self.found



def test():
    t = RollingHash()
    t.setSubstring('class=')
    t.loadText('    <div class="testClass1 testClass2">', False)
    t.findInstances()

test()










#This is the Rabin-Karp algorithm I found on stack exchange after many hours trying to fix my own.
def Rabin_Karp_Matcher(text, pattern, d, q):
    n = len(text)
    m = len(pattern)
    h = pow(d, m - 1) % q
    p = 0
    t = 0
    result = []

    for i in range(m):  # preprocessing                 #appending everything in sequential order, starting with 0
        p = (d * p + ord(pattern[i])) % q                    #so p is the hash of the substring
        t = (d * t + ord(text[i])) % q                       #while t is the hash of the first window frame of the text

    for s in xrange(n - m + 1):  # note the +1

        #Checks for a match
        if p == t:  # check character by character
            match = True
            for i in range(m):
                if pattern[i] != text[s + i]:
                    match = False
                    break
            if match:
                result = result + [s]

        if s < n - m:
            t = (t - h * ord(text[s])) % q  # remove letter s
            t = (t * d + ord(text[s + m])) % q  # add letter s+m
            t = (t + q) % q  # make sure that t >= 0
    return result










