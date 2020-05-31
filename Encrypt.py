import RoundFunctions
import KeySchedule
import Constants as C
import Galois
def EncryptBlock(keyByteList, inputByteList):
    if len(inputByteList) != C.Nb() * 4:
        raise ValueError("This method encrypts in ECB mode -- only flat arrays of 16 byte-like objects are allowed")
    if len(keyByteList) != C.Nk() * 4:
        raise ValueError("This method only supports 128-bit keys -- only flat arrays of 16 byte-like objects are allowed")

    state = RoundFunctions.State([Galois.BytePolynomial.fromInt(b) for b in inputByteList])
    keySchedule = KeySchedule.KeySchedule(keyByteList)

    RoundFunctions.AddRoundKey(state, keySchedule.next())

    for round in range(1, C.Nr()):
        RoundFunctions.SubBytes(state)
        RoundFunctions.ShiftRows(state)
        RoundFunctions.MixColumns(state)
        RoundFunctions.AddRoundKey(state, keySchedule.next())
    
    RoundFunctions.SubBytes(state)
    RoundFunctions.ShiftRows(state)
    RoundFunctions.AddRoundKey(state, keySchedule.next())

    return state.asList()