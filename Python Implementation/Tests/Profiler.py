# Hack sys.path to get code from the parent folder
import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir) 
# </hack>

import cProfile

import Encrypt
import Decrypt
from Crypto.Cipher import AES
import re

encryptHere = """key=b'0123456789abcdef'
block=b'0123456789abcdef'
en = Encrypt.AmateurEncrypt(key)
en.encryptBlock(block)"""

decryptHere = """key=b'0123456789abcdef'
block=b'0123456789abcdef'
de = Decrypt.AmateurDecrypt(key)
de.decryptBlock(block)"""

encryptPycrypto = """key=b'0123456789abcdef'
block=b'0123456789abcdef'
en = AES.new(key, AES.MODE_ECB)
en.encrypt(block)"""

decryptPycrypto = """key=b'0123456789abcdef'
block=b'0123456789abcdef'
en = AES.new(key, AES.MODE_ECB)
en.decrypt(block)"""

if __name__ == '__main__':
    cProfile.run(encryptHere)
    cProfile.run(encryptPycrypto)

    cProfile.run(decryptHere)
    cProfile.run(decryptPycrypto)

