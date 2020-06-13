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

def invSBox(value):
    # I could find the inverse, in GF(2), of an 8x8 matrix
    # Or I could copy-and-paste the handy table on page 22 of the documentation.
    # (And massage it a bit into python syntax
    inverseGrid = [0x52, 0x9, 0x6a, 0xd5, 0x30, 0x36, 0xa5, 0x38, 0xbf, 0x40, 0xa3, 0x9e, 0x81, 0xf3, 0xd7, 0xfb, 0x7c, 0xe3, 0x39, 0x82, 0x9b, 0x2f, 0xff, 0x87, 0x34, 0x8e, 0x43, 0x44, 0xc4, 0xde, 0xe9, 0xcb, 0x54, 0x7b, 0x94, 0x32, 0xa6, 0xc2, 0x23, 0x3d, 0xee, 0x4c, 0x95, 0xb, 0x42, 0xfa, 0xc3, 0x4e, 0x8, 0x2e, 0xa1, 0x66, 0x28, 0xd9, 0x24, 0xb2, 0x76, 0x5b, 0xa2, 0x49, 0x6d, 0x8b, 0xd1, 0x25, 0x72, 0xf8, 0xf6, 0x64, 0x86, 0x68, 0x98, 0x16, 0xd4, 0xa4, 0x5c, 0xcc, 0x5d, 0x65, 0xb6, 0x92, 0x6c, 0x70, 0x48, 0x50, 0xfd, 0xed, 0xb9, 0xda, 0x5e, 0x15, 0x46, 0x57, 0xa7, 0x8d, 0x9d, 0x84, 0x90, 0xd8, 0xab, 0x0, 0x8c, 0xbc, 0xd3, 0xa, 0xf7, 0xe4, 0x58, 0x5, 0xb8, 0xb3, 0x45, 0x6, 0xd0, 0x2c, 0x1e, 0x8f, 0xca, 0x3f, 0xf, 0x2, 0xc1, 0xaf, 0xbd, 0x3, 0x1, 0x13, 0x8a, 0x6b, 0x3a, 0x91, 0x11, 0x41, 0x4f, 0x67, 0xdc, 0xea, 0x97, 0xf2, 0xcf, 0xce, 0xf0, 0xb4, 0xe6, 0x73, 0x96, 0xac, 0x74, 0x22, 0xe7, 0xad, 0x35, 0x85, 0xe2, 0xf9, 0x37, 0xe8, 0x1c, 0x75, 0xdf, 0x6e, 0x47, 0xf1, 0x1a, 0x71, 0x1d, 0x29, 0xc5, 0x89, 0x6f, 0xb7, 0x62, 0xe, 0xaa, 0x18, 0xbe, 0x1b, 0xfc, 0x56, 0x3e, 0x4b, 0xc6, 0xd2, 0x79, 0x20, 0x9a, 0xdb, 0xc0, 0xfe, 0x78, 0xcd, 0x5a, 0xf4, 0x1f, 0xdd, 0xa8, 0x33, 0x88, 0x7, 0xc7, 0x31, 0xb1, 0x12, 0x10, 0x59, 0x27, 0x80, 0xec, 0x5f, 0x60, 0x51, 0x7f, 0xa9, 0x19, 0xb5, 0x4a, 0xd, 0x2d, 0xe5, 0x7a, 0x9f, 0x93, 0xc9, 0x9c, 0xef, 0xa0, 0xe0, 0x3b, 0x4d, 0xae, 0x2a, 0xf5, 0xb0, 0xc8, 0xeb, 0xbb, 0x3c, 0x83, 0x53, 0x99, 0x61, 0x17, 0x2b, 0x4, 0x7e, 0xba, 0x77, 0xd6, 0x26, 0xe1, 0x69, 0x14, 0x63, 0x55, 0x21, 0xc, 0x7d]
    return Galois.BytePolynomial.fromInt(inverseGrid[int(value)])

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