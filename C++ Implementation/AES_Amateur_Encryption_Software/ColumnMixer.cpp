#include "pch.h"
#include "ColumnMixer.h"

constexpr uint8_t  em = 0x1b;
constexpr uint16_t m = 0x11b;
constexpr uint16_t mLen = 8;

uint8_t ColumnMixer::times02(uint8_t value) {
    static_assert(sizeof(int) > 1, "sizeof(int) == 1 ??");
    int result = value << 1;
    if (result < 256) {
        return result;
    }
    else {
        return static_cast<uint8_t>(result ^ em);
    }
}

uint8_t ColumnMixer::times03(uint8_t value) {
    int result = (value << 1) ^ value;
    if (result < 256) {
        return result;
    }
    else {
        return static_cast<uint8_t>(result ^ em);
    }
}

uint8_t ColumnMixer::times09(uint8_t value)
{
    int result = (value << 3) ^ value;
    for (int shift = 3; result > 256; --shift) {
        //if (result > (m << shift))
        if (result & (1 << (shift + mLen)))
            result ^= m << shift;
    }
    return static_cast<uint8_t>(result);
}

uint8_t ColumnMixer::times0b(uint8_t value)
{
    int result = (value << 3) ^ (value << 1) ^ value;
    for (int shift = 3; result > 256; --shift) {
        if (result & (1 << (shift + mLen)))
            result ^= m << shift;
    }
    return static_cast<uint8_t>(result);
}

uint8_t ColumnMixer::times0d(uint8_t value)
{
    int result = (value << 3) ^ (value << 2) ^ value;
    for (int shift = 3; result > 256; --shift) {
        if (result & (1 << (shift + mLen)))
            result ^= m << shift;
    }
    return static_cast<uint8_t>(result);
}

uint8_t ColumnMixer::times0e(uint8_t value)
{
    int result = (value << 3) ^ (value << 2) ^ (value << 1);
    for (int shift = 3; result > 256; --shift) {
        if (result & (1 << (shift + mLen)))
            result ^= m << shift;
    }
    return static_cast<uint8_t>(result);
}
