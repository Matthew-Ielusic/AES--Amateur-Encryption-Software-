#include "pch.h"
#include "AmateurEncrypt.h"
#include "RoundFunctions.h"
#include "Constants.h"
#include <stdexcept>

AmateurEncrypt::AmateurEncrypt(const std::vector<uint8_t>& key) : schedule(key) { }

std::vector<uint8_t> AmateurEncrypt::encryptBlock(const std::vector<uint8_t>& block)
{
    if (block.size() != 16) {
        throw std::invalid_argument("Input blocks must be 16 bytes long");
    }

    RoundFunctions::State state(block);

    state.AddRoundKey(schedule);

    for (int i = 0; i < Nr - 1; ++i) {
        state.SubBytes();
        state.ShiftRows();
        state.MixColumns();
        state.AddRoundKey(schedule);
    }

    state.SubBytes();
    state.ShiftRows();
    state.AddRoundKey(schedule);

    schedule.reset();

    return state.toVector();
}

std::vector<std::vector<uint8_t>> AmateurEncrypt::cbc(const std::vector<std::vector<uint8_t>> data, const std::vector<uint8_t>& iv)
{
    if (iv.size() != 16) {
        throw std::invalid_argument("The length of the IV must be 16 bytes");
    }

    std::vector<std::vector<uint8_t>> output;
    const std::vector<uint8_t>* previous = &iv;
    for (auto block : data) { // Deliberate vector copy!
        CipherBlockChaining::pairwiseXOR(block, previous);
        output.push_back(encryptBlock(block));
        previous = &output.back();
    }
    return output;
}

void CipherBlockChaining::pairwiseXOR(std::vector<uint8_t>& target, const std::vector<uint8_t>* key)
{
    for (int i = 0; i < 16; ++i) {
        target[i] ^= (*key)[i];
    }
}