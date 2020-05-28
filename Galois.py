# -*- coding: utf-8 -*-

from GeneralizedPoly import GenPoly
import GeneralizedPoly
# Section 3.2: "bytes are interpreted as finite field elements using a [degree-7] polynomial representation" (The finite field being GF(2^8), IE Galois finite field with 2**8=256 elements)

class BytePolynomial: # Represents specifically a polynomial in GF(2^8) OR an eight-bit byte
    def __init__(self, coefficients):
        # coefficients[i] should be the coefficient of the term with degree i
        # (EG, coefficients[0] should be the constant)
        if (len(coefficients)) != 8:
            raise ValueError("A polynomial in GF(2^8) has 8 coefficients.  Actual coefficient list: " + str(coefficients) + "; len: " + str(len(coefficients)))
        for i in coefficients:
            if not i in [0,1]:
                raise ValueError("A polynomial in GF(2^8) has coefficients of zero or one.  Actual coefficient list: " + str(coefficients))
        self.coefficients = coefficients

    @staticmethod
    def fromInt(x):
        x = int(x)
        if x < 0 or x > 255:
            raise ValueError("Tried to make a value of " + str(x) + " into a byte")
        masked = [x & (1 << i) for i in range(8)]
        bits = [masked[i] >> i for i in range(8)]
        return BytePolynomial(bits)

    def __add__(self, other):
        # Section 4.1: "The addition of two elements in a finite field is achieved by 'adding' the coefficients for the corresponding powers in the polynomials for the two elements. The addition is performed with the XOR operation"
        new_coeff = [-1] * 8
        for i in range(8):
            new_coeff[i] = self.coefficients[i] ^ other.coefficients[i]
        return BytePolynomial(new_coeff)

    def __sub__(self, other):
        # Section 4.1: "subtraction of polynomials is identical to addition of polynomials."
        return self + other

    def __mul__(self, other):
        # "multiplication in GF(2^8) (denoted by •) corresponds with the multiplication of polynomials modulo an irreducible polynomial of degree 8."
        product = self.asGenPoly() * other.asGenPoly()
        # Defer implementation of multiplation to that in GenPoly

        # But then return the product modulo m = 1 + x + x^3 + x^4 + x^8
        return modulo_m(product)
    
    def __truediv__(self, other):
        # Polynomial long division
        quotient = self.asGenPoly() / other.asGenPoly()
        return toBytePolynomial(quotient)
    
    def __str__(self):
        # Convienent string representation not described in the specification
        output = []
        for i in range(7, 1, -1): # 7, 6, 5, 4, 3, 2
            if self.coefficients[i]:
                output.append("x^" + str(i))
        if self.coefficients[1]:
            output.append("x") # Not x^1
        if self.coefficients[0]:
            output.append("1") # Certainly not x^0
        if any(output):
            return " + ".join(output)
        else:
            return "0"

    def __bool__(self):
        return any(self.coefficients)

    def __pow__(self, power):
        output = oneByte()
        while power > 0:
            power -= 1
            output *= self
        return output


    def inverse(self):
        if not any(self.coefficients):
            # Special case -- `self` is zero
            # Section 5.1.1: "Take the multiplicative inverse [...] the element {00} is mapped to itself"
            return zeroByte()

        # EEA based off of wikipedia pseudocode
        old_s = GenPoly([1]) # IE, old_s = 1
        s = GenPoly([0]) #IE, s = 0
        old_t = GenPoly([0]) #IE, old_t = 0
        t = GenPoly([1]) # IE, t = 1
        old_r = m()
        r = GenPoly(self.coefficients)
        while any(r.coefficients):
            quotient = old_r / r
            (old_r, r) = (r, old_r - quotient * r)
            (old_s, s) = (s, old_s - quotient * s)
            (old_t, t) = (t, old_t - quotient * t)

        # At this point:
        # self * old_t = m() * old_s
        # So by section 4.2, the inverse of self is old_t % m()
       
        return modulo_m(old_t)

        # Just in case...
        #print("Bézout coefficients:", old_s, old_t, sep=',')
        #print("greatest common divisor:", old_r)
        #print("quotients by the gcd:", t, s, sep=',')

    def __eq__(self, other):
        return self.coefficients == other.coefficients

    def degree(self):
        return lsDegree(self.coefficients)

    def copy(self):
        return BytePolynomial(self.coefficients[:])

    def asGenPoly(self):
        return GenPoly(self.coefficients[:])

    def __int__(self):
        output = 0
        for i in range(8):
            if self.coefficients[i]:
                output += 2 ** i
        return output



 

def zeroByte():
    return BytePolynomial([0] * 8)

def oneByte():
    output = BytePolynomial([0] * 8)
    output.coefficients[0] = 1
    return output

def mCoefficients():
    # Returns the coefficient array for the irreducible polynomial m used for multiplication
    return [1,1,0,1,1,0,0,0,1] # 1 + x + x^3 + x^4 + x^8

def mDegree():
    return 8

def m():
    return GenPoly(mCoefficients())

def toBytePolynomial(genPoly):
    if len(genPoly.coefficients) > 8:
        return BytePolynomial(genPoly.coefficients[:8])
    else:
        coeff = genPoly.coefficients + ([0] * (8 - len(genPoly.coefficients)))
        return BytePolynomial(coeff)

def modulo_m(poly):
    # Polynomial long division by m, but return the remainder
    remainder = GenPoly(poly.coefficients)
    divisor = m()
    degreeDifference = remainder.degree() - mDegree()
    while degreeDifference >= 0 and any(remainder.coefficients):
        factor = GeneralizedPoly.xToThe(degreeDifference)
        remainder -= (factor * divisor)
        degreeDifference = remainder.degree() - mDegree()
    # Repeated calls to trim() in GenPoly.__sub__ mean len(remainder.coefficients) <= 8
    # But now we need to pad it to be 8 ints long
    return toBytePolynomial(remainder)

def lsDegree(coefficients):
    # I can't find a simple way to find the index of last nonzero element of a list,
    # especially if the list may be all zeros
    for i in range(len(coefficients) - 1, 0, -1):
        if coefficients[i]:
            return i
    return 0 #0 has degree 0.

