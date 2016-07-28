

#Create a hashing class without chaining.


class openAddressingHash(object):
    """ADT that allows for hashing without chaining. Probes spots of an array to check which are available and inserts items appropriately.
    The linearHash method is slow and inefficient because it creates clusters of size O(lgn)."""
    def __init__(self, m=16):
        self.n = 0
        self.m = m
        self.hashed = []

        self.tableDouble()


    def tableDouble(self):
        """Either initializes a table of size m upon object creation, or doubles the table size, rehashing all of the current items."""
        if self.hashed == []:
            for i in xrange(self.m):
                self.hashed.append(None)
        else:
            self.m *= 2
            items = self.hashed[:]

            self.hashed = []
            for i in xrange(self.m):
                self.hashed.append(None)

            self.n = 0
            for k in items:
                if k in (None, "deleteMe"):
                    continue
                else:
                    self.insert(k)


    def insert(self, k):
        """Inserts an item, k, into the hash table. Will write over 'deleteMe' instances created by the delete method."""

        if float(self.n) / self.m > 0.6:
            self.tableDouble()

        i = 0
        while True:
            h = self.doubleHash(k, i)
            # h = self.linearHash(k, i)

            if self.hashed[h] in (None, "deleteMe"):

                if self.hashed[h] == "deleteMe":
                    self.hashed[h] = k
                    return
                else:
                    self.hashed[h] = k
                    self.n += 1
                    return

            else:
                i += 1


    def delete(self, k):
        """Finds and removes an item from the hashed array, replacing them with a 'deleteMe' object.
        Note: the 'deleteMe' objects still contribute to the load factor of the array."""
        h = self.search(k)
        if h == None:
            return
        else:
            self.hashed[h] = "deleteMe"


    def search(self, k):
        """Finds a key in the array using the hash function, and returns it's position if it is present."""
        i = 0
        while True:
            h = self.doubleHash(k, i)
            # h = self.linearHash(k, i)

            if self.hashed[h] == None:

                print "Key '" + str(k) + "' is not in the hash table."
                return None

            elif self.hashed[h] == k:
                return h

            else:
                i += 1


    def doubleHash(self, k, i):
        """h(k,i) = ( h1(k,i) + i*h2(k,i) ) % m, where h1 and h2 are regular hash functions.
        I am unsure if the method I have implemented below is sufficient.
        This method should nearly abide by the uniform hashing assumption."""
        return (hash(k) + i * hash(k)) % self.m


    def linearHash(self, k, i):
        """This is an inefficient hash method as it is prone to creating clusters.
        Clusters will be on average O(lgn) in length, and will slow all of the functions associated with this data type.
        doubleHash is a much better method for cluster avoidance, bringing one closer to the uniform hashing assumption."""
        return (hash(k) + i) % self.m






















# x = openAddressingHash()
#
# y = 'abcdsfhgggjhk'
# for i in y:
#     x.insert(i)
# # print x.n
# # print x.m
# print x.hashed
# x.delete('g')
# x.delete('g')
# x.search('c')
# x.search(20)
# print x.hashed

