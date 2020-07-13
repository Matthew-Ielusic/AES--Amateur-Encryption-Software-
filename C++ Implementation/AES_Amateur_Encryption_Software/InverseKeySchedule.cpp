#include "pch.h"
#include "InverseKeySchedule.h"
#include "Constants.h"

constexpr int counterThreshold = 4;

InverseKeySchedule::InverseKeySchedule(const std::vector<uint8_t>& key) :  KeySchedule(key)
{
	reset();
}

uint32_t InverseKeySchedule::next()
{
	uint32_t output = keys.at(index);
	index++;
	blockCounter++;
	if (blockCounter == counterThreshold)
	{
		blockCounter = 0;
		index -= 2 * Nb;
	}
	return output;

}

void InverseKeySchedule::reset()
{
	index = startIndex();
	blockCounter = 0;
}

int InverseKeySchedule::startIndex()
{
	return keys.size() - Nb;
}
