
class GenPoly:


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