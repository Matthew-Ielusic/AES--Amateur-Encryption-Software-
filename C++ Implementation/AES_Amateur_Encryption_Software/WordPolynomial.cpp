#include "pch.h"

#include "WordPolynomial.h"
#include <stdexcept>

uint8_t& WordPolynomial::at(int index) {
	if (index < 0 || index >= 4) {
		throw std::out_of_range("Index of a WordPolynomial must be between 0 and 3");
	} else {
		return (*this)[index];
	}
}

uint8_t& WordPolynomial::operator[](int index) {
	return coefficients[index];
}