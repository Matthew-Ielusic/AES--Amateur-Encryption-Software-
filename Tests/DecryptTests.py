# Hack sys.path to get code from the parent folder
import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir) 
# </hack>

import Decrypt
import Encrypt
import unittest

class TestDecrypt(unittest.TestCase):
    def test_roundTrip(self):
        input = [0x32, 0x43, 0xf6, 0xa8, 0x88, 0x5a, 0x30, 0x8d, 0x31, 0x31, 0x98, 0xa2, 0xe0, 0x37, 0x07, 0x34]
        cipherKey = 0x2b7e151628aed2a6abf7158809cf4f3c
        cipherKeyBytes = bytes([0x2b, 0x7e, 0x15, 0x16, 0x28, 0xae, 0xd2, 0xa6, 0xab, 0xf7, 0x15, 0x88, 0x09, 0xcf, 0x4f, 0x3c])
        roundTrip = Decrypt.decryptBlock(cipherKeyBytes, Encrypt.EncryptBlock(cipherKeyBytes, input))
        self.assertEqual(input, roundTrip, "Decryption round-trip failed")

if __name__ == '__main__':
    try:
        unittest.main()
    except SystemExit:
        # unittest & my IDE don't play nice
        # It raises a SystemExit when it finishes
        pass
