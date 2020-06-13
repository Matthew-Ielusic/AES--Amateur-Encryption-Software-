import unittest
from EncryptTests import TestEncrypt
from DecryptTests import TestDecrypt

def suite():
    suite = unittest.TestSuite()
    suite.addTest(TestEncrypt('test_encrypt'))
    return suite

if __name__ == '__main__':
    try:
        unittest.main() 
    except SystemExit:
        # unittest & my IDE don't play nice
        # It raises a SystemExit when it finishes
        pass