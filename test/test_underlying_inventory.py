import unittest
import sys
sys.path.append('../')

from src.underlying_inventory import UnderlyingInventory

class TestPhonologyMethods(unittest.TestCase):
    def setUp(self):
        self.ui = UnderlyingInventory(["p","t","f","a","i"],{"k":["t","fa"],"her":["a","pi"],"d":["t"],"r":["t"],"kar":["tap"]})
        
    def tearDown(self):
        del self.ui
        
    def test_borrow(self):
        self.assertEqual(["paf"], sorted(self.ui.borrow("paf").traverse()), "paf not borrowed as  ['paf']")
        self.assertEqual(["a", "pi"], sorted(self.ui.borrow("her").traverse()), "her not borrowed as  ['a', 'pi']")
        self.assertEqual(["tifa", "tit"], sorted(self.ui.borrow("tik").traverse()), "paf not borrowed as  ['tifa', 'tit']")
        self.assertEqual(["fait", "tit"], sorted(self.ui.borrow("kit").traverse()), "paf not borrowed as  ['fait', 'tit']")
        self.assertEqual(["faat", "tap","tat"], sorted(self.ui.borrow("kar").traverse()), "paf not borrowed as  ['faat', 'tap','tat']")
        
        self.assertFalse(self.ui.borrow("er"),"Can borrow er")
        self.assertFalse(self.ui.borrow("tet"),"Can borrow tet")