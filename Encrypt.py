from Implementation import RoundFunctions
from Implementation import KeySchedule
from Implementation import Constants as C
from Implementation.FiniteField import Galois
import operator

class AmateurEncrypt:
    def __init__(self, keyByteList):
        if len(keyByteList) != C.Nk() * 4:
            raise ValueError("This class only supports 128-bit keys -- only flat arrays of 16 byte-like objects are allowed")
        self.keySchedule = KeySchedule.KeySchedule(keyByteList)

    def encryptBlock(self, inputByteList):
        if len(inputByteList) != C.Nb() * 4:
            raise ValueError("This method encrypts in ECB mode -- only flat arrays of 16 byte-like objects are allowed")

        state = RoundFunctions.State([Galois.BytePolynomial.fromInt(b) for b in inputByteList])

        RoundFunctions.AddRoundKey(state, self.keySchedule.next())

        for round in range(C.Nr() - 1):
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

        cipherText = []
        previous = iv
        for block in inputBlocks:
            if len(block) is not 16:
                raise ValueError("The inputBlocks must be a list of lists of 16 byte-like objects")
            
            block = list(map(operator.xor, block, previous))
            cipherText.append(self.encryptBlock(block))
            previous = cipherText[-1]

        return cipherText
