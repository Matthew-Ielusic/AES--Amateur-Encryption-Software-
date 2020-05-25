import IntPolynomial as IP
import Galois

eight  = Galois.BytePolynomial([0, 0, 0, 1, 0, 0, 0, 0])
not8   = Galois.BytePolynomial([1, 1, 1, 0, 1, 1, 1, 1])
zeroF  = Galois.BytePolynomial([0, 0, 0, 0, 1, 1, 1, 1])
eightC = Galois.BytePolynomial([0, 0, 0, 1, 1, 0, 1, 1])
eight2 = Galois.BytePolynomial([0, 0, 0, 1, 1, 0, 1, 1])
zero   = Galois.zeroByte()
ff     = Galois.BytePolynomial([1, 1, 1, 1, 1, 1, 1, 1])
fourTwo= Galois.BytePolynomial([0, 0, 1, 0, 0, 1, 0, 0])
cf     = Galois.BytePolynomial([0, 0, 1, 1, 1, 1, 1, 1])

print("Testing IntPolynomial.__plus__ ...")
def testAdd(x, y, expected):
    actual = x + y
    if actual != expected:
        print("add failed")
        print("x: ", x, sep='')
        print("y: ", y, sep='')
        print("sum:      ", actual, sep='')
        print("expected: ", expected, sep='')

x =        IP.IntPolynomial([eight, zeroF, fourTwo, eight])
y =        IP.IntPolynomial([eight, zero,  eightC,  ff])
expected = IP.IntPolynomial([zero,  zeroF, cf,      not8])
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
