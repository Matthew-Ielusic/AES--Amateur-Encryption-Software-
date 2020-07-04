#include "pch.h"
#include "AmateurEncrypt.h"
#include "RoundFunctions.h"
#include <stdexcept>

AmateurEncrypt::AmateurEncrypt(const std::vector<uint8_t>& key) : schedule(key) { }

std::vector<uint8_t> AmateurEncrypt::encrypt(const std::vector<uint8_t>& block)
{
    if (block.size() != 16) {
        throw std::invalid_argument("Input blocks must be 16 bytes long");
    }

    RoundFunctions::State state(block);
    



   /* def encryptBlock(self, inputByteList) :
        if len(inputByteList) != C.Nb() * 4 :
            raise ValueError("This method encrypts in ECB mode -- only flat arrays of 16 byte-like objects are allowed")
            inputAsPolynomials = [BytePolynomial.fromInt(b) for b in inputByteList]
            state = RoundFunctions.State(inputAsPolynomials)

            RoundFunctions.AddRoundKey(state, self.keySchedule.next())

            for _ in range(C.Nr() - 1) :
                RoundFunctions.SubBytes(state)
                RoundFunctions.ShiftRows(state)
                RoundFunctions.MixColumns(state)
                RoundFunctions.AddRoundKey(state, self.keySchedule.next())

                RoundFunctions.SubBytes(state)
                RoundFunctions.ShiftRows(state)
                RoundFunctions.AddRoundKey(state, self.keySchedule.next())

                self.keySchedule.reset()
                return state.asList()*/
}
