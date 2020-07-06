#pragma once
#include <cstdint>
#include <vector>
#include "KeySchedule.h"
namespace RoundFunctions {
	class State {
	public:
		State(const std::vector<uint8_t>& block);

		void AddRoundKey(KeySchedule& schedule);
		void SubBytes();
		void ShiftRows();
		void MixColumns();
		uint8_t& at(int row, int column);

		std::vector<uint8_t> toVector() const;
	private:
		uint8_t values[4][4];
		// Access values using values[rowIndex][columnIndex]
		friend bool operator==(const State&, const State&);

	};

	bool operator==(const State&, const State&);
}

namespace FiniteField {
	uint8_t sBox(uint8_t value);
	uint8_t invSBox(uint8_t value);
}
