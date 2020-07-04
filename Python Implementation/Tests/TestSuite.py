import unittest
from EncryptTests import TestEncrypt
from DecryptTests import TestDecrypt
from GaloisTests import TestBytePoly
from GenPolyTests import TestGenPoly
from IntPolyTests import TestIntPoly
from KeyScheduleTests import TestKeySchedule
from RoundFunctionTests import TestState
from RoundFunctionTests import TestForward
from RoundFunctionTests import TestBackward


if __name__ == '__main__':
    try:
        unittest.main() 
    except SystemExit:
        # unittest & my IDE don't play nice
        # It raises a SystemExit when it finishes
        pass