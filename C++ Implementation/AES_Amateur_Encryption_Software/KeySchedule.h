#pragma once
#include <cstdint>
#include <vector>
class KeySchedule
{
public:
	KeySchedule(const std::vector<uint8_t>& key);
	static KeySchedule InverseSchedule(const std::vector<uint8_t>& key);

	uint32_t next();
	void reset();
	uint32_t at(int index) const;

private:
	std::vector<uint32_t> keys;
	int index;
	int direction;
};

uint32_t Rcon(int i);
uint32_t transform(uint32_t, int);