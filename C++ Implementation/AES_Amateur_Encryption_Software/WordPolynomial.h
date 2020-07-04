#pragma once
#include <cstdint>
class WordPolynomial
{
public:
	uint8_t& at(int index);
	uint8_t& operator[](int index);
private:
	uint8_t coefficients[4];
};
