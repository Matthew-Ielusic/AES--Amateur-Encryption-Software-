from  Implementation import RoundFunctions
from Implementation import KeySchedule
from Implementation import Constants as C
from Implementation.FiniteField import Galois
import operator

class AmateurDecrypt:
    def __init__(self, keyByteList):
        if len(keyByteList) != C.Nk() * 4:
            raise ValueError("This class only supports 128-bit keys -- only flat arrays of 16 byte-like objects are allowed")
        self.keySchedule = KeySchedule.InverseKeySchedule(keyByteList)

    def decryptBlock(self, inputByteList):
        if len(inputByteList) != C.Nb() * 4:
            raise ValueError("This method decrypts in ECB mode -- only flat arrays of 16 byte-like objects are allowed")

        state = RoundFunctions.State([Galois.BytePolynomial.fromInt(b) for b in inputByteList])

        RoundFunctions.AddRoundKey(state, self.keySchedule.next())

        for round in range(C.Nr() - 1):
            RoundFunctions.invShiftRows(state)
            RoundFunctions.invSubBytes(state)
            RoundFunctions.AddRoundKey(state, self.keySchedule.next())
            RoundFunctions.invMixColumns(state)
    
        RoundFunctions.invShiftRows(state)
        RoundFunctions.invSubBytes(state)
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
            fullDecryption = list(map(operator.xor, partialDecryption, previous))
            previous = block
            
            plainText.append(fullDecryption)

        return plainText