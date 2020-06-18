# Hack sys.path to get code from the parent folder
import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir) 
# </hack>

from Implementation import RoundFunctions
from Implementation.FiniteField import Galois
from Implementation.FiniteField import IntPolynomial

import unittest

class TestState(unittest.TestCase):
	def setUp(self):
		self.input = [Galois.BytePolynomial.fromInt(i) for i in range(16)]

	def test_get(self):
		state = RoundFunctions.State(self.input)
		
		for row in range(4):
			for column in range(4):
				expected = self.input[column * 4 + row]
				actual = state.data[row][column]
				self.assertEqual(expected, actual, "state.data[r][c] failed -- expected " + str(expected) + "; got " + str(actual))
		
				actual = state[row][column]
				self.assertEqual(expected, actual, "state[r][c] failed -- expected " + str(expected) + "; got " + str(actual))
	def test_set(self):
		state = RoundFunctions.State(self.input)

		value = Galois.BytePolynomial.fromInt(252)
		state.data[1][2] = value

		expected = value
		actual = state.data[1][2]
		self.assertEqual(expected, actual, "setting via state.data failed -- expected " + str(expected) + "; got " + str(actual))

		state[3][2] = value
		actual = state[3][2]
		self.assertEqual(expected, actual, "setting via state.__getitem__ failed -- expected " + str(expected) + "; got " + str(actual))

class TestForward(unittest.TestCase):
	def test_sbox(self):
		ff = Galois.BytePolynomial.fromInt(0xff)
		expected = Galois.BytePolynomial.fromInt(0x16)
		self.assertEqual(expected, RoundFunctions.sBox(ff), "sBox(" + str(int(ff)) + ") was " + hex(int(expected)) + ", not 0x16")

		ab = Galois.BytePolynomial.fromInt(0xab)
		expected = Galois.BytePolynomial.fromInt(0x62)
		self.assertEqual(expected, RoundFunctions.sBox(ab), "sBox(" + str(int(ab)) + ") was " + hex(int(expected)) + ", not 0x62")

		zero = Galois.zeroByte()
		expected = Galois.BytePolynomial.fromInt(0x63)
		self.assertEqual(expected, RoundFunctions.sBox(zero), "sBox(" + str(int(zero)) + ") was " + hex(int(expected)) + ", not 0x63")

	def test_shift_rows(self):
		input = [Galois.BytePolynomial.fromInt(i) for i in range(16)]
		original =  RoundFunctions.State(input)
		state	 =  RoundFunctions.State(input)
		RoundFunctions.ShiftRows(state)
		for r in range(4):
			for c in range(4):
				self.assertEqual(original[r][(c + r) % 4], state[r][c], "The byte in row " + str(r) + " and column " + str(c) + " was not shifted correctly.")

	def test_mix_columns(self):
		aesExampleBytes = [[0x52, 0x85, 0xe3, 0xf6], [0xa4, 0x11, 0xcf, 0x50], [0xc8, 0x6a, 0x2f, 0x5e], [0x94, 0x28, 0xd7, 0x07]]
		state = RoundFunctions.State.from4x4([[Galois.BytePolynomial.fromInt(x) for x in y] for y in aesExampleBytes])
		RoundFunctions.MixColumns(state)
		bytesExpected = [[0x0f, 0x60, 0x6f, 0x5e], [0xd6, 0x31, 0xc0, 0xb3], [0xda, 0x38, 0x10, 0x13], [0xa9, 0xbf, 0x6b, 0x01]]
		bytesActual   = [[int(state[r][c]) for c in range(4)] for r in range(4)]
		self.assertEqual(bytesExpected, bytesActual, "MixColumns did not mix correctly.  Expected " + str(bytesExpected) + "; actual: " + str(bytesActual))

class TestBackward(unittest.TestCase):
	def setUp(self):
		self.input = [Galois.BytePolynomial.fromInt(i) for i in range(16)]

	def test_inv_s_box(self):
		original = Galois.BytePolynomial.fromInt(0xab)
		boxed = RoundFunctions.sBox(original)
		unboxed = RoundFunctions.invSBox(boxed)
		self.assertEqual(original, unboxed, f'Expected {original}, got {unboxed}')

		original = Galois.BytePolynomial.fromInt(0x71)
		boxed = RoundFunctions.sBox(original)
		unboxed = RoundFunctions.invSBox(boxed)
		self.assertEqual(original, unboxed, f'Expected {original}, got {unboxed}')

		original = Galois.BytePolynomial.fromInt(0x00)
		boxed = RoundFunctions.sBox(original)
		unboxed = RoundFunctions.invSBox(boxed)
		self.assertEqual(original, unboxed, f'Expected {original}, got {unboxed}')

		original = Galois.BytePolynomial.fromInt(0xF3)
		boxed = RoundFunctions.sBox(original)
		unboxed = RoundFunctions.invSBox(boxed)
		self.assertEqual(original, unboxed, f'Expected {original}, got {unboxed}')

	def test_inv_shift_rows(self):
		original = RoundFunctions.State(self.input)
		state	 = RoundFunctions.State(self.input)
		RoundFunctions.ShiftRows(state)
		RoundFunctions.invShiftRows(state)
		for r in range(4):
			for c in range(4):
				self.assertEqual(original[r][c], state[r][c], "The byte in row " + str(r) + " and column " + str(c) + " was not shifted correctly.")

	def test_inv_mix_columns(self):
		original = RoundFunctions.State(self.input)
		state	 = RoundFunctions.State(self.input)
		RoundFunctions.MixColumns(state)
		RoundFunctions.invMixColumns(state)
		for r in range(4):
			for c in range(4):
				self.assertEqual(original[r][c], state[r][c], "The byte in row " + str(r) + " and column " + str(c) + " was not shifted correctly.")

if __name__ == '__main__':
    try:
        unittest.main()
    except SystemExit:
        # unittest & my IDE don't play nice
        # unittest raises a SystemExit when it finishes
        pass








#print("Done.")
#print("Testing invShiftRows")


#print("Done")
#print("Testing invMixColumns")

#print("Done")


