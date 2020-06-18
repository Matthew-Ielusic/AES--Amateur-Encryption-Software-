from . import Galois

class IntPolynomial: # Section 4.3: Degree-4 polynomial with coefficients in GF(2^8)
    def __init__(self, coefficients):
        # coefficients[i] should be the coefficient of the term with degree i
        # (EG, coefficients[0] should be the constant)
        if (len(coefficients)) != 4:
            raise ValueError("An IntPoy has 4 coefficients.  Actual coefficient list: " + str(coefficients) + "; len: " + str(len(coefficients)))
        if any([type(c) is not Galois.BytePolynomial for c in coefficients]):
            raise ValueError("An IntPoy has coefficients in GF(2^8).  Actual coefficient list: " + str(coefficients))
        self.coefficients = coefficients

    @staticmethod
    def zero():
        return IntPolynomial([Galois.zeroByte()] * 4)
    
    def __add__(self, other):
        # Section 4.3: "Addition is performed by adding the finite field
        # coefficients of like powers"
        sum = [self.coefficients[i] + other.coefficients[i] for i in range(4)]
        return IntPolynomial(sum)

    def __mul__(self, other):
        # Section 4.3: "Multiplication is achieved in two steps.
            # In the first step, the polynomial product c(x) = a(x) • b(x) is
            # algebraically expanded [...]
            # the result [is] reduced to a polynomial of degree less than 4.
            # For the AES algorithm, this is accomplished with the polynomial
            # x^4 + 1"
        
        # Calculate the product
        product = [Galois.zeroByte() for i in range(7)]
        for i in range(4):
            for j in range(4):
                product[i + j] += self.coefficients[i] * other.coefficients[j]

        # Reduce modulo x^4 + 1
        modulo_x4(product)
        return IntPolynomial(product[:4])

    def modularProduct(self, other):
        # Section 4.3: "The modular product of a(x) and b(x) [...] is given by the four-term polynomial d(x) [definition omitted]"
        d = [Galois.zeroByte() for i in range(4)]
        for i in range(4): # Index into self.coefficients
            for j in range(4): # Index into other.coefficients
                index = (i + j) % 4
                d[index] += self.coefficients[i] * other.coefficients[j]
        return IntPolynomial(d)

        
    def __str__(self):
        # Convienent string representation not described in the specification
        output = []
        for i in range(3, 1, -1): # 3, 2, 1
            byte = int(self.coefficients[i])
            if byte:
                if byte > 1:
                    output.append(str(byte) + "x^" + str(i))
                else:
                    output.append("x^" + str(i))
        if self.coefficients[1]:
            byte = int(self.coefficients[1])
            if byte:
                if byte > 1:
                    output.append(str(byte) + "x")# Not x^1
                else:
                    output.append("x")
        output.append(str(int(self.coefficients[0]))) # Certainly not x^0
        return " + ".join(output)

    def __eq__(self, other):
        if type(other) is IntPolynomial:
            matches = [
                        self.coefficients[i].coefficients == other.coefficients[i].coefficients 
                        for i in range(4)
                      ]
            return all(matches)
        else:
            return False

    def __int__(self):
        ints = [int(c) for c in self.coefficients]
        return sum([ints[i] << (i*8) for i in range(4)])

    def __getitem__(self, key):
        return self.coefficients[key]
    def __setitem__(self, key, value):
        self.coefficients[key] = value
                

# Special polynomial
def a():
    three = Galois.BytePolynomial([1, 1, 0, 0, 0, 0, 0, 0])
    two   = Galois.BytePolynomial([0, 1, 0, 0, 0, 0, 0, 0])
    one   = Galois.BytePolynomial([1, 0, 0, 0, 0, 0, 0, 0])
    return IntPolynomial([two, one, one, three])

def aInv():
    e    = Galois.BytePolynomial([0, 1, 1, 1, 0, 0, 0, 0])
    nine = Galois.BytePolynomial([1, 0, 0, 1, 0, 0, 0, 0])
    d    = Galois.BytePolynomial([1, 0, 1, 1, 0, 0, 0, 0])
    b    = Galois.BytePolynomial([1, 1, 0, 1, 0, 0, 0, 0])
    return IntPolynomial([e, nine, d, b])


# Another special polynomial
def xCubed():
    return IntPolynomial([Galois.zeroByte(), Galois.zeroByte(), Galois.zeroByte(), Galois.oneByte()])


def modulo_x4(coeffList):
    # We want to take a polynomial of degree <= 6 and reduce it modulo x^4 + 1
    # Call our polynomial h(x) = ax^6 + bx^5 + cx^4 + dx^3 + ex^2 + fx^1 + gx^0
    # We're just gonna subtract ax^2(x^4 + 1), bx(a^4 + 1), and  c(x^4 + 1) from h(x)
    # All the terms of degree 4 or more are cancelled out, leaving the remainder modulo x^4 + 1 
    degree = 6
    while degree >= 4:
        coeffList[degree - 4] -= coeffList[degree]
        coeffList[degree] = Galois.zeroByte()
        degree -= 1



def lsDegree(coeffList):
    nonzero = [any(c.coefficients) for c in coeffList].reverse()
    if any(nonzero):
        return nonzero.index(True)
    else:
        return 0

