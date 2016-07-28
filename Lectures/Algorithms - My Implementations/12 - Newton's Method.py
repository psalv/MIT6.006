

#The decimal library is important for high precision computations.
from decimal import *
import math


def quad(x):
    """A test function, f(x) = x**2 - 2, the root should be sq. root 2."""
    return Decimal(x)**2 - 2
def derivQuad(x):
    """A test function, f'(x) = 2*x."""
    return Decimal(2)*x


def findKSigDigitsSqRoot(a, k=10, fl=1):
    """Takes in an a value and approximates the root of eq to k decimal points by Newton's Method.
    The initial floor condition, fl, is a guess we make. Often one that can be done easily by division.

    ex. If a is a very large number we may choose a power of two for easy shifting division."""

    # This line is necessary to lift the decimal limit (set to a default of 28 decimal points).
    getcontext().prec = k * 2
    iterations = int(math.ceil(math.log(k, 2)))     #Need log(k) iterations due to having quadratic convergence.

    numCorrect = 1
    Xn_1 = Decimal(fl)

    for i in xrange(iterations):
        Xn = Xn_1
        Xn_1 = (Xn + Decimal(a)/Xn)/2
        numCorrect *= 2

        # print "Digits correct: " + str(numCorrect) + ". Current estimate: " + str(Xn_1)
    print "\nIrrational to " + str(k) + " decimal points: " + str(Xn_1)[:k + 1]

    return Xn_1


def findKSigDigitsEquations(eq, derivEq, k=10, fl=1):
    """Uses two equations (eq and it's derivative) to approximate the root of eq to k decimal points by Newton's Method.
    I need to find a way to determine the floor of the function easily."""

    getcontext().prec = k * 2
    iterations = int(math.ceil(math.log(k, 2)))

    numCorrect = 1
    Xn_1 = Decimal(fl)

    for i in xrange(iterations):
        Xn = Xn_1
        Xn_1 = Xn - Decimal((eq(Xn)/derivEq(Xn)))
        numCorrect *= 2
    print "\nIrrational to " + str(k) + " decimal points: " + str(Xn_1)[:k + 1]

    return Xn_1


def letPythonDoItForMe():
    """Alternatively this type of approximation is already worked into python's standard libraries."""
    getcontext().prec = 70
    print "                                ", Decimal(2)**(Decimal(1)/2)


findKSigDigitsSqRoot(2, 70)
findKSigDigitsEquations(quad, derivQuad, 70)
letPythonDoItForMe()