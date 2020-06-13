
# Hack sys.path to get code from the parent folder
import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir) 
# </hack>


import Encrypt
from Crypto.Cipher import AES
import unittest

class TestEncrypt(unittest.TestCase):
	def test_against_standard(self):
		# Appendix B example
		input = [0x32, 0x43, 0xf6, 0xa8, 0x88, 0x5a, 0x30, 0x8d, 0x31, 0x31, 0x98, 0xa2, 0xe0, 0x37, 0x07, 0x34]
		cipherKey = 0x2b7e151628aed2a6abf7158809cf4f3c
		cipherKeyBytes = bytes([0x2b, 0x7e, 0x15, 0x16, 0x28, 0xae, 0xd2, 0xa6, 0xab, 0xf7, 0x15, 0x88, 0x09, 0xcf, 0x4f, 0x3c])

		expectedOutput = [0x39, 0x25, 0x84, 0x1d, 0x2, 0xdc, 0x9, 0xfb, 0xdc, 0x11, 0x85, 0x97, 0x19, 0x6a, 0xb, 0x32]
		actualOutput = Encrypt.EncryptBlock(cipherKeyBytes, input)
		self.assertEqual(expectedOutput, actualOutput, "The test against the example in Appendix B failed")
	def test_against_pycrypto(self):
		input = b'123456789aBcDeF_'
		key   = b'0xdeadBEEFcabEA3'
		pycrypto = AES.new(key, AES.MODE_ECB)
		expected = [int(b) for b in pycrypto.encrypt(input)]
		actual = Encrypt.EncryptBlock(key, input)
		self.assertEqual(expected, actual, "The test against pycrypto failed")

if __name__ == '__main__':
    try:
        unittest.main()
    except SystemExit:
        # unittest & my IDE don't play nice
        # It raises a SystemExit when it finishes
        pass