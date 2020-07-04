#pragma once

#include "KeySchedule.h"
#include <cstdint>
#include <vector>

__declspec(dllexport) class AmateurEncrypt
{
public:
	std::vector<uint8_t> encrypt(const std::vector<uint8_t>& block);

	void encrypt(std::vector<uint8_t>& block);

private:
	KeySchedule schedule;
};
