# -*- coding: utf-8 -*-


class GenPoly: # Represents a generalized polynomial with coefficients of 0 or 1
    def __init__(self, coefficients=[0] * 8):
        # coefficients[i] should be the coefficient of the term with degree i
        # (EG, coefficients[0] should be the constant)
        for i in coefficients:
            if not i in [0,1]:
                raise ValueError("A polynomial in GF(2^8) has coefficients of zero or one.  Actual coefficient list: " + str(coefficients))
        self.coefficients = coefficients[:]

    def degree(self):
        return degree(self.coefficients)
        
    def __len__(self):
        return len(self.coefficients)

    def __add__(self, other):
        newLen = min(len(self), len(other))
        # Section 4.1: "The addition of two elements in a finite field is achieved by 'adding' the coefficients for the corresponding powers in the polynomials for the two elements. The addition is performed with the XOR operation"
        new_coeff = [-1] * newLen
        for i in range(newLen):
            new_coeff[i] = self.coefficients[i] ^ other.coefficients[i]
        return GenPoly(new_coeff)
    
    def __sub__(self, other):
        # Section 4.1: "subtraction of polynomials is identical to addition of polynomials."
        return self + other
    
    def __mul__(self, other):
        # Just honking multiply the polynomials the hard way, and let EEA handle the fallout
        productLen = len(self) * len(other)
        product = [0] * productLen
        for i in range(len(self.coefficients)): # Index into self.coefficients
            for j in range(len(other.coefficients)): # Index into other.coefficients
                term = self.coefficients[i] * other.coefficients[j]
                index = i + j
                product[index] ^= term # "add" (xor) terms of the same degree
        return GenPoly(product)
    
    def __truediv__(self, other):
        # Polynomial long division
        if not any(other.coefficients):
            raise ZeroDivisionError # No coefficient of other is nonzero means other is zero
        quotient = GenPoly()
        remainder = GenPoly(self.coefficients)
        degreeDifference = degree(remainder.coefficients) - degree(other.coefficients)
        while degreeDifference >= 0 and any(remainder.coefficients):
            leftShift = ([0] * degreeDifference) + other.coefficients
            factor = GenPoly(leftShift[:8])
            remainder -= factor
            quotient.coefficients[degreeDifference] = 1
            degreeDifference = degree(remainder.coefficients) - degree(other.coefficients)
        return quotient
    
    def inverse(self):
        # EEA based off of wikipedia pseudocode
        old_s = one()
        s = zero()
        old_t = zero()
        t = one()
        old_r = mPoly()
        r = self
        while any(r.coefficients):
            quotient = old_r / r
            (old_r, r) = (r, old_r - quotient * r)
            (old_s, s) = (s, old_s - quotient * s)
            (old_t, t) = (t, old_t - quotient * t)
        print("Bézout coefficients:", old_s, old_t, sep='')
        print("greatest common divisor:", old_r)
        print("quotients by the gcd:", t, s, sep='')
                
            
            
    
    def __str__(self):
        # Convienent string representation not described in the specification
        output = []
        for i in range(len(self) - 1, 1, -1): # 7, 6, 5, 4, 3, 2
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


def m():
    # Returns the coefficient array for the irreducible polynomial m used for multiplication
    return [1,1,0,1,1,0,0,0,1] # 1 + x + x^3 + x^4 + x^8
        
class mPoly:
    def __init__(self):
        self.coefficients = m()

    def __sub__(self, other):
        difference = mPoly()
        for i in range(len(other.coefficients)):
            difference.coefficients[i] ^= other.coefficients[i]
        return Polynomial()
        
    def __truediv__(self, other):
        # Polynomial long division
        if not any(other.coefficients):
            raise ZeroDivisionError # No coefficient of other is nonzero means other is zero

        quotient = Polynomial()

        degreeDifference = degree(self.coefficients) - degree(other.coefficients)
        quotient.coefficients[degreeDifference] = 1

        # Assume `other` is a Polynomial, with degree <= 8
        # Special handling for the first iteration, where `remainder` is m, which has too many coefficients

        factorCoefficients = ([0] * degreeDifference) + other.coefficients
        remainderCoefficients = self.coefficients[:]
        for i in range(9):
            remainderCoefficients[i] ^= factorCoefficients[i]
        
        remainder = Polynomial(remainderCoefficients[:8])
        degreeDifference = degree(remainder.coefficients) - degree(other.coefficients)
        while degreeDifference >= 0 and any(remainder.coefficients):
            quotient.coefficients[degreeDifference] = 1
            
            factorCoeff = ([0] * degreeDifference) + other.coefficients
            factor = Polynomial(factorCoeff)
            remainder -= factor
            degreeDifference = degree(remainder.coefficients) - degree(other.coefficients)
        return quotient


    def __str__(self):
        return "x^8 + x^4 + x^3 + x +1"
        #
        #remainder = Polynomial(m())
        #degreeDifference = degree(remainder.coefficients) - degree(other.coefficients)
        #while degreeDifference >= 0 and any(remainder.coefficients):
        #    leftShift = ([0] * degreeDifference) + other.coefficients
        #    factor = Polynomial(leftShift[:8])
        #    remainder -= factor
        #    quotient.coefficients[degreeDifference] = 1
        #    degreeDifference = degree(remainder.coefficients) - degree(other.coefficients)
        #return quotient


def one():
    return Polynomial([1,0,0,0,0,0,0,0])

def zero():
    return Polynomial([0,0,0,0,0,0,0,0])

       
def degree(coefficients):
    # I can't find a simple way to find the index of last nonzero element of a list,
    # especially if the list may be all zeros
    for i in range(len(coefficients) - 1, 0, -1):
        if coefficients[i]:
            return i
    return 0 #0 has degree 0.


em = mPoly()
q = GenPoly([1,0,0,0,1,1,1,1])
r = GenPoly([0,0,1,1,0,1])
print(q)
print(r)
print(q+r)
print(q-r)
print(q*r)
print(q/r)