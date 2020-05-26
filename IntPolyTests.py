import IntPolynomial as IP
import Galois

zeroEight  = Galois.BytePolynomial([0, 0, 0, 1, 0, 0, 0, 0])
not0x08   = Galois.BytePolynomial([1, 1, 1, 0, 1, 1, 1, 1])
f0  = Galois.BytePolynomial([0, 0, 0, 0, 1, 1, 1, 1])
c8 = Galois.BytePolynomial([0, 0, 0, 1, 1, 0, 1, 1])
twoEight = Galois.BytePolynomial([0, 0, 0, 1, 1, 0, 1, 1])
zero   = Galois.zeroByte()
ff     = Galois.BytePolynomial([1, 1, 1, 1, 1, 1, 1, 1])
twoFour= Galois.BytePolynomial([0, 0, 1, 0, 0, 1, 0, 0])
fc     = Galois.BytePolynomial([0, 0, 1, 1, 1, 1, 1, 1])

print("Testing IntPolynomial.__plus__ ...")
def testAdd(x, y, expected):
    actual = x + y
    if actual != expected:
        print("add failed")
        print("x: ", x, sep='')
        print("y: ", y, sep='')
        print("sum:      ", actual, sep='')
        print("expected: ", expected, sep='')

x =        IP.IntPolynomial([zeroEight, f0, twoFour, zeroEight])
y =        IP.IntPolynomial([zeroEight, zero,  c8,  ff])
expected = IP.IntPolynomial([zero,  f0, fc,      not0x08])
testAdd(x, y, expected)


print("Testing IntPolynomial.__mul__ ...")
def testMult(x, y, expected):
    actual = x * y
    if actual != expected:
        print("multiplication failed")
        print("x: ", x, sep='')
        print("y: ", y, sep='')
        print("product:  ", actual, sep='')
        print("expected: ", expected, sep='')

one = IP.IntPolynomial([Galois.oneByte(), zero, zero, zero])
testMult(x, one, x)
testMult(one, y, y)
print("(",str(x),")", " * ", "(",str(y),")"," evaluates to ",str(x * y), sep='')
print("(That may or may not be correct)")


print("Testing modular product...")
print("(",str(x),")", " {modular product} ", "(",str(y),")"," evaluates to ",str(x.modularProduct(y)), sep='')
print("(That may or may not be correct)")

# Do __mul__  and modular product ultimately perform the same operation?
