from Encrypt import AmateurEncrypt
from Decrypt import AmateurDecrypt

if __name__ == '__main__':
    key =   b'0123456789abcdef'
    block = b'fedcba9876542310'

    print("Message:    ", block)
    print("Key:        ", key)
    
    # How to encrypt a block
    enc = AmateurEncrypt(key)
    cipherText = bytes(enc.encryptBlock(block))
    print("Ciphertext: ", cipherText)

    # How to decrypt a block
    dec = AmateurDecrypt(key)
    plaintext = bytes(dec.decryptBlock(cipherText))
    print("Round-Trip: ", plaintext)

    # How to use cipher block chaining
    
    print("Encrypting multiple blocks:")

    message = [[42] * 16] * 10 # Create a message of 10 blocks
    iv = [61] * 16 # Create an IV
    print("Message:   ")
    for m in message:
        print(m)
    print("IV: ", iv)

    cipherText = enc.cbc(message, iv)

    print("Cipher Text:")
    for c in cipherText:
        print(c)

    plaintext = dec.cbc(cipherText, iv)

    print("Round Trip:")
    for p in plaintext:
        print(p)