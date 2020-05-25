import Galois
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

    def __getitem__(self, key):
         return self.data[key]


def sBoxMatrix():
    matrix = [ [int(((i + j) % 8) >= 3) for j in range(8)] for i in range(8)]
    matrix.reverse()
    return matrix

def sBoxVector():
    return [1,1,0,0,0,1,1,0]

def gf2MatMul(matrix, vector):
    elementwiseProduct = [[row[i] * vector[i] for i in range(8)] for row in matrix]
    reduced =[ functools.reduce(operator.xor, row, 0) for row in elementwiseProduct]
    return reduced

def sBox(initial):
    # I could type out the entire 16x16 grid in Figure 7, but the maths are so elegant
    inverse = initial.inverse() # Inverse should be correct
    # Unfortunately, we can't use numpy.matmul because we need bits to be xor-ed together, not added
    product = gf2MatMul(sBoxMatrix(), inverse.coefficients) # So the problem is here
    sum = numpy.bitwise_xor(product, sBoxVector()).tolist()
    return Galois.BytePolynomial(sum)

def SubBytes(state):
    for r in range(4):
        for c in range(4):
            state[r][c] = sBox(state[r][c])