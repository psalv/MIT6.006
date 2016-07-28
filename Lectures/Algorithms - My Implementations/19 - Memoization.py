


def fastFib(n, memo={}):
    """Use memoization to keep track of which fibonacci numbers we have already computed and compute F(n) in O(n)."""
    if n in memo:
        return memo[n]

    if n <= 2:
        f = 1

    else:
        f = fastFib(n - 1, memo) + fastFib(n - 2, memo)

    memo[n] = f
    return f

# import sys
# sys.setrecursionlimit(1500)
# print fastFib(100)




def noRecursionFastFib(n):
    """A for loop accomplishes the same thing as above however does not require recursive calls."""
    fib = {}
    for i in xrange(1, n + 1):
        if i <= 2:
             f = 1
        else:
            f = fib[i - 1] + fib[i - 2]
        fib[i] = f
    return fib[n]

# print noRecursionFastFib(100000)


def noRecursionSaveSpaceFastFib(n):
    """Then we apply knowledge that we do not need to store every number, can save memory."""
    fib = [1, 1]
    for i in xrange(3, n + 1):
        f = fib[0] + fib[1]

        fib[0] = fib[1]
        fib[1] = f

    return fib[1]

# print noRecursionSaveSpaceFastFib(500000)


