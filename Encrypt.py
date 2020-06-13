import RoundFunctions
import KeySchedule
import Constants as C
import Galois

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

