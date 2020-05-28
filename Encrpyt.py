#Cipher(byte in[4*Nb], byte out[4*Nb], word w[Nb*(Nr+1)])
# begin
# byte state[4,Nb]
 
#state = in
 
#AddRoundKey(state, w[0, Nb-1]) // See Sec. 5.1.4
 
#for round = 1 step 1 to Nr–1
# SubBytes(state) // See Sec. 5.1.1
# ShiftRows(state) // See Sec. 5.1.2
# MixColumns(state) // See Sec. 5.1.3
# AddRoundKey(state, w[round*Nb, (round+1)*Nb-1])
# end for
 
#SubBytes(state)
# ShiftRows(state)
# AddRoundKey(state, w[Nr*Nb, (Nr+1)*Nb-1])
 
#out = state
# end
 
import RoundFunctions
import KeySchedule
import Constants as C
import Galois
def EncrpytBlock(inputByteArray, keyInt):
    state = RoundFunctions.State([Galois.BytePolynomial.fromInt(b) for b in inputByteArray])
    keySchedule = KeySchedule.KeySchedule(keyInt)

    RoundFunctions.AddRoundKey(state, keySchedule[0])

    for round in range(1, C.Nr()):
        RoundFunctions.SubBytes(state)
        RoundFunctions.ShiftRows(state)
        RoundFunctions.MixColumns(state)
        RoundFunctions.AddRoundKey(state, keySchedule[round])
    
    RoundFunctions.SubBytes(state)
    RoundFunctions.ShiftRows(state)
    RoundFunctions.AddRoundKey(state, keySchedule[-1])

    return state.asList()