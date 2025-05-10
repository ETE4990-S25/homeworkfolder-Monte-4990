# run the test outside of Jupyter/ipkernel 

import unittest
from Project import Warrior
class TestWarriorClass(unittest.TestCase):
    def test_add_method_returns_correct_result(self):
         self.assertEqual(Warrior("Anthony", 100).status(), "Anthony is alive!")

if __name__=='__main__': 
   unittest.main()