from Implementation import RoundFunctions
from Implementation.KeySchedule import KeySchedule
from Implementation import Constants as C
from Implementation.FiniteField.Galois import BytePolynomial
import operator

class AmateurEncrypt:
    def __init__(self, keyByteList):
        if len(keyByteList) != C.Nk() * 4:
            raise ValueError("This class only supports 128-bit keys -- only flat arrays of 16 byte-like objects are allowed")
        self.keySchedule = KeySchedule(keyByteList)

    def encryptBlock(self, inputByteList):
        if len(inputByteList) != C.Nb() * 4:
            raise ValueError("This method encrypts in ECB mode -- only flat arrays of 16 byte-like objects are allowed")
        inputAsPolynomials = [BytePolynomial.fromInt(b) for b in inputByteList]
        state = RoundFunctions.State(inputAsPolynomials)

        RoundFunctions.AddRoundKey(state, self.keySchedule.next())

        for _ in range(C.Nr() - 1):
            RoundFunctions.SubBytes(state)
            RoundFunctions.ShiftRows(state)
            RoundFunctions.MixColumns(state)
            RoundFunctions.AddRoundKey(state, self.keySchedule.next())
    
        RoundFunctions.SubBytes(state)
        RoundFunctions.ShiftRows(state)
        RoundFunctions.AddRoundKey(state, self.keySchedule.next())

        self.keySchedule.reset()
        return state.asList()

    def cbc(self, inputBlocks, iv):
        if len(iv) is not 16:
            raise ValueError("The IV was not a flat list of 16 byte-like objects")

        output = []
        previous = iv
        for block in inputBlocks:
            if len(block) is not 16:
                raise ValueError("The inputBlocks must be a list of lists of 16 byte-like objects")
            
            block = [bl ^ prev for (bl, prev) in zip(block, previous)]
            cipherText = self.encryptBlock(block)
            previous = cipherText
            output.append(cipherText)

        return output
