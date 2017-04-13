import unittest
from FSA import FSA
from Phonotactics import Phonotactics

class TestPhonotacticMethods(unittest.TestCase):
    def test_syllable_FSA_leftside(self):
        phonotactics = Phonotactics("l",3,2,False,False,False,False)
        
        actualFSA = phonotactics.syllableFSA()
        
    def test_syllable_FSA_bad_edge_left(self):
        phonotactics = Phonotactics("l",1,3,False,False,False,True)
        
        actualFSA = phonotactics.syllableFSA()
    
    def test_syllable_FSA_simple(self):
        phonotactics = Phonotactics("n",3,2,False,False,False,False)
        
        actualFSA = phonotactics.syllableFSA()
        
    def test_syllable_FSA_rightside(self):
        phonotactics = Phonotactics("r",3,2,False,False,False,False)
        
        actualFSA = phonotactics.syllableFSA()
        
    def test_syllable_FSA_bad_edge_right(self):
        phonotactics = Phonotactics("r",1,3,False,False,False,True)
        
        actualFSA = phonotactics.syllableFSA()