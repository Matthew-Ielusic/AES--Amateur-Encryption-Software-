
#include "pch.h"
#include "CppUnitTest.h"
#include <vector>

#include "KeySchedule.h"
#include "InverseKeySchedule.h"


using namespace Microsoft::VisualStudio::CppUnitTestFramework;

namespace Tests
{
	TEST_CLASS(KeyScheduleTests)
	{
	public:

		TEST_METHOD(TestKeyScheduleAt)
		{
			std::vector<uint8_t> key = { 0x2b, 0x7e, 0x15, 0x16, 0x28, 0xae, 0xd2, 0xa6, 0xab, 0xf7, 0x15, 0x88, 0x09, 0xcf, 0x4f, 0x3c };
			KeySchedule sched(key);

			Assert::AreEqual((uint32_t)0x2b7e1516, sched.at(0));
			Assert::AreEqual((uint32_t)0xdb0bad00, sched.at(19));
			Assert::AreEqual((uint32_t)0xc9ee2589, sched.at(41));
		}

		TEST_METHOD(TestKeyScheduleNext)
		{
			std::vector<uint8_t> key = { 0x2b, 0x7e, 0x15, 0x16, 0x28, 0xae, 0xd2, 0xa6, 0xab, 0xf7, 0x15, 0x88, 0x09, 0xcf, 0x4f, 0x3c };
			KeySchedule sched(key);

			std::vector<uint32_t> expected{ 0x2b7e1516, 0x28aed2a6, 0xabf71588, 0x09cf4f3c, 0xa0fafe17, 0x88542cb1 };
			for (int i = 0; i < expected.size(); ++i) {
				Assert::AreEqual(expected.at(i), sched.next());
			}
		}


		TEST_METHOD(TestInverseKeyScheduleAt)
		{
			std::vector<uint8_t> key = { 0x2b, 0x7e, 0x15, 0x16, 0x28, 0xae, 0xd2, 0xa6, 0xab, 0xf7, 0x15, 0x88, 0x09, 0xcf, 0x4f, 0x3c };
			KeySchedule sched = InverseKeySchedule(std::vector<uint8_t>(key));

			Assert::AreEqual((uint32_t)0x2b7e1516, sched.at(0));
			Assert::AreEqual((uint32_t)0xdb0bad00, sched.at(19));
			Assert::AreEqual((uint32_t)0xc9ee2589, sched.at(41));
		}


		TEST_METHOD(TestInverseKeyScheduleNext)
		{
			std::vector<uint8_t> key = { 0x2b, 0x7e, 0x15, 0x16, 0x28, 0xae, 0xd2, 0xa6, 0xab, 0xf7, 0x15, 0x88, 0x09, 0xcf, 0x4f, 0x3c };
			KeySchedule sched = InverseKeySchedule(key);

			std::vector<uint32_t> expected{ 0xd014f9a8,  0xc9ee2589, 0xe13f0cc8, 0xb6630ca6};
			for (int i = 0; i < expected.size(); ++i) {
				Assert::AreEqual(expected.at(i), sched.next());
			}
		}
	};
}
