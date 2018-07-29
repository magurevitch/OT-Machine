import unittest
import sys
sys.path.append('../')

from src.fsa import FSA, FSAEdge
from src.phonotactics import Phonotactics

class TestPhonotacticMethods(unittest.TestCase):
    def test_syllable_FSA_leftside(self):
        expectedFSA = FSA(
            "I",
            ["EP","P","U1","U2","S"],
            ["I","B1","B2","EP","P","U1","U2","S"],
            [
                FSAEdge("I","EP",""),
                FSAEdge("I","B1",""),
                FSAEdge("B1","EP","."),
                FSAEdge("B1","B2","."),
                FSAEdge("B2","P","."),
                FSAEdge("P","U1","."),
                FSAEdge("U1","U2","."),
                FSAEdge("U2","S","."),
                FSAEdge("S","U1",".")
            ])
        
        phonotactics = Phonotactics("l",3,2,False,False,False,False,False,False)
        
        actualFSA = phonotactics.syllableFSA()
        
        self.assertTrue(actualFSA.equivalent(expectedFSA), "left side phonotactics not working")
        
    def test_syllable_FSA_bad_edge_left(self):
        expectedFSA = FSA(
            "I",
            ["P","B"],
            ["I","P","B","U1","U2","U3","S"],
            [
                FSAEdge("I","B",""),
                FSAEdge("I","P",""),
                FSAEdge("P","U1","."),
                FSAEdge("U1","U2","."),
                FSAEdge("U2","U3","."),
                FSAEdge("U3","S","."),
                FSAEdge("S","U1",".")
            ])
        for state in expectedFSA.states:
            if state != "I":
                expectedFSA.addEdge(state,"B",".")
        phonotactics = Phonotactics("l",1,3,False,False,False,True,False,False)
        
        actualFSA = phonotactics.syllableFSA()
        self.assertTrue(actualFSA.equivalent(expectedFSA), "left side bad edge phonotactics not working")
        
    def test_syllable_FSA_simple(self):
        expectedFSA = FSA(
            "I",
            ["I"],
            ["I"],
            [FSAEdge("I","I","."),])
        
        phonotactics = Phonotactics("n",3,2,False,False,False,False,False,False)
        
        actualFSA = phonotactics.syllableFSA()
        self.assertTrue(actualFSA.equivalent(expectedFSA), "no side phonotactics not working")
        
        
    def test_syllable_FSA_rightside(self):
        expectedFSA = FSA(
            "I",
            ["F"],
            ["I","P","S","EP","U1","U2","A1","A2"],
            [
                FSAEdge("I","EP",""),
                FSAEdge("I","P",""),
                FSAEdge("I","S",""),
                FSAEdge("I","U1",""),
                FSAEdge("I","U2",""),
                FSAEdge("S","U1","."),
                FSAEdge("U1","U2","."),
                FSAEdge("U2","S","."),
                FSAEdge("U2","P","."),
                FSAEdge("P","A1","."),
                FSAEdge("A1","A2","."),
                FSAEdge("A2","F",""),
                FSAEdge("EP","A2","."),
                FSAEdge("EP","F","")
            ])
        
        phonotactics = Phonotactics("r",3,2,False,False,False,False,False,False)
        
        actualFSA = phonotactics.syllableFSA()
        self.assertTrue(actualFSA.equivalent(expectedFSA), "right side phonotactics not working")
        
    def test_syllable_FSA_bad_edge_right(self):
        expectedFSA = FSA(
            "I",
            ["F"],
            ["I","P","S","U1","U2","U3","B","F"],
            [
                FSAEdge("I","B",""),
                FSAEdge("I","P",""),
                FSAEdge("P","F",""),
                FSAEdge("B","P","."),
                FSAEdge("B","S","."),
                FSAEdge("B","U1","."),
                FSAEdge("B","U2","."),
                FSAEdge("B","U3","."),
                FSAEdge("S","U1","."),
                FSAEdge("U1","U2","."),
                FSAEdge("U2","U3","."),
                FSAEdge("U3","S","."),
                FSAEdge("U3","P",".")
            ])
        
        phonotactics = Phonotactics("r",1,3,False,False,False,True,False,False)
        
        actualFSA = phonotactics.syllableFSA()
        
        self.assertTrue(actualFSA.equivalent(expectedFSA), "right side bad edge phonotactics not working")
        
    def test_syllable_FSA_no_secondary_stress(self):
        expectedFSA = FSA(
            "I",
            ["EP","P","U"],
            ["I","B","EP","P","U"],
            [
                FSAEdge("I","EP",""),
                FSAEdge("I","B",""),
                FSAEdge("B","P","."),
                FSAEdge("P","U","."),
                FSAEdge("U","U",".")
            ])
        
        phonotactics = Phonotactics("l",2,0,False,False,False,False,False,False)
        
        actualFSA = phonotactics.syllableFSA()
        self.assertTrue(actualFSA.equivalent(expectedFSA), "no secondary stress phonotactics not working")
        
    def test_can_delete_primary_stress(self):
        expectedFSA = FSA(
            "I",
            ["EP","P","U"],
            ["I","B","EP","P","U"],
            [
                FSAEdge("I","EP",""),
                FSAEdge("I","B",""),
                FSAEdge("I","P","",["pen"]),
                FSAEdge("B","P","."),
                FSAEdge("P","U","."),
                FSAEdge("U","U",".")
            ])
        
        phonotactics = Phonotactics("l",2,0,False,False,False,False,False,True)
        
        actualFSA = phonotactics.syllableFSA()
        self.assertTrue(actualFSA.equivalent(expectedFSA), "delete only primary phonotactics not working")
        
    def test_can_delete_both_stress_chain(self):
        expectedFSA = FSA(
            "I",
            ["EP","P","U1","U2","S"],
            ["I","EP","B1","B2","P","U1","U2","S"],
            [
                FSAEdge("I","EP",""),
                FSAEdge("I","B1",""),
                FSAEdge("B1","B2","."),
                FSAEdge("B2","P","."),
                FSAEdge("B1","P",".",["pen"]),
                FSAEdge("B1","EP","."),
                FSAEdge("P","U1","."),
                FSAEdge("U1","U2","."),
                FSAEdge("U2","S","."),
                FSAEdge("S","U1","."),
                FSAEdge("U1","S",".",["pen"])
            ])
        
        phonotactics = Phonotactics("l",3,2,False,False,False,False,False,True)
        
        actualFSA = phonotactics.syllableFSA()
        self.assertTrue(actualFSA.equivalent(expectedFSA), "delete both phonotactics not working")
        
    def test_can_delete_both_stress_edgecase(self):
        expectedFSA = FSA(
            "I",
            ["P"],
            ["I","S","U","P"],
            [
                FSAEdge("I","S",""),
                FSAEdge("I","U",""),
                FSAEdge("I","P",""),
                FSAEdge("S","U","."),
                FSAEdge("U","S","."),
                FSAEdge("S","S",".",["pen"]),
                FSAEdge("U","P","."),
                FSAEdge("S","P",".",["pen"])
            ])
        
        phonotactics = Phonotactics("r",1,1,False,False,False,False,False,True)
        
        actualFSA = phonotactics.syllableFSA()
        self.assertTrue(actualFSA.equivalent(expectedFSA), "delete edge case phonotactics not working")
        
    def test_can_insert_primary_stress(self):
        expectedFSA = FSA(
            "I",
            ["EP","P","U"],
            ["I","B","EP","P","U"],
            [
                FSAEdge("I","EP",""),
                FSAEdge("I","B",""),
                FSAEdge("B","B",".",["pen"]),
                FSAEdge("B","P","."),
                FSAEdge("P","U","."),
                FSAEdge("U","U",".")
            ])
        
        phonotactics = Phonotactics("l",2,0,False,False,False,False,True,False)
        
        actualFSA = phonotactics.syllableFSA()
        self.assertTrue(actualFSA.equivalent(expectedFSA), "insert only primary phonotactics not working")
        
    def test_can_insert_both_stress_chain(self):
        expectedFSA = FSA(
            "I",
            ["EP","P","U1","U2","S"],
            ["I","EP","B1","B2","P","U1","U2","S"],
            [
                FSAEdge("I","EP",""),
                FSAEdge("I","B1",""),
                FSAEdge("B1","B2","."),
                FSAEdge("B2","B2",".",["pen"]),
                FSAEdge("B2","P","."),
                FSAEdge("B1","EP","."),
                FSAEdge("P","U1","."),
                FSAEdge("U1","U2","."),
                FSAEdge("U2","U2",".",["pen"]),
                FSAEdge("U2","S","."),
                FSAEdge("S","U1",".")
            ])
        
        phonotactics = Phonotactics("l",3,2,False,False,False,False,True,False)
        
        actualFSA = phonotactics.syllableFSA()
        self.assertTrue(actualFSA.equivalent(expectedFSA), "insert both phonotactics not working")
        
    def test_can_insert_both_stress_edgecase(self):
        expectedFSA = FSA(
            "I",
            ["F"],
            ["I","S","U","P","A","F"],
            [
                FSAEdge("I","S",""),
                FSAEdge("I","U",""),
                FSAEdge("I","P",""),
                FSAEdge("S","U","."),
                FSAEdge("U","U",".",["pen"]),
                FSAEdge("U","S","."),
                FSAEdge("U","P","."),
                FSAEdge("P","F",""),
                FSAEdge("A","F",""),
                FSAEdge("P","A",".",["pen"]),
                FSAEdge("A","A",".",["pen"])
            ])
        
        phonotactics = Phonotactics("r",1,1,False,False,False,False,True,False)
        
        actualFSA = phonotactics.syllableFSA()
        self.assertTrue(actualFSA.equivalent(expectedFSA), "insert edge case phonotactics not working")
        
        
    def test_can_insert_and_delete_both_stress_edgecase(self):
        expectedFSA = FSA(
            "I",
            ["F"],
            ["I","S","U","P","A","F"],
            [
                FSAEdge("I","S",""),
                FSAEdge("I","U",""),
                FSAEdge("I","P",""),
                FSAEdge("S","U","."),
                FSAEdge("U","U",".",["pen"]),
                FSAEdge("U","S","."),
                FSAEdge("U","P","."),
                FSAEdge("P","F",""),
                FSAEdge("A","F",""),
                FSAEdge("P","A",".",["pen"]),
                FSAEdge("A","A",".",["pen"]),
                FSAEdge("S","S",".",["pen"]),
                FSAEdge("S","P",".",["pen"])
            ])

        phonotactics = Phonotactics("r",1,1,False,False,False,False,True,True)
        
        actualFSA = phonotactics.syllableFSA()
        
        self.assertTrue(actualFSA.equivalent(expectedFSA), "insert and delete edge case phonotactics not working")
        