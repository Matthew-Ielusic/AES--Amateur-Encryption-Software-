from Implementation import RoundFunctions
from Implementation.KeySchedule import DecryptKeySchedule
from Implementation import Constants as C
from Implementation.FiniteField.Galois import BytePolynomial
import operator

class AmateurDecrypt:
    def __init__(self, keyByteList):
        if len(keyByteList) != C.Nk() * 4:
            raise ValueError("This class only supports 128-bit keys -- only flat arrays of 16 byte-like objects are allowed")
        self.keySchedule = DecryptKeySchedule(keyByteList)

    def decryptBlock(self, inputByteList):
        if len(inputByteList) != C.Nb() * 4:
            raise ValueError("This method decrypts in ECB mode -- only flat arrays of 16 byte-like objects are allowed")
        inputAsPolynomials = [BytePolynomial.fromInt(b) for b in inputByteList]
        state = RoundFunctions.State(inputAsPolynomials)

        RoundFunctions.AddRoundKey(state, self.keySchedule.next())

        for _ in range(C.Nr() - 1):
            RoundFunctions.inverseShiftRows(state)
            RoundFunctions.inverseSubBytes(state)
            RoundFunctions.AddRoundKey(state, self.keySchedule.next())
            RoundFunctions.inverseMixColumns(state)
    
        RoundFunctions.inverseShiftRows(state)
        RoundFunctions.inverseSubBytes(state)
        RoundFunctions.AddRoundKey(state, self.keySchedule.next())

        self.keySchedule.reset()
        return state.asList()

    def cbc(self, inputBlocks, iv):
        if len(iv) is not 16:
            raise ValueError("The IV was not a flat list of 16 byte-like objects")

        plainText = []
        previous = iv
        for block in inputBlocks:
            if len(block) is not 16:
                raise ValueError("The inputBlocks must be a list of lists of 16 byte-like objects")
            
            partialDecryption = self.decryptBlock(block)
            fullDecryption = [part ^ prev for (part, prev) in zip(partialDecryption, previous)]
            previous = block
            
            plainText.append(fullDecryption)

        return plainText