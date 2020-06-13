import RoundFunctions
import KeySchedule
import Constants as C
import Galois

#begin
# byte state[4,Nb]
 
#state = in
 
#AddRoundKey(state, w[Nr*Nb, (Nr+1)*Nb-1]) // See Sec. 5.1.4
 
#for round = Nr-1 step -1 downto 1
# InvShiftRows(state) // See Sec. 5.3.1
# InvSubBytes(state) // See Sec. 5.3.2
# AddRoundKey(state, w[round*Nb, (round+1)*Nb-1])
# InvMixColumns(state) // See Sec. 5.3.3
# end for
 
#InvShiftRows(state)
# InvSubBytes(state)
# AddRoundKey(state, w[0, Nb-1])
 
#out = state
  
def decryptBlock(keyByteList, inputByteList):
    if len(inputByteList) != C.Nb() * 4:
        raise ValueError("This method decrypts in ECB mode -- only flat arrays of 16 byte-like objects are allowed")
    if len(keyByteList) != C.Nk() * 4:
        raise ValueError("This method only supports 128-bit keys -- only flat arrays of 16 byte-like objects are allowed")

    state = RoundFunctions.State([Galois.BytePolynomial.fromInt(b) for b in inputByteList])
    keySchedule = KeySchedule.InverseKeySchedule(keyByteList)

    RoundFunctions.AddRoundKey(state, keySchedule.next())

    for round in range(C.Nr() - 1):
        RoundFunctions.invShiftRows(state)
        RoundFunctions.invSubBytes(state)
        RoundFunctions.AddRoundKey(state, keySchedule.next())
        RoundFunctions.invMixColumns(state)
    
    RoundFunctions.invShiftRows(state)
    RoundFunctions.invSubBytes(state)
    RoundFunctions.AddRoundKey(state, keySchedule.next())

    return state.asList()