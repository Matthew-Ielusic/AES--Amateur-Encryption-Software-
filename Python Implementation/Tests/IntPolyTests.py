# Hack sys.path to get code from the parent folder
import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir) 
# </hack>


import Implementation.FiniteField.IntPolynomial as IP
from Implementation.FiniteField import Galois
import unittest

class TestIntPoly(unittest.TestCase):
    def test_add(self):
        zeroEight  = Galois.BytePolynomial([0, 0, 0, 1, 0, 0, 0, 0])
        not0x08   = Galois.BytePolynomial([1, 1, 1, 0, 1, 1, 1, 1])
        f0  = Galois.BytePolynomial([0, 0, 0, 0, 1, 1, 1, 1])
        c8 = Galois.BytePolynomial([0, 0, 0, 1, 1, 0, 1, 1])
        twoEight = Galois.BytePolynomial([0, 0, 0, 1, 1, 0, 1, 1])
        zero   = Galois.zeroByte()
        ff     = Galois.BytePolynomial([1, 1, 1, 1, 1, 1, 1, 1])
        twoFour= Galois.BytePolynomial([0, 0, 1, 0, 0, 1, 0, 0])
        fc     = Galois.BytePolynomial([0, 0, 1, 1, 1, 1, 1, 1])

        x =        IP.IntPolynomial([zeroEight, f0, twoFour, zeroEight])
        y =        IP.IntPolynomial([zeroEight, zero,  c8,  ff])
        expected = IP.IntPolynomial([zero,  f0, fc,      not0x08])
        
        self.assertEqual(expected, x+y, "IntPolynomial's __add__ failed")

    def test_mult(self):
        x        = IP.IntPolynomial([Galois.BytePolynomial.fromInt(0x52),
                                   Galois.BytePolynomial.fromInt(0xa4),
                                   Galois.BytePolynomial.fromInt(0xc8),
                                   Galois.BytePolynomial.fromInt(0x94)])
        expected = IP.IntPolynomial([Galois.BytePolynomial.fromInt(0x0f),
                                   Galois.BytePolynomial.fromInt(0xd6),
                                   Galois.BytePolynomial.fromInt(0xda),
                                   Galois.BytePolynomial.fromInt(0xa9)])
        self.assertEqual(expected, x * IP.a(), "IntPolynomial's __mult__ failed")


if __name__ == '__main__':
    try:
        unittest.main()
    except SystemExit:
        # unittest & my IDE don't play nice
        # unittest raises a SystemExit when it finishes
        pass