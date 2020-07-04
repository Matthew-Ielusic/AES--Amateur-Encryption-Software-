#include "pch.h"

#include "KeySchedule.h"
#include "RoundFunctions.h"
#include "Constants.h"
#include <stdexcept>

uint32_t word(const uint8_t* current);

KeySchedule::KeySchedule(const uint8_t* key) : index(0), direction(1)
{
	
	for (int i = 0; i < Nk * Nb; i += 4) {
		keys.push_back(word(key + i));
	}

	uint32_t current;
	for (int i = Nk; i < Nb * (Nr + 1); ++i) {
		current = keys.at(i - 1);
		if (i % Nk == 0) {
			current = transform(current, i);
		}
		current ^= keys.at(i - Nk);
		keys.push_back(current);
	}
}

uint32_t KeySchedule::next()
{
	uint32_t output = keys.at(index);
	index += direction;
	return output;
}

uint32_t KeySchedule::at(int index) const
{
	return keys.at(index);
}

KeySchedule KeySchedule::InverseSchedule(const uint8_t* key)
{
	KeySchedule output(key);
	output.index = (Nb * (Nr + 1)) - 1;
	output.direction = -1;
	return output;
}

uint32_t word(const uint8_t* current) {
	uint32_t msb         = static_cast<uint32_t>(*current++) << 24;
	uint32_t secondMost  = static_cast<uint32_t>(*current++) << 16;
	uint32_t secondLeast = static_cast<uint32_t>(*current++) << 8;
	uint32_t lsb         = static_cast<uint32_t>(*current);
	return msb | secondMost | secondLeast | lsb;
}




uint32_t transform(uint32_t value, int i) {
	// result = SubWord(RotWord(temp)) xor Rcon[i / Nk]
	uint8_t bytes[] = { (uint8_t)((value & 0xff000000) >> 24), (uint8_t)((value & 0x00ff0000) >> 16), (uint8_t)((value & 0xff00) >> 8), (uint8_t)(value & 0xff) };
	for (int i = 0; i < 4; ++i) {
		bytes[i] = FiniteField::sBox(bytes[i]);
	}
	uint8_t rotated[4] = { bytes[1], bytes[2], bytes[3], bytes[0] };

	return word(rotated) ^ Rcon(i / 4);
}

uint32_t Rcon(int i) {
	uint8_t MSB = 1;
	
	if (1 <= i && i <= 8) {
		MSB <<= (i - 1);
	}
	else if (i == 9) {
		MSB = 0x1b;
	}
	else if (i == 10) {
		MSB = 0x36;
	}
	else {
		throw std::out_of_range("i must be between 0 and 10 (inclusive)");
	}

	return MSB << 24;
}


