

#Performs multiplication in O(n**lg3) time.

#######Currently only works for if both the length of x and y are equivalent and even numbered.




def katsubaMult(x, y, r=10):
    stringX = str(x)
    stringY = str(y)

    n = max(len(stringX), len(stringY))

    if len(stringX) < 4 and len(stringY) < 4:
        return x * y

    else:
        lengthX, lengthY = len(stringX), len(stringY)

        # print stringX, stringY

        x0, x1 = int(stringX[lengthX/2:]), int(stringX[:lengthX/2])
        y0, y1 = int(stringY[lengthY/2:]), int(stringY[:lengthY/2])

        z0 = katsubaMult(x0, y0)
        z2 = katsubaMult(x1, y1)

        z1 = (x0 + x1) * (y0 + y1) - z0 - z2

        return int(z2*(r**n) + z1*(r**(n/2.0)) + z0)


print 111111*222222
# print 1111*2222
print katsubaMult(111111, 222222)


