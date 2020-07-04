#pragma once
#include "RoundFunctions.h"
#include "KeySchedule.h"
#include <iostream>


#include <cstdio>

using namespace RoundFunctions;

void teststate();
void testkeysched();

int main() {
	testkeysched();
	return 0;
}

void testkeysched() {
	uint8_t key[] = { 0x2b, 0x7e, 0x15, 0x16, 0x28, 0xae, 0xd2, 0xa6, 0xab, 0xf7, 0x15, 0x88, 0x09, 0xcf, 0x4f, 0x3c };
	KeySchedule ks(key);
	for (int i = 0; i < 11; ++i) {
		std::cout << ks.next() << " ";
	}
}

void teststate() {

	//State s;
	//int r, c;
	//	//19 a0 9a e9
	//	//3d f4 c6 f8
	//	//e3 e2 8d 48
	//	//be 2b 2a 08
	//uint8_t start[] = { 0x19, 0xa0, 0x9a, 0xe9, 0x3d, 0xf4, 0xc6, 0xf8, 0xe3, 0xe2, 0x8d, 0x48, 0xbe, 0x2b, 0x2a, 0x08 };
	//for (r = 0; r < 4; ++r) {
	//	for (c = 0; c < 4; ++c) {
	//		s.at(r, c) = start[c + (4 * r)];
	//	}
	//}


	//s.SubBytes();
	//s.ShiftRows();
	//s.MixColumns();

	////  04 e0 48 28
	////	66 cb f8 06
	////	81 19 d3 26
	////	e5 9a 7a 4c

	//std::cout << std::hex;
	//for (r = 1; r <= 10; ++r) {
	//	std::cout << Rcon(r) << '\n';
	//}
}