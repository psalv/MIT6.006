
from __future__ import print_function

def loadWords(file="test1"):
    file = open(file, "r")
    words = file.readline().split()
    return words



def greedyJustify(charLim=75):
    """An imperfect greedy text justification."""
    words = loadWords()
    c = 0
    for i in words:
        if c + len(i) <= charLim:
            c += len(i) + 1
            print(i + " ", end="")
        else:
            print()
            c = len(i) + 1
            print(i + " ", end="")



def badness(i, j, text, memo, charLim=75):
    totalWidth = -1

    if (i, j) in memo:
        totalWidth = memo[(i, j)]
        return (charLim - totalWidth) ** 3

    elif (i, j - 1) in memo:

        totalWidth = memo[(i, j - 1)] + len(text[j])

    elif (i + 1, j) in memo:

        totalWidth = memo[(i + 1, j)] + len(text[i])

    else:

        for w in text[i:j]:
            totalWidth += len(w) + 1


    if totalWidth > charLim:
        return "Z"

    else:
        memo[(i, j)] = totalWidth
        return (charLim - totalWidth)**3



def textJustify(start, words, memo, charLim=75):


    print("i have no idea what i'm doing")
    exit()

    if start == len(words) - 1:
        return 0

    pack = []

    for j in range(start + 1, len(words)):
        try:
            pack.append(textJustify(j, words, memo) + badness(start, j, words, memo))
        except TypeError:
            break

    print(pack, start)
    return min(pack)




def DPjustify():
    words = loadWords()
    memo = {}
    textJustify(0, words, memo)


DPjustify()
