# Hack sys.path to get code from the parent folder
import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir) 
# </hack>

from KeySchedule import KeySchedule
# Appendex A.1
key = 0x2b7e151628aed2a6abf7158809cf4f3c
w0 = 0x2b7e1516 
w1 = 0x28aed2a6
w2 = 0xabf71588 
w3 = 0x09cf4f3c 
schedule = KeySchedule(key)

print("Testing key schedule initialization")
assert int(schedule.roundKeys[0]) == w0, "Expected " + hex(int(w0)) + "; got " + hex(int(schedule.roundKeys[0]))
assert int(schedule.roundKeys[1]) == w1, "Expected " + str(int(w1)) + "; got " + str(int(schedule.roundKeys[1]))
assert int(schedule.roundKeys[2]) == w2, "Expected " + str(int(w2)) + "; got " + str(int(schedule.roundKeys[2]))
assert int(schedule.roundKeys[3]) == w3, "Expected " + str(int(w3)) + "; got " + str(int(schedule.roundKeys[3]))
print("Done")

print("Testing snippets of the keys schedule")
w13 = 0x4716fe3e 
assert int(schedule.roundKeys[13]) == w13, "Expected " + hex(int(w13)) + "; got " + hex(int(schedule.roundKeys[13]))
w24 = 0x6d88a37a
assert int(schedule.roundKeys[24]) == w24, "Expected " + hex(int(w24)) + "; got " + hex(int(schedule.roundKeys[24]))
w43 = 0xb6630ca6
assert int(schedule.roundKeys[43]) == w43, "Expected " + hex(int(w43)) + "; got " + hex(int(schedule.roundKeys[43]))
print("Done")