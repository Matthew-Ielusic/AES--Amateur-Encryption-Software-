import RoundFunctions
import Galois

#input = [Galois.BytePolynomial.fromInt(i) for i in range(16)]
#state = RoundFunctions.State(input)

#print("Testing indexing...")
#for row in range(4):
#	for column in range(4):
#		expected = input[column * 4 + row]
#		actual = state.data[row][column]
#		assert actual == expected, "state.data[r][c] failed -- expected " + str(expected) + "; got " + str(actual)
		
#		actual = state[row][column]
#		assert actual == expected, "state[r][c] failed -- expected " + str(expected) + "; got " + str(actual)
#print("Done.")
#print("Testing setting...")

#value = Galois.BytePolynomial.fromInt(252)
#state.data[1][2] = value
#expected = value
#actual = state.data[1][2]
#assert actual == expected, "setting via state.data failed -- expected " + str(expected) + "; got " + str(actual)
#state[3][2] = value
#actual = state[3][2]
#assert actual == expected, "setting via state.__getitem__ failed -- expected " + str(expected) + "; got " + str(actual)
#print("Done.")


print("Testing the substitution box")
ff = Galois.BytePolynomial.fromInt(0xff)
expected = Galois.BytePolynomial.fromInt(0x16)
assert RoundFunctions.sBox(ff) == expected, "sBox(" + str(int(ff)) + ") was " + hex(int(expected)) + ", not 0x16"
