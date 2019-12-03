# -*- coding: utf-8 -*-


class Polynomial: # Represents specifically a polynomial in GF(2^8)
    def __init__(self, coefficients=[0] * 8):
        if (len(coefficients)) != 8:
            raise ValueError("A polynomial in GF(2^8) has 8 coefficients.  Actual coefficient list: " + str(coefficients) + "; len: " + str(len(coefficients)))
        for i in coefficients:
            if not i in [0,1]:
                raise ValueError("A polynomial in GF(2^8) has coefficients of zero or one.  Actual coefficient list: " + str(coefficients))
        self.coefficients = coefficients
        
    def __add__(self, other):
        # Straightforward element-wise XOR
        new_coeff = [-1] * 8
        for i in range(8):
            new_coeff[i] = self.coefficients[i] ^ other.coefficients[i]
        return Polynomial(new_coeff)
    
    def __sub(self, other):
        return self + other # In GF(2^8), addition and subtraction are the same
    
    def __mul__(self, other):
        # Sadly we cannot convert the coefficient arrays to Integers and multiply,
        # because python Integer multiplication doesn't quite behave the same way as
        # GF(2^8) polynomial multiplication.
        # EG: (x + 1)(x + 1) = x^2 + x + x + 1 = x^2 + 1 
        # But x+1 converts to 3, x^2+1 converts to 5, and 3*3 is not 5
        product = [0] * 15 # product of degree-7 polynomials is at most degree 14 (so 14+1 coefficients)
        for i in range(len(self.coefficients)): # Index into self.coefficients
            for j in range(len(other.coefficients)): # Index into other.coefficients
                term = self.coefficients[i] * other.coefficients[j]
                index = i + j
                product[index] ^= term # "add" (xor) terms of the same degree
        # Now that we have the product, possibly of degree 8 or more, modulo it with m = x^8 + x^4 + x^3 + x + 1
        # The algorithm is polynomial long division, discarding the quotient
        while degree(product) > 8:
            factorDegree = degree(product) - degree(m())
            factor = ([0] * factorDegree) + m() # concatenate coefficient arrays
            for i in range(len(factor)):
                product[i] ^= factor[i] 
        return Polynomial(product[:8]) # Drop all but the first 8 coefficients     
    
    def __str__(self):
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

def m():
    return [1,1,0,1,1,0,0,0,1] # 1 + x + x^3 + x^4 + x^8
       
def degree(coefficients):
    for i in range(len(coefficients) - 1, 0, -1):
        if coefficients[i]:
            return i
    return 0 #1 has degree 0.  0 also has degree 0.

x = Polynomial([1,1,1,0,1,0,1,0])
y = Polynomial([1,1,0,0,0,0,0,1])
print("x:", x, sep=' ')
print("y:", y, sep=' ')
print("x+y:", x+y, sep=' ')
print("(Expected value: x^7 + x^6 + x^4 + x^2)")
print("x*y:", x*y, sep=' ')
print("(Expected value: x^7 + x^6 + 1)")
