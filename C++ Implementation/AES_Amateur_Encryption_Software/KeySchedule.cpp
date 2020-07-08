#include "pch.h"

#include "KeySchedule.h"
#include "RoundFunctions.h"
#include "Constants.h"
#include <stdexcept>

uint32_t word(const std::vector<uint8_t> data, int index);

KeySchedule::KeySchedule(const std::vector<uint8_t>& key) : index(0), direction(1)
{
	if (key.size() != Nk * Nb) {
		throw std::invalid_argument("Only 128-bit keys are supported");
	}
	
	for (int index = 0; index < Nk * Nb; index += 4) {
		keys.push_back(word(key, index));
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

KeySchedule::KeySchedule()
{
}

uint32_t KeySchedule::next()
{
	uint32_t output = keys.at(index);
	index += direction;
	return output;
}

void KeySchedule::reset()
{
	switch (direction) {
	case 1:
		index = 0;
		return;
	case -1:
		index = keys.size() - 1;
		return;
	default:
		throw std::logic_error("`direction` had an illegal value");
	}
}

uint32_t KeySchedule::at(int index) const
{
	return keys.at(index);
}

KeySchedule KeySchedule::InverseSchedule(const std::vector<uint8_t>& key)
{
	KeySchedule output(key);
	output.index = (Nb * (Nr + 1)) - 1;
	output.direction = -1;
	return output;
}

uint32_t word(const std::vector<uint8_t> data, int index) {
	uint32_t msb         = static_cast<uint32_t>(data.at(index)) << 24; index++;
	uint32_t secondMost  = static_cast<uint32_t>(data.at(index)) << 16; index++;
	uint32_t secondLeast = static_cast<uint32_t>(data.at(index)) << 8;  index++;
	uint32_t lsb         = static_cast<uint32_t>(data.at(index));
	return msb | secondMost | secondLeast | lsb;
}




uint32_t transform(uint32_t value, int i) {
	// result = SubWord(RotWord(temp)) xor Rcon[i / Nk]
	uint8_t bytes[] = { (uint8_t)((value & 0xff000000) >> 24), (uint8_t)((value & 0x00ff0000) >> 16), (uint8_t)((value & 0xff00) >> 8), (uint8_t)(value & 0xff) };
	for (int i = 0; i < 4; ++i) {
		bytes[i] = FiniteField::sBox(bytes[i]);
	}
	std::vector<uint8_t> rotated = { bytes[1], bytes[2], bytes[3], bytes[0] };

	return word(rotated, 0) ^ Rcon(i / 4);
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


