import RoundFunctions
import Galois

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
