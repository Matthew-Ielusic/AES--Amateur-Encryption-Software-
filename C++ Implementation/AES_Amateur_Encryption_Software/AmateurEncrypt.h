#pragma once

#include "KeySchedule.h"
#include <cstdint>
#include <vector>

class AmateurEncrypt
{
public:
	AmateurEncrypt(const std::vector<uint8_t>& key);
	
	std::vector<uint8_t> encryptBlock(const std::vector<uint8_t>& block);
	std::vector<std::vector<uint8_t>> cbc(const std::vector<std::vector<uint8_t>> data, const std::vector<uint8_t>& iv);

private:
	KeySchedule schedule;
};

namespace CipherBlockChaining {
	void pairwiseXOR(std::vector<uint8_t>& target, const std::vector<uint8_t>* key);
}


