import RoundFunctions
import KeySchedule
import Constants as C
import Galois
def EncryptBlock(inputByteArray, keyInt):
    state = RoundFunctions.State([Galois.BytePolynomial.fromInt(b) for b in inputByteArray])
    keySchedule = KeySchedule.KeySchedule(keyInt)

    RoundFunctions.AddRoundKey(state, keySchedule[0:4])

    for round in range(1, C.Nr()):
        RoundFunctions.SubBytes(state)
        RoundFunctions.ShiftRows(state)
        RoundFunctions.MixColumns(state)
        RoundFunctions.AddRoundKey(state, keySchedule[round*4:(round + 1) * 4])
    
    RoundFunctions.SubBytes(state)
    RoundFunctions.ShiftRows(state)
    RoundFunctions.AddRoundKey(state, keySchedule[-4:])

    return state.asList()