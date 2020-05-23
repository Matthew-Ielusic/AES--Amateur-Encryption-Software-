# -*- coding: utf-8 -*-



import GeneralizedPoly # Used for the implementation of inverse

# Section 3.2: "bytes are interpreted as finite field elements using a [degree-7] polynomial representation" (The finite field being GF(2^8), IE Galois finite field with 2**8=256 elements)

class Polynomial: # Represents specifically a polynomial in GF(2^8)
    def __init__(self, coefficients=[0] * 8):
        # coefficients[i] should be the coefficient of the term with degree i
        # (EG, coefficients[0] should be the constant)
        if (len(coefficients)) != 8:
            raise ValueError("A polynomial in GF(2^8) has 8 coefficients.  Actual coefficient list: " + str(coefficients) + "; len: " + str(len(coefficients)))
        for i in coefficients:
            if not i in [0,1]:
                raise ValueError("A polynomial in GF(2^8) has coefficients of zero or one.  Actual coefficient list: " + str(coefficients))
        self.coefficients = coefficients[:]

    def __add__(self, other):
        # Section 4.1: "The addition of two elements in a finite field is achieved by 'adding' the coefficients for the corresponding powers in the polynomials for the two elements. The addition is performed with the XOR operation"
        new_coeff = [-1] * 8
        for i in range(8):
            new_coeff[i] = self.coefficients[i] ^ other.coefficients[i]
        return Polynomial(new_coeff)

    def __sub__(self, other):
        # Section 4.1: "subtraction of polynomials is identical to addition of polynomials."
        return self + other

    def __mul__(self, other):
        # "multiplication in GF(2^8) (denoted by •) corresponds with the multiplication of polynomials modulo an irreducible polynomial of degree 8."
        # Sadly, python Integer multiplication doesn't quite behave the same way as GF(2^8) polynomial multiplication.
        # EG: (x + 1)(x + 1) = x^2 + x + x + 1 = x^2 + 1 
        # But x + 1 = 1x^1 + 1x^0 corresponds to 3, x^2 + 1 = 1x^2 + 0x^1 + 1x^2 corresponds to 5, but 3*3 is not 5
        # Therefore, this implementation cannot something simple such as converting the coefficient arrays to Integers and multiplying.
        # (Section 4.2.1 describes a special-case implementation of multiplication by x^1, which is not implemented here for pedagogical reasons.)
        product = [0] * 15 # product of degree-7 polynomials is at most degree 14 (so 14+1 coefficients)
        for i in range(len(self.coefficients)): # Index into self.coefficients
            for j in range(len(other.coefficients)): # Index into other.coefficients
                term = self.coefficients[i] * other.coefficients[j]
                index = i + j
                product[index] ^= term # "add" (xor) terms of the same degree
        # Now that we have the product, possibly of degree 8 or more, modulo it with m = x^8 + x^4 + x^3 + x + 1
        # The algorithm is polynomial long division, discarding the quotient
        
        while lsDegree(product) > 8:
            factorDegree = lsDegree(product) - lsDegree(m())
            factor = ([0] * factorDegree) + m() # m() is a coefficient array
            for i in range(len(factor)):
                product[i] ^= factor[i] 

        return Polynomial(product[:8]) # Drop all but the first 8 coefficients  
    
    def __truediv__(self, other):
        # Polynomial long division
        if not any(other.coefficients):
            raise ZeroDivisionError # No coefficient of other is nonzero means other is zero
        quotient = Polynomial()
        remainder = Polynomial(self.coefficients)
        degreeDifference = lsDegree(remainder.coefficients) - lsDegree(other.coefficients)
        while degreeDifference >= 0 and any(remainder.coefficients):
            leftShift = ([0] * degreeDifference) + other.coefficients
            factor = Polynomial(leftShift[:8])
            remainder -= factor
            quotient.coefficients[degreeDifference] = 1
            degreeDifference = lsDegree(remainder.coefficients) - lsDegree(other.coefficients)
        return quotient
    
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


    def inverse(self):
        # EEA based off of wikipedia pseudocode
        old_s = GeneralizedPoly.GenPoly([1]) # IE, old_s = 1
        s = GeneralizedPoly.GenPoly([0]) #IE, s = 0
        old_t = GeneralizedPoly.GenPoly([0]) #IE, old_t = 0
        t = GeneralizedPoly.GenPoly([1]) # IE, t = 1
        old_r = GeneralizedPoly.GenPoly(m()) # m() returns a list of coefficients!
        r = GeneralizedPoly.GenPoly(self.coefficients)
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

    def degree(self):
        return lsDegree(self.coefficients)

    def copy(self):
        return Polynomial(self.coefficients)

def m():
    # Returns the coefficient array for the irreducible polynomial m used for multiplication
    return [1,1,0,1,1,0,0,0,1] # 1 + x + x^3 + x^4 + x^8

def mDegree():
    return 8

def mPoly():
    return GeneralizedPoly.GenPoly(m())

def modulo_m(poly):
    modulus = GeneralizedPoly.GenPoly(poly.coefficients)
    while modulus.degree() > 8:
        factorDegree = modulus.degree() - mDegree()
        factor = GeneralizedPoly.xToThe(factorDegree) * mPoly()
        modulus -= factor
    
    output = Polynomial()
    for i in range(len(modulus.coefficients)):
        output.coefficients[i] = modulus.coefficients[i]
    return output

def lsDegree(coefficients):
    # I can't find a simple way to find the index of last nonzero element of a list,
    # especially if the list may be all zeros
    for i in range(len(coefficients) - 1, 0, -1):
        if coefficients[i]:
            return i
    return 0 #0 has degree 0.