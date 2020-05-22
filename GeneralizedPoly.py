class GenPoly: # Represents a generalized polynomial with coefficients of 0 or 1
    def __init__(self, coefficients=[0] * 8):
        # coefficients[i] should be the coefficient of the term with degree i
        # (EG, coefficients[0] should be the constant)
        for i in coefficients:
            if not i in [0,1]:
                raise ValueError("A polynomial in GF(2^8) has coefficients of zero or one.  Actual coefficient list: " + str(coefficients))
        self.coefficients = coefficients[:]

    def degree(self):
        return lsDegree(self.coefficients)
        
    def __len__(self):
        return len(self.coefficients)

    def __add__(self, other):
        highDegree = None
        lowDegree = None
        if self.degree() < other.degree():
            highDegree = other.coefficients
            lowDegree = self.coefficients
        else: 
            highDegree = self.coefficients
            lowDegree = other.coefficients
        
        output = highDegree[:]
        for i in range(lsDegree(lowDegree) + 1): #We have to be careful of having a most-significant-coefficient of 0
            output[i] ^= lowDegree[i]
        return GenPoly(output)
    
    def __sub__(self, other):
        # Section 4.1: "subtraction of polynomials is identical to addition of polynomials."
        return self + other
    
    def __mul__(self, other):
        # Just honking multiply the polynomials the hard way, and let EEA handle the fallout
        productLen = len(self) + len(other)
        product = [0] * productLen
        for i in range(len(self.coefficients)): # Index into self.coefficients
            for j in range(len(other.coefficients)): # Index into other.coefficients
                term = self.coefficients[i] * other.coefficients[j]
                index = i + j
                product[index] ^= term # "add" (xor) terms of the same degree
        # Problem: one of the coefficient arrays may have a most-significant-coefficient of zero
        # Solution: trim product of trailing zeros via array slices & degree()
        return GenPoly(product[:lsDegree(product) + 1])
    
    def __truediv__(self, other):
        # Polynomial long division
        if not any(other.coefficients):
            raise ZeroDivisionError # No coefficient of other is nonzero means other is zero
        quotient = GenPoly([0] * len(self.coefficients))
        remainder = GenPoly(self.coefficients)
        degreeDifference = remainder.degree() - other.degree()
        while degreeDifference >= 0 and any(remainder.coefficients):
            factor = xToThe(degreeDifference)
            remainder -= (factor * other)
            quotient.coefficients[degreeDifference] = 1
            degreeDifference = remainder.degree() - other.degree()
        quotient.trim()
        return quotient
    
    def inverse(self):
        raise NotImplementedError
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

    def trim(self):
        self.coefficients = self.coefficients[:self.degree() + 1]
                
            
            
    
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

def xToThe(n):
    leftPad = [0] * n;
    return GenPoly(leftPad + [1])

def one():
    return Polynomial([1,0,0,0,0,0,0,0])

def zero():
    return Polynomial([0,0,0,0,0,0,0,0])

       
def lsDegree(coefficients):
    # I can't find a simple way to find the index of last nonzero element of a list,
    # especially if the list may be all zeros
    for i in range(len(coefficients) - 1, 0, -1):
        if coefficients[i]:
            return i
    return 0 #0 has degree 0.