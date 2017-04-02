import unittest
from FSA import FSA
from FST import FST
from Phonology import Phonology
from Phonotactics import Phonotactics
from Assimilation import Assimilation
from PriorityQueue import PriorityQueue

class TestAssimilationMethods(unittest.TestCase):
    completelyTransparent = Assimilation([],[])
    hasOpaque = Assimilation([],[])
    
    def localHarmony(self):
        expectedFSA = FSA()
        localHarmony = Assimilation([],False)
        
        actualFSA = localHarmony.harmonyFSA()
        
        self.assertEqual(actualFSA, expectedFSA)
        
class TestFSTMethods(unittest.TestCase):
    def setUp(self):
        unittest.TestCase.setUp(self)
        
class TestFSAMethods(unittest.TestCase):
    def setUp(self):
        unittest.TestCase.setUp(self)
        
class TestPhonologyMethods(unittest.TestCase):
    def setUp(self):
        unittest.TestCase.setUp(self)
        
class TestPhonotacticMethods(unittest.TestCase):
    def setUp(self):
        unittest.TestCase.setUp(self)
        
class TestPriorityQueueMethods(unittest.TestCase):
    def setUp(self):
        unittest.TestCase.setUp(self)

if __name__ == '__main__':
    unittest.main()