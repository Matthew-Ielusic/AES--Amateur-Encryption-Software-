
#include "pch.h"
#include "CppUnitTest.h"
#include <vector>

#include "RoundFunctions.h"

using namespace Microsoft::VisualStudio::CppUnitTestFramework;

namespace Tests
{
	TEST_CLASS(RoundFunctionTests)
	{
	public:
		TEST_METHOD(TestSBox)
		{
			uint8_t input    = 0xff;
			uint8_t expected = 0x16;
			uint8_t actual    = FiniteField::sBox(input);
			Assert::AreEqual(expected, actual);

			input    = 0xab;
			expected = 0x62;
			actual   = FiniteField::sBox(input);
			Assert::AreEqual(expected, actual);

			actual   = FiniteField::sBox(0);
			expected = 0x63;
			Assert::AreEqual(expected, actual);
		}

		TEST_METHOD(TestShiftRows)
		{
			std::vector<uint8_t> data(16);
			for (int i = 0; i < 16; ++i)
				data[i] = i;

			RoundFunctions::State block(data);
			RoundFunctions::State expected(data);
			block.ShiftRows();

			for (int r = 0; r < 4; ++r) {
				for (int c = 0; c < 4; ++c) {
					int shifted = c - r;
					if (shifted < 0)
						shifted += 4;
					Assert::AreEqual(expected.at(r, c), block.at(r, shifted));
				}
			}
		}

		TEST_METHOD(TestMixColumns)
		{
			std::vector<uint8_t> before = { 0x87, 0x6e, 0x46, 0xa6, 0xf2, 0x4c, 0xe7, 0x8c, 0x4d, 0x90, 0x4a, 0xd8, 0x97, 0xec, 0xc3, 0x95 };
			uint8_t after[4][4] = { {0x47, 0x40, 0xa3, 0x4c}, {0x37, 0xd4, 0x70, 0x9f}, {0x94, 0xe4, 0x3a, 0x42}, {0xed, 0xa5, 0xa6, 0xbc} };

			RoundFunctions::State block(before);
			block.MixColumns();
			for (int r = 0; r < 4; ++r) {
				for (int c = 0; c < 4; ++c) {
					Assert::AreEqual(after[r][c], block.at(r, c));
				}
			}
		}

		TEST_METHOD(TestAddRoundKey)
		{
			std::vector<uint8_t> input{ 0x32, 0x43, 0xf6, 0xa8, 0x88, 0x5a, 0x30, 0x8d, 0x31, 0x31, 0x98, 0xa2, 0xe0, 0x37, 0x07, 0x34 };
			RoundFunctions::State block(input);
			
			std::vector<uint8_t> key{ 0x2b, 0x7e, 0x15, 0x16, 0x28, 0xae, 0xd2, 0xa6, 0xab, 0xf7, 0x15, 0x88, 0x09, 0xcf, 0x4f, 0x3c };
			KeySchedule sch(key);

			block.AddRoundKey(sch);
			uint8_t expected[4][4] = { {0x19, 0xa0, 0x9a, 0xe9},{0x3d, 0xf4, 0xc6, 0xf8},{0xe3, 0xe2, 0x8d, 0x48},{0xbe, 0x2b, 0x2a, 0x08} };
			for (int r = 0; r < 4; ++r) {
				for (int c = 0; c < 4; ++c) {
					Assert::AreEqual(expected[r][c], block.at(r, c));
				}
			}
		}
	};
}
