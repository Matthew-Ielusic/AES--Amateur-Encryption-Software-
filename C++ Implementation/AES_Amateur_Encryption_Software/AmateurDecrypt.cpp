#include "pch.h"

#include "AmateurDecrypt.h"
#include "RoundFunctions.h"
#include "Constants.h"

#include <stdexcept>

AmateurDecrypt::AmateurDecrypt(const std::vector<uint8_t>& key) : schedule(key) { }

std::vector<uint8_t> AmateurDecrypt::decryptBlock(const std::vector<uint8_t>& block)
{
    if (block.size() != 16) {
        throw std::invalid_argument("Input blocks must be 16 bytes long");
    }

    RoundFunctions::State state(block);

    state.AddRoundKey(schedule);

    for (int i = 0; i < Nr - 1; ++i) {
        state.InvShiftRows();
        state.InvSubBytes();
        state.AddRoundKey(schedule);
        state.InvMixColumns();
    }

    state.InvShiftRows();
    state.InvSubBytes();
    state.AddRoundKey(schedule);

    schedule.reset();
    return state.toVector();
}

std::vector<std::vector<uint8_t>> AmateurDecrypt::cbc(const std::vector<std::vector<uint8_t>> data, const std::vector<uint8_t>& iv)
{
    if (iv.size() != 16) {
        throw std::invalid_argument("The length of the IV must be 16 bytes");
    }

    std::vector<std::vector<uint8_t>> output;
    const std::vector<uint8_t>* previous = &iv;

    for (const auto& block : data) { // No array copy
        std::vector<uint8_t> decryption = decryptBlock(block);
        CipherBlockChaining::pairwiseXOR(decryption, previous);
        output.push_back(decryption);
        previous = &block;
    }

    return output;
}
   