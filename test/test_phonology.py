import unittest
import sys
sys.path.append('../')

from src.FSA import FSA
from src.FST import FST
from src.Phonology import Phonology
from src.Phonotactics import Phonotactics
from src.FSTEdge import FSTEdge
from src.FSAEdge import FSAEdge

class TestPhonologyMethods(unittest.TestCase):
    def setUp(self):
        categories = {'C':['p','t','f'],'V':['a','i']}
        inserts = {'V':('t','b'),'C':('i','a')}
        changes = {"fi":["fa","pi"]}
        undel = ['t','i']
        phonotax = Phonotactics("n", 0, 0, False, False, False, False,False,False)
        order = ["harm",'pen',"bs",'del','ins','chg']
        geminate = "V"
        codas = {'f':['p'],'t':['p','f']}
        vowels = 'V'
        harmonies = []
        badstrings = ["afa","at","ta","pi"]
        self.phonology = Phonology(categories,inserts,changes,undel,phonotax,order,geminate,codas,vowels,harmonies,badstrings)
        
    def tearDown(self):
        del self.phonology
        
    def test_modification_FST(self):
        expectedFST = FST(0,[0],[0],[])
        actualFST = self.phonology.modificationFST()
        
        #self.assertEqual(actualFST, expectedFST, "modification FST isn't working correctly")
        
    def test_codas(self):
        expectedFST = FST('B',['A','E'],['A','B','E'],[
            FSTEdge('A','B','.','.',[]),
            FSTEdge('A','E','.','_',[]),
            FSTEdge('A','A','f','p',["chg"]),
            FSTEdge('A','A','t','f',["chg"]),
            FSTEdge('A','A','t','p',["chg"]),
            ])
        for letter in "ftpai_":
            expectedFST.addEdge('A','A',letter,letter,[])
            if letter in "ai":
                expectedFST.addEdge('B','A',letter,letter,[])
            else:
                expectedFST.addEdge('B','B',letter,letter,[])
        
        actualFST = self.phonology.codasFST()
        
        self.assertEqual(actualFST, expectedFST, "codas FST isn't working correctly")
        
    def test_bad_strings(self):
        expectedFSA = FSA(0,[0,'A','P','T','F'],[0,'A','P','T','F'],[
            FSAEdge(0,'A','a'),FSAEdge(0,0,'f'),FSAEdge(0,0,'i'),
            FSAEdge(0,'P','p'),FSAEdge(0,'T','t'),
            FSAEdge('A','A','a'),FSAEdge('A','F','f'),FSAEdge('A',0,'i'),
            FSAEdge('A','P','p'),FSAEdge('A','T','t',['bs']),
            FSAEdge('F','A','a',['bs']),FSAEdge('F',0,'f'),FSAEdge('F',0,'i'),
            FSAEdge('F','P','p'),FSAEdge('F','T','t'),
            FSAEdge('T','A','a',['bs']),FSAEdge('T',0,'f'),FSAEdge('T',0,'i'),
            FSAEdge('T','P','p'),FSAEdge('T','T','t'),
            FSAEdge('P','A','a'),FSAEdge('P',0,'f'),FSAEdge('P',0,'i',['bs']),
            FSAEdge('P','P','p'),FSAEdge('P','T','t'),
            ])
        for state in expectedFSA.states:
            expectedFSA.addEdge(state,state,'.')
        
        actualFSA = self.phonology.badStrings()
        
        actualFSA.relabelStates()

        self.assertTrue(actualFSA.equivalent(expectedFSA), "badStrings FSA isn't working correctly")