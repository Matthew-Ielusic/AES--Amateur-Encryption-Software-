# -*- coding: utf-8 -*-

from Galois import BytePolynomial

def testAdd(x, y, expected):
    actual = x + y
    if not (actual.coefficients == expected.coefficients):
        print("add failed")
        print("x: ", x, sep='')
        print("y: ", y, sep='')
        print("sum: ", actual, sep='')
        print("expected: ", expected, sep='')
        
def testMult(x, y, expected):
    actual = x * y
    if not (actual.coefficients == expected.coefficients):
        print("multiplication failed")
        print("x: ", x, sep='')
        print("y: ", y, sep='')
        print("product: ", actual, sep='')
        print("expected: ", expected, sep='')
        
def testDiv(x, y, expected):
    actual = x / y
    if not (actual.coefficients == expected.coefficients):
        print("division failed")
        print("x: ", x, sep='')
        print("y: ", y, sep='')
        print("quotient: ", actual, sep='')
        print("expected: ", expected, sep='')
        
        
        
x = BytePolynomial([1,1,1,0,1,0,1,0])
y = BytePolynomial([1,1,0,0,0,0,0,1])

added = BytePolynomial([0,0,1,0,1,0,1,1])
multiplied = BytePolynomial([1,0,0,0,0,0,1,1])

print("Testing add...")
testAdd(x,y,added) # Add is simple
print("Done.")

print("Testing multiplication...")
testMult(x,y,multiplied) # Multiplication is complex, but there is a complicated test case
print("Done.")

# Let's do a lot of testing of division

print("Testing division...")
deg7 = BytePolynomial([0,0,0,0,0,0,0,1])
deg0 = BytePolynomial([1,0,0,0,0,0,0,0])
deg2 = BytePolynomial([1,0,1,0,0,0,0,0]) #x^2 + 1
deg1 = BytePolynomial([1,1,0,0,0,0,0,0]) #x + 1
zero = BytePolynomial([0,0,0,0,0,0,0,0])
testDiv(zero, deg7, zero)
testDiv(zero, deg2, zero)
testDiv(deg2, deg1, deg1)
testDiv(x, deg0, x)
testDiv(y, deg0, y)
testDiv(x,y,zero) 
testDiv(y,deg1,BytePolynomial([0,1,1,1,1,1,1,0]))
print("Done.")

print("Testing inverse...")

def testInverse(x, expected):
    actual = x.inverse()
    if not (actual.coefficients == expected.coefficients):
        print("inverse failed")
        print("x: ", x, sep='')
        print("actual: ", actual, sep='')
        print("expected: ", expected, sep='')
       
x = BytePolynomial([0,1,0,0,0,0,0,0])
xInverse = BytePolynomial([1, 0, 1, 1, 0, 0, 0, 1])
testInverse(x, xInverse)
testInverse(xInverse, x)
testMult(x, xInverse, BytePolynomial([1,0,0,0,0,0,0,0]))
print("Done")