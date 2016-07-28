
import random

class Grid(object):

    def __init__(self, m, n, r=9):
        """m x n matrix, so m is the number of rows and n i s the number of columns.
        r represents the range of weight values.

        Grid entries are of the form: (weight down, weight right)"""

        self.m = m
        self.n = n
        self.r = r
        self.grid = []

        for i in xrange(m):
            self.grid.append([])
            for j in xrange(n):
                self.grid[i].append([(random.randint(1, r), random.randint(1, r)), None])

    def getWeight(self, i, j, down=True):
        if down:
            d = 0
        else:
            d = 1
        return self.grid[i][j][0][d]

    def getPath(self, i, j):
        return self.grid[i][j][1]

    def setPath(self, i, j, p):
        self.grid[i][j][1] = p


    def __str__(self):
        toStr = ""
        for i in self.grid:
            toStr += str(i) + "\n"
        return toStr


def solve(grid, finish):
    i = finish[0]
    j = finish[1]

    if finish == (0, 0):
        grid.setPath(i, j, 0)

    elif finish[0] == 0:
        grid.setPath(i, j, grid.getWeight(0, j - 1, False) + grid.getPath(0, j - 1))

    elif finish[1] == 0:
        grid.setPath(i, j, grid.getWeight(i - 1, 0, True) + grid.getPath(i - 1, 0))

    else:
        grid.setPath(i, j, min(grid.getWeight(i - 1, j, True) + grid.getPath(i - 1, j), grid.getWeight(i, j - 1, False) + grid.getPath(i, j - 1)))




def findShortestPath(finish, size):
    """Starts in the top right corner, use optimal substructure to compute the shortest path to the finish.
    Operates udner the principle that the graph is already topologically sorted when viewed left > right, up > down.
    Works in O(V) time."""

    m = size[0]
    n = size[1]
    grid = Grid(m, n)
    print grid

    f = False
    for i in xrange(m):
        for j in xrange(n):
            solve(grid, (i, j))
            if (i, j) == finish:
                f = True
                break
        if f:
            break

    print grid
    return grid.getPath(finish[0], finish[1])



size = (3, 3)
start = (0, 0)
finish = (1, 1)
print findShortestPath(finish, size)



