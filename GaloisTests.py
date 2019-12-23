# -*- coding: utf-8 -*-

from Galois import Polynomial

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
        
        
        
x = Polynomial([1,1,1,0,1,0,1,0])
y = Polynomial([1,1,0,0,0,0,0,1])

added = Polynomial([0,0,1,0,1,0,1,1])
multiplied = Polynomial([1,0,0,0,0,0,1,1])

testAdd(x,y,added) # Add is simple
testMult(x,y,multiplied) # Multiplication is complex, but there is a complicated test case

# Let's do a lot of testing of division

deg7 = Polynomial([0,0,0,0,0,0,0,1])
deg0 = Polynomial([1,0,0,0,0,0,0,0])
deg2 = Polynomial([1,0,1,0,0,0,0,0]) #x^2 + 1
deg1 = Polynomial([1,1,0,0,0,0,0,0]) #x + 1
zero = Polynomial()
testDiv(zero, deg7, zero)
testDiv(zero, deg2, zero)
testDiv(deg2, deg1, deg1)
testDiv(x, deg0, x)
testDiv(y, deg0, y)
testDiv(x,y,zero) 
testDiv(y,deg1,Polynomial([0,1,1,1,1,1,1,0]))

print("done")
