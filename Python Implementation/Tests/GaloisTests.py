# -*- coding: utf-8 -*-

# Hack sys.path to get code from the parent folder
import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir) 
# </hack>

from Implementation.FiniteField.Galois import BytePolynomial
import unittest

class TestBytePoly(unittest.TestCase):
    def test_add(self):
        x =   BytePolynomial([1,1,1,0,1,0,1,0])
        y =   BytePolynomial([1,1,0,0,0,0,0,1])
        sum = BytePolynomial([0,0,1,0,1,0,1,1])
        self.assertEqual(sum, x+y, "BytePolynomial's __add__ failed")

    def test_mult(self):
        x =       BytePolynomial([1,1,1,0,1,0,1,0])
        y =       BytePolynomial([1,1,0,0,0,0,0,1]) 
        product = BytePolynomial([1,0,0,0,0,0,1,1])
        self.assertEqual(product, x*y, "BytePolynomial's __mul__ failed")
        self.assertEqual(product, y*x, "BytePolynomial's __mul__ failed")
    
    def test_div(self):
        x    =   BytePolynomial([1,1,1,0,1,0,1,0])
        y    =   BytePolynomial([1,1,0,0,0,0,0,1])
        deg7 = BytePolynomial([0,0,0,0,0,0,0,1])
        deg0 = BytePolynomial([1,0,0,0,0,0,0,0])
        deg2 = BytePolynomial([1,0,1,0,0,0,0,0]) #x^2 + 1
        deg1 = BytePolynomial([1,1,0,0,0,0,0,0]) #x + 1
        zero = BytePolynomial([0,0,0,0,0,0,0,0])
        self.assertEqual(zero, zero / deg7, "BytePolynomial's __truediv__ failed")
        self.assertEqual(zero, zero / deg2, "BytePolynomial's __truediv__ failed")
        self.assertEqual(deg1, deg2 / deg1, "BytePolynomial's __truediv__ failed")
        self.assertEqual(x, x / deg0, "BytePolynomial's __truediv__ failed")
        self.assertEqual(y, y / deg0, "BytePolynomial's __truediv__ failed")
        self.assertEqual(zero, x / y ,"BytePolynomial's __truediv__ failed") 
        self.assertEqual(BytePolynomial([0,1,1,1,1,1,1,0]), y / deg1,"BytePolynomial's __truediv__ failed")

    def test_inverse(self):
        x = BytePolynomial([0,1,0,0,0,0,0,0])
        xInverse = BytePolynomial([1, 0, 1, 1, 0, 0, 0, 1])
        self.assertEqual(xInverse, x.inverse(), "BytePolynomial's inverse failed")
        self.assertEqual(x, xInverse.inverse(), "BytePolynomial's inverse failed")
        one = BytePolynomial([1,0,0,0,0,0,0,0])
        self.assertEqual(one, x * xInverse, "BytePolynomial times its inverse was not one")

    def test_fromInt(self):
        c3 = BytePolynomial([0, 0, 1, 1, 1, 1, 0, 0])
        c3Int = 0x3c # Little Endian vs Big Endian
        actual = BytePolynomial.fromInt(c3Int)
        self.assertEqual(c3, actual, "BytePolynomial's fromInt failed")

if __name__ == '__main__':
    try:
        unittest.main()
    except SystemExit:
        # unittest & my IDE don't play nice
        # unittest raises a SystemExit when it finishes
        pass


