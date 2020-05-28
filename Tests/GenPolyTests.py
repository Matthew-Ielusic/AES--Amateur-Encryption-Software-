# -*- coding: utf-8 -*-

# Hack sys.path to get code from the parent folder
import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir) 
# </hack>


from GeneralizedPoly import GenPoly

print("Testing add...")


def testAdd(x, y, expected):
    actual = x + y
    if not (actual.coefficients == expected.coefficients):
        print("add failed")
        print("x: ", x, sep='')
        print("y: ", y, sep='')
        print("sum:      ", actual, sep='')
        print("expected: ", expected, sep='')

x =   GenPoly([1,0])
y =   GenPoly([1,0,1])
sum = GenPoly([0,0,1])
testAdd(x, y, sum)

x =   GenPoly([1,1,1,0,1,0,1,0])
y =   GenPoly([1,1,0,0,0,0,0,1])
sum = GenPoly([0,0,1,0,1,0,1,1])
testAdd(x,y,sum) 

x =   GenPoly([1, 0, 1, 0, 0, 1, 0, 1])
y =   GenPoly([0, 1, 0, 1, 1, 1])
sum = GenPoly([1, 1, 1, 1, 1, 0, 0, 1])
testAdd(x, y, sum)

print("Done.")

print("Testing multiplication...")

def testMult(x, y, expected):
    actual = x * y
    if not (actual.coefficients == expected.coefficients):
        print("multiplication failed")
        print("x: ", x, sep='')
        print("y: ", y, sep='')
        print("product:  ", actual, sep='')
        print("expected: ", expected, sep='')

x =   GenPoly([1,1,1,0,1,0,1,0])
y =   GenPoly([1,1,0,0,0,0,0,1])
prd = GenPoly([1,0,0,1,1,1,1,0,1,1,0,1,0,1])
testMult(x,y,prd) 

x   = GenPoly([1, 0, 0, 0])
y   = GenPoly([0, 1, 1, 1, 1, 1, 1])
prd = GenPoly([0, 1, 1, 1, 1, 1, 1])
testMult(x,y,prd) 

x   = GenPoly([1, 0, 0, 0])
y   = GenPoly([0, 1, 1, 1, 1, 1, 1])
prd = GenPoly([0, 1, 1, 1, 1, 1, 1])
testMult(x,y,prd) 

x   = GenPoly([0, 1, 0, 0])
y   = GenPoly([0, 1, 1, 1, 1, 1, 1])
prd = GenPoly([0, 0, 1, 1, 1, 1, 1, 1])
testMult(x,y,prd) 

x   = GenPoly([1, 0, 1, 1])
y   = GenPoly([0, 1, 1, 1, 0, 1, 1])
prd = GenPoly([0, 1, 1, 0, 0, 1, 0, 1, 0, 1])
testMult(x,y,prd) 
print("Done.")

print("Testing division...")

def testDiv(x, y, expected):
    actual = x / y
    if not (actual.coefficients == expected.coefficients):
        print("division failed")
        print("x: ", x, sep='')
        print("y: ", y, sep='')
        print("quotient: ", actual, sep='')
        print("expected: ", expected, sep='')

x   = GenPoly([0, 1, 1, 1, 1, 1, 1])
y   = GenPoly([1, 0, 0, 0])
quo = GenPoly([0, 1, 1, 1, 1, 1, 1])
testDiv(x, y, quo)

x   = GenPoly([0, 1, 1, 1, 1, 1, 1])
y   = GenPoly([1, 0, 0, 0])
quo = GenPoly([0, 1, 1, 1, 1, 1, 1])
testDiv(x, y, quo)

x   = GenPoly([0, 1, 1, 1, 1, 1, 1])
y   = GenPoly([0, 1, 0, 0])
quo = GenPoly([1, 1, 1, 1, 1, 1])
testDiv(x, y, quo)

x   = GenPoly([0, 1, 1, 1, 1, 1, 1])
y   = GenPoly([0, 0, 1, 0])
quo = GenPoly([1, 1, 1, 1, 1])
testDiv(x, y, quo)

x   = GenPoly([1, 1, 0, 1, 0, 1, 0, 0, 1, 0])
y   = GenPoly([1, 0, 1, 0])
quo = GenPoly([1, 0, 1, 1, 1, 0, 1])
testDiv(x, y, quo)

print("Done.")