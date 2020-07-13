#pragma once
#include <cstdint>
#include <vector>
class KeySchedule
{
public:
	KeySchedule(const std::vector<uint8_t>& key);

	virtual uint32_t next();
	virtual void reset();
	uint32_t at(int index) const;

protected:
	std::vector<uint32_t> keys;
	int index;
};
