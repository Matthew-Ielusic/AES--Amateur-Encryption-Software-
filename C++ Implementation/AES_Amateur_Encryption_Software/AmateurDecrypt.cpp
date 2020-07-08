#include "pch.h"

#include "AmateurDecrypt.h"
#include "RoundFunctions.h"
#include "Constants.h"

#include <stdexcept>

AmateurDecrypt::AmateurDecrypt(const std::vector<uint8_t>& key)
{
    schedule = KeySchedule::InverseSchedule(key);
}

std::vector<uint8_t> AmateurDecrypt::decryptBlock(const std::vector<uint8_t>& block)
{
    throw "Not Implemented";
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
   