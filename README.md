# AES (Amateur Encryption Software)
 
I wanted to figure out how modern encryption software works. 

So I downloaded a copy of the AES standard, and wrote a program to implement it.

Amateur Encryption Software is implemented in Python, and is an unoptimized implementation of AES that emphasizes the theory behind the standard.  Only 128-bit keys are supported.

(So, for example, the substitution box is implemented as described -- taking the multiplicative inverse of a byte, multiplying by a matrix, and adding a vector -- and not as a lookup table.)

Encryption is done by the AmateurEncrypt class in the Encrypt.py module.  Its constructor takes the key as a list of 16 bytes, and encrypts blocks of 16 bytes.  The encryptBlock method takes a single list of 16 bytes and returns its ciphertext.

It has a `cbc` method that takes a list of blocks and an initial value, and returns the cipher text for each block using cipher block chaining.

Decryption is done by the AmateurDecrypt class in the Decrypt.py module.  Its interface is almost exactly the same as AmateurEncrypt's is.
