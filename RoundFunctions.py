import Galois
import IntPolynomial
import numpy
import operator 
import functools

class State:
    # Section 5.1: "At the start of the Cipher, the input is copied to the State array using the conventions described in Sec. 3.4."
    # Section 3.4: " the AES algorithm’s operations are performed on a two-dimensional array of bytes called the State. 
    #                   The State consists of four rows of bytes, each containing Nb bytes, where Nb is [4].
    #                   In the State array denoted by the symbol s, each individual byte has two indices, with its row number r [...] and its column number c."
    # Section 5.1 Pseudocode: The state array is taken by transforming a flat array of 16 bytes into a 4x4 array of bytes
    def __init__(self, input):
        self.data = [[input[row * 4 + column] for row in range(4)] for column in range(4)]
     # Section 3.4, Figure 3: s[r,c] = in[4*r + c]

    @staticmethod
    def from4x4(input):
        if len(input) != 4 or any([len(ls) != 4 for ls in input]):
            raise ValueError("The input was not a 4x4 list.  input: " + str(input))
        out = State(range(16))
        out.data = input[:4][:4]
        return out

    def __getitem__(self, key):
         return self.data[key]

    def getColumn(self, columnIndex):
         return [self[i][columnIndex] for i in range(4)]

    def setColumn(self, columnIndex, newColumn):
         for i in range(4):
             self[i][columnIndex] = newColumn[i]

    def asList(self):
        # Column 0 is self.asList[0:4], column 1 is self.asList()[4:8], and so on
        return [int(self.data[c][r]) for r in range(4) for c in range(4)]


def sBoxMatrix():
    matrix = [ [int(((i + j) % 8) >= 3) for j in range(8)] for i in range(8)]
    matrix.reverse()
    return matrix

def invSBoxMatrix():
    # "I have nothing to offer but blood, toil, tears and sweat" (and manually-calculated inverses of 8x8 matrices under GF(2))
    return [
            [0,0,1,0,0,1,0,1],
            [1,0,0,1,0,0,1,0],
            [0,1,0,0,1,0,0,1],
            [1,0,1,0,0,1,0,0],
            [0,1,0,1,0,0,1,0],
            [0,0,1,0,1,0,0,1],
            [1,0,0,1,0,1,0,0],
            [0,1,0,0,1,0,1,0]
           ]

def sBoxVector():
    return [1,1,0,0,0,1,1,0]

def gf2MatMul(matrix, vector):
    # Multiplies a matrix by a vector in GF(2)
    # (IE, we combine elements with XOR, not addition)
    elementwiseProduct = [[row[i] * vector[i] for i in range(8)] for row in matrix]
    reduced =[ functools.reduce(operator.xor, row, 0) for row in elementwiseProduct ]
    return reduced

def sBox(initial):
    # I could type out the entire 16x16 grid in Figure 7, but the maths are so elegant
    inverse = initial.inverse()
    product = gf2MatMul(sBoxMatrix(), inverse.coefficients) 
    sum = numpy.bitwise_xor(product, sBoxVector()).tolist()
    return Galois.BytePolynomial(sum)

def SubBytes(state):
    for r in range(4):
        for c in range(4):
            state[r][c] = sBox(state[r][c])

def ShiftRows(state):
    for r in range(1, 4): # ShiftRows does not change row 0
        old = state[r][:]
        for c in range(4):
            state[r][c] = old[(c + r) % 4]

def MixColumns(state):
    columns     = [state.getColumn(i) for i in range(4)]
    polys       = [IntPolynomial.IntPolynomial(col) for col in columns]
    products    = [poly * IntPolynomial.a() for poly in polys]
    newColumns  = [[poly.coefficients[i] for i in range(4)]  for poly in products]
    for i in range(4):
        state.setColumn(i, newColumns[i])


def AddRoundKey(state, roundKeys):
    for r in range(4):
        for c in range(4):
            state[r][c] = state[r][c] + roundKeys[c][3-r]

            
def invShiftRows(state):
    for r in range(1, 4): 
        old = state[r][:]
        for c in range(4):
            state[r][c] = old[(c - r) % 4]

def invSBox(initial):
    # Section 5.3.2: "the inverse of the affine transformation (5.1) followed by taking the multiplicative inverse in GF(2^8)."
    # That affine transformation is a matrix multiplication and then a vector addition
    # The inverse is the vector addition (XOR is its own inverse) followed by multiplication by the inverse of that matrix
    sum = numpy.bitwise_xor(initial.coefficients, sBoxVector()).tolist()
    product = gf2MatMul(invSBoxMatrix(), sum)
    inverse = Galois.BytePolynomial(product).inverse()
    return inverse

    return Galois.BytePolynomial(sum)
def invSubBytes(state):
    for r in range(4):
        for c in range(4):
            state[r][c] = invSBox(state[r][c])

def invMixColumns(state):
    columns     = [state.getColumn(i) for i in range(4)]
    polys       = [IntPolynomial.IntPolynomial(col) for col in columns]
    products    = [poly * IntPolynomial.aInv() for poly in polys]
    newColumns  = [[poly.coefficients[i] for i in range(4)]  for poly in products]
    for i in range(4):
        state.setColumn(i, newColumns[i])