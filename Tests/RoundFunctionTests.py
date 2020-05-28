# Hack sys.path to get code from the parent folder
import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir) 
# </hack>

import RoundFunctions
import Galois
import IntPolynomial

input = [Galois.BytePolynomial.fromInt(i) for i in range(16)]
state = RoundFunctions.State(input)

print("Testing indexing...")
for row in range(4):
	for column in range(4):
		expected = input[column * 4 + row]
		actual = state.data[row][column]
		assert actual == expected, "state.data[r][c] failed -- expected " + str(expected) + "; got " + str(actual)
		
		actual = state[row][column]
		assert actual == expected, "state[r][c] failed -- expected " + str(expected) + "; got " + str(actual)
print("Done.")
print("Testing setting...")

value = Galois.BytePolynomial.fromInt(252)
state.data[1][2] = value
expected = value
actual = state.data[1][2]
assert actual == expected, "setting via state.data failed -- expected " + str(expected) + "; got " + str(actual)
state[3][2] = value
actual = state[3][2]
assert actual == expected, "setting via state.__getitem__ failed -- expected " + str(expected) + "; got " + str(actual)
print("Done.")


print("Testing the substitution box")
ff = Galois.BytePolynomial.fromInt(0xff)
expected = Galois.BytePolynomial.fromInt(0x16)
assert RoundFunctions.sBox(ff) == expected, "sBox(" + str(int(ff)) + ") was " + hex(int(expected)) + ", not 0x16"

ab = Galois.BytePolynomial.fromInt(0xab)
expected = Galois.BytePolynomial.fromInt(0x62)
assert RoundFunctions.sBox(ab) == expected, "sBox(" + str(int(ab)) + ") was " + hex(int(expected)) + ", not 0x62"

zero = Galois.zeroByte()
expected = Galois.BytePolynomial.fromInt(0x63)
assert RoundFunctions.sBox(zero) == expected, "sBox(" + str(int(zero)) + ") was " + hex(int(expected)) + ", not 0x63"

print("Done.")
print("Testing ShiftRows")
original =  RoundFunctions.State(input)
state	 = RoundFunctions.State(input)
RoundFunctions.ShiftRows(state)
for r in range(4):
	for c in range(4):
		assert state[r][c] == original[r][(c + r) % 4], "The byte in row " + str(r) + " and column " + str(c) + " was not shifted correctly."

print("Done.")
print("Testing MixColumns")

aesExampleBytes = [[0x52, 0x85, 0xe3, 0xf6], [0xa4, 0x11, 0xcf, 0x50], [0xc8, 0x6a, 0x2f, 0x5e], [0x94, 0x28, 0xd7, 0x07]]
state = RoundFunctions.State.from4x4([[Galois.BytePolynomial.fromInt(x) for x in y] for y in aesExampleBytes])
RoundFunctions.MixColumns(state)
bytesExpected = [[0x0f, 0x60, 0x6f, 0x5e], [0xd6, 0x31, 0xc0, 0xb3], [0xda, 0x38, 0x10, 0x13], [0xa9, 0xbf, 0x6b, 0x01]]
bytesActual   = [[int(state[r][c]) for c in range(4)] for r in range(4)]
assert bytesExpected == bytesActual, "MixColumns did not mix correctly.  Expected " + str(bytesExpected) + "; actual: " + str(bytesActual)

print("Done.")
print("Testing AddRoundKey")
raise NotImplementedError
input = [Galois.BytePolynomial.fromInt(i) for i in range(16)]
state = RoundFunctions.State(input)
roundKey = [IntPolynomial.IntPolynomial([Galois.BytePolynomial.fromInt(i*4) for i in range(4)])]*4
RoundFunctions.AddRoundKey(state, roundKey)
for r in range(4):
	for c in range(4):
		expected = None #???
		assert int(state[r][c]) == expected, f'Expected {expected}, got {state[r][c]}'
print("Done.")