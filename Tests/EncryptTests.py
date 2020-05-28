# Hack sys.path to get code from the parent folder
import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir) 
# </hack>


import Encrypt

print("Testing ECB encryption")
# Appendex B example
input = [0x32, 0x43, 0xf6, 0xa8, 0x88, 0x5a, 0x30, 0x8d, 0x31, 0x31, 0x98, 0xa2, 0xe0, 0x37, 0x07, 0x34]
cipherKey = 0x2b7e151628aed2a6abf7158809cf4f3c
expectedOutput = [0x39, 0x02, 0xdc, 0x19, 0x25, 0xdc, 0x11, 0x6a, 0x84, 0x09, 0x85, 0x0b, 0x1d, 0xfb, 0x97, 0x32]

actualOutput = Encrypt.EncryptBlock(input, cipherKey)

assert actualOutput == expectedOutput, f'Expected {expectedOutput}, got {actualOutput}'
print("Done")