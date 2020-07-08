#pragma once
#include "KeySchedule.h"
#include "AmateurEncrypt.h"
#include <cstdint>
#include <vector>

__declspec(dllexport) class AmateurDecrypt
{
public:
	AmateurDecrypt(const std::vector<uint8_t>& key);

	std::vector<uint8_t> decryptBlock(const std::vector<uint8_t>& block);
	std::vector<std::vector<uint8_t>> cbc(const std::vector<std::vector<uint8_t>> data, const std::vector<uint8_t>& iv);

private:
	KeySchedule schedule;
};

