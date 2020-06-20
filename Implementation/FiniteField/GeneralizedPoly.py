# GenPoly tepresents a generalized polynomial (IE, of arbitrary degree) with coefficients of 0 or 1
class GenPoly: 
    def __init__(self, coefficients):
        if len(coefficients) == 0:
            raise ValueError("Empty coefficient array")
        # coefficients[i] should be the coefficient of the term with degree i
        # (EG, coefficients[0] should be the constant)

        # Error checking
        for i in coefficients:
            if not i in [0,1]:
                raise ValueError("GenPoly can have coefficients of 0 or 1.  Actual coefficient list: " + str(coefficients))
        self.coefficients = coefficients

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

    def trim(self):
        self.coefficients = self.coefficients[:self.degree() + 1]
    
    def __str__(self):
        # Convienent string representation not described in the specification
        output = []
        for i in range(len(self) - 1, 1, -1): # From top to bottom, except for the x^1 & x^0 terms
            if self.coefficients[i]:
                output.append("x^" + str(i))
        if len(self.coefficients) >= 2 and self.coefficients[1]:
            output.append("x") # Not x^1
        if self.coefficients[0]:
            output.append("1") # Certainly not x^0
        if any(output):
            return " + ".join(output)
        else:
            return "0"

    def __eq__(self, other):
        return self.coefficients == other.coefficients

    def copy(self):
        return GenPoly(self.coefficients)
    

def xToThe(n):
    leftPad = [0] * n;
    return GenPoly(leftPad + [1])
       
def lsDegree(coefficients):
    # I can't find a simple way to find the index of last nonzero element of a list,
    # especially if the list may be all zeros
    for i in range(len(coefficients) - 1, 0, -1):
        if coefficients[i]:
            return i
    return 0 #0 has degree 0.