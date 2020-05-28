from IntPolynomial import IntPolynomial
import Galois
import RoundFunctions
import Constants as C

class KeySchedule():
    # Amateur Encryption Software supports Nk = 4 (128 bits) only
    def __init__(self, cipherKey):
        # Thanks stack overflow -- https://stackoverflow.com/questions/6187699/how-to-convert-integer-value-to-array-of-four-bytes-in-python
        keyBytes = [Galois.BytePolynomial.fromInt((cipherKey >> i) & 0xff) for i in range(120, -1, -8)]
        # Reverse the endianness of each 4-byte word
        w = [IntPolynomial(keyBytes[3::-1])] + [IntPolynomial(keyBytes[i+3:i-1:-1]) for i in (4, 8, 12)]
        # Sadly, keyBytes[3:-1:-1] = [] 
        for i in range(C.Nk(), C.Nb() * (C.Nr() + 1)):
            temp = w[i - 1]
            if i % C.Nk() == 0:
                rot = RotWord(temp)
                sub = SubWord(rot)
                rcon = sub + Rcon(int(i / C.Nk()))
                temp = SubWord(RotWord(temp)) + Rcon(int(i / C.Nk()))
            w.append(w[i - C.Nk()] + temp)

        self.roundKeys = w

    def __getitem__(self, key):
        return self.roundKeys[key]

#temp = w[i-1]
# if (i mod Nk = 0)
# temp = SubWord(RotWord(temp)) xor Rcon[i/Nk]
# else if (Nk > 6 and i mod Nk = 4)
# temp = SubWord(temp)
# end if
# w[i] = w[i-Nk] xor temp
# i = i + 1


def SubWord(intPoly):
    return IntPolynomial([RoundFunctions.sBox(bytePoly) for bytePoly in intPoly.coefficients])

def RotWord(intPoly):
    return IntPolynomial(intPoly.coefficients[3:4] + intPoly.coefficients[0:3])

def twoByte():
    out = Galois.BytePolynomial([0] * 8)
    out.coefficients[1] = 1
    return out

def Rcon(i):
    return IntPolynomial([Galois.zeroByte(), Galois.zeroByte(), Galois.zeroByte(), twoByte() ** (i - 1)])
