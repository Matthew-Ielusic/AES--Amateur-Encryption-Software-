#pragma once

#include "KeySchedule.h"
#include <cstdint>
#include <vector>

__declspec(dllexport) class AmateurEncrypt
{
public:
	AmateurEncrypt(const std::vector<uint8_t>& key);
	
	std::vector<uint8_t> encryptBlock(const std::vector<uint8_t>& block);
	std::vector<std::vector<uint8_t>> cbc(const std::vector<std::vector<uint8_t>> data, const std::vector<uint8_t>& iv);

private:
	KeySchedule schedule;
};

void pairwiseXOR(std::vector<uint8_t>& target, const std::vector<uint8_t>* key);

