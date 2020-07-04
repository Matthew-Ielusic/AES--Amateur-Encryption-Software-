# -*- coding: utf-8 -*-

# Hack sys.path to get code from the parent folder
import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir) 
# </hack>


from Implementation.FiniteField.GeneralizedPoly import GenPoly
import unittest

class TestGenPoly(unittest.TestCase):
    def test_add(self):
        x =   GenPoly([1,0])
        y =   GenPoly([1,0,1])
        sum = GenPoly([0,0,1])
        self.assertEqual(sum, x+y, "GenPoly's __add__ failed")

        x =   GenPoly([1,1,1,0,1,0,1,0])
        y =   GenPoly([1,1,0,0,0,0,0,1])
        sum = GenPoly([0,0,1,0,1,0,1,1])
        self.assertEqual(sum, x+y, "GenPoly's __add__ failed")

    def test_mult(self):
        x =   GenPoly([1,1,1,0,1,0,1,0])
        y =   GenPoly([1,1,0,0,0,0,0,1])
        prd = GenPoly([1,0,0,1,1,1,1,0,1,1,0,1,0,1])
        self.assertEqual(prd, x*y, "GenPoly's __mul__ failed")

        x   = GenPoly([1, 0, 0, 0])
        y   = GenPoly([0, 1, 1, 1, 1, 1, 1])
        prd = GenPoly([0, 1, 1, 1, 1, 1, 1])
        self.assertEqual(prd, x*y, "GenPoly's __mul__ failed")

        x   = GenPoly([0, 1, 0, 0])
        y   = GenPoly([0, 1, 1, 1, 1, 1, 1])
        prd = GenPoly([0, 0, 1, 1, 1, 1, 1, 1])
        self.assertEqual(prd, x*y, "GenPoly's __mul__ failed")
        
        x   = GenPoly([1, 0, 1, 1])
        y   = GenPoly([0, 1, 1, 1, 0, 1, 1])
        prd = GenPoly([0, 1, 1, 0, 0, 1, 0, 1, 0, 1])
        self.assertEqual(prd, x*y, "GenPoly's __mul__ failed")

    def test_div(self):
        x   = GenPoly([0, 1, 1, 1, 1, 1, 1])
        y   = GenPoly([1, 0, 0, 0])
        quo = GenPoly([0, 1, 1, 1, 1, 1, 1])
        self.assertEqual(quo, x / y, "GenPoly's __truediv__ failed")

        x   = GenPoly([0, 1, 1, 1, 1, 1, 1])
        y   = GenPoly([1, 0, 0, 0])
        quo = GenPoly([0, 1, 1, 1, 1, 1, 1])
        self.assertEqual(quo, x / y, "GenPoly's __truediv__ failed")
        
        x   = GenPoly([0, 1, 1, 1, 1, 1, 1])
        y   = GenPoly([0, 1, 0, 0])
        quo = GenPoly([1, 1, 1, 1, 1, 1])
        self.assertEqual(quo, x / y, "GenPoly's __truediv__ failed")

        x   = GenPoly([0, 1, 1, 1, 1, 1, 1])
        y   = GenPoly([0, 0, 1, 0])
        quo = GenPoly([1, 1, 1, 1, 1])
        self.assertEqual(quo, x / y, "GenPoly's __truediv__ failed")

        x   = GenPoly([1, 1, 0, 1, 0, 1, 0, 0, 1, 0])
        y   = GenPoly([1, 0, 1, 0])
        quo = GenPoly([1, 0, 1, 1, 1, 0, 1])
        self.assertEqual(quo, x / y, "GenPoly's __truediv__ failed")

if __name__ == '__main__':
    try:
        unittest.main()
    except SystemExit:
        # unittest & my IDE don't play nice
        # unittest raises a SystemExit when it finishes
        pass