# Hack sys.path to get code from the parent folder
import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir) 
# </hack>

from Implementation.KeySchedule import KeySchedule
from Implementation.KeySchedule import DecryptKeySchedule
from Implementation import Constants
import unittest

class TestKeySchedule(unittest.TestCase):
    def test_schedule_init(self):
        # Appendex A.1
        key = [0x2b, 0x7e, 0x15, 0x16, 0x28, 0xae, 0xd2, 0xa6, 0xab, 0xf7, 0x15, 0x88, 0x09, 0xcf, 0x4f, 0x3c]
        schedule = KeySchedule(key)
        
        w0 = 0x2b7e1516 
        k0 = int(schedule.roundKeys[0])
        self.assertEqual(w0, k0, "KeySchedule initialization failed")

        w1 = 0x28aed2a6
        k1 = int(schedule.roundKeys[1])
        self.assertEqual(w1, k1, "KeySchedule initialization failed")
        
        w2 = 0xabf71588 
        k2 = int(schedule.roundKeys[2])
        self.assertEqual(w2, k2, "KeySchedule initialization failed")
        
        w3 = 0x09cf4f3c 
        k3 = int(schedule.roundKeys[3])
        self.assertEqual(w3, k3, "KeySchedule initialization failed")
        
    def test_decrypt_schedule(self):
        key = range(16)
        sch = KeySchedule(key)
        inv = DecryptKeySchedule(key)

        for i in range(Constants.Nr()):
            j = (Constants.Nr() * Constants.Nb()) - (i*4)
            nx = inv.next()
            self.assertEqual([int(k) for k in sch.roundKeys[j:j+4]], [int(k) for k in nx], "Decrypt key schedule was wrong")

    def test_reset(self):
        key = range(0, 32, 2)
        sch = KeySchedule(key)
        initial = sch.next()
        while sch.hasNext():
            sch.next()
        sch.reset()
        self.assertEqual(initial, sch.next(), "KeySchedule's reset failed")

        inv = DecryptKeySchedule(key)
        initial = inv.next()
        while inv.hasNext():
            inv.next()
        inv.reset()
        self.assertEqual(initial, inv.next(), "DecryptKeySchedule's reset failed")

if __name__ == '__main__':
    try:
        unittest.main() 
    except SystemExit:
        # unittest & my IDE don't play nice
        # It raises a SystemExit when it finishes
        pass