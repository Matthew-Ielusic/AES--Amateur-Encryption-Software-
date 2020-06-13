from IntPolynomial import IntPolynomial
import Galois
import RoundFunctions
import Constants as C

class KeySchedule():
    # Amateur Encryption Software supports Nk = 4 (128 bits) only
    def __init__(self, cipherKeyBytes):
        if len(cipherKeyBytes) != C.Nk() * 4:
            raise ValueError("This implementation of AES supports 128-bit keys only")
        keyBytes = [Galois.BytePolynomial.fromInt(b) for b in cipherKeyBytes]
        # Reverse the endianness of each 4-byte word
        # Sadly, keyBytes[3:-1:-1] = [] 
        w = [IntPolynomial(keyBytes[3::-1])] + [IntPolynomial(keyBytes[i+3:i-1:-1]) for i in (4, 8, 12)]
        for i in range(C.Nk(), C.Nb() * (C.Nr() + 1)):
            temp = w[i - 1]
            if i % C.Nk() == 0:
                rot = RotWord(temp)
                sub = SubWord(rot)
                rcon = sub + Rcon(int(i / C.Nk()))
                temp = SubWord(RotWord(temp)) + Rcon(int(i / C.Nk()))
            w.append(w[i - C.Nk()] + temp)

        self.roundKeys = w
        self._roundSize = 4
        self._roundDirection = 1
        self._roundNumber = 0
        self._initialRoundNumber = 0

    def next(self):
        output = self.roundKeys[self._roundNumber : self._roundNumber + self._roundSize]
        if not output:
            raise IndexError("Tried to call next too many times")

        self._roundNumber += self._roundDirection * self._roundSize
        return output

    def hasNext(self):
        if self._roundDirection is 1:
            return (self._roundNumber + self._roundSize) <= len(self.roundKeys)
        elif self._roundDirection is -1:
            return self._roundNumber >= 0
        else:
            raise ValueError("Illegal value for self._roundDirection")

    def reset(self):
        self._roundNumber = self._initialRoundNumber

    def __getitem__(self, key):
        return self.roundKeys[key]


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


def InverseKeySchedule(cipherKeyBytes):
    schedule = KeySchedule(cipherKeyBytes)
    schedule._roundNumber = C.Nr() * C.Nb()
    schedule._initialRoundNumber = schedule._roundNumber
    schedule._roundDirection = -1
    return schedule
