import unittest
import sys
sys.path.append('../')

from src.fsa import FSA, FSAEdge
from src.fst import FST, FSTEdge
from src.phonology import Phonology
from src.phonotactics import Phonotactics

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
        traces = {"C":"H"}
        self.phonology = Phonology(categories,inserts,changes,undel,phonotax,order,geminate,codas,vowels,harmonies,badstrings,traces,False)
        
    def tearDown(self):
        del self.phonology
        
    #def test_modification_FST(self):
    #    expectedFST = FST(0,[0],[0],[])
    #    actualFST = self.phonology.modificationFST()
        
        #self.assertEqual(actualFST, expectedFST, "modification FST isn't working correctly")
        
    def test_codas(self):
        expectedFST = FST('B',['A','E'],['A','B','E'],[
            FSTEdge('A','B','.','.'),
            FSTEdge('A','E','.',""),
            FSTEdge('A','E','.',"H"),
            FSTEdge('A','A','f','p',["chg"]),
            FSTEdge('A','A','t','f',["chg"]),
            FSTEdge('A','A','t','p',["chg"]),
            ])
        for letter in ["f","t","p","a","i","'","",",","H"]:
            expectedFST.addEdge('A','A',letter,letter)
            if letter in "ai":
                expectedFST.addEdge('B','A',letter,letter)
            else:
                expectedFST.addEdge('B','B',letter,letter)
        
        actualFST = self.phonology.codasFST()
                
        self.assertEqual(actualFST, expectedFST, "codas FST isn't working correctly")
        
    def test_bad_strings(self):
        expectedFSA = FSA(0,['A','P','T','N'],['A','P','T','N',0],[
            FSAEdge(0,0,"H"),FSAEdge(0,0,""),
            FSAEdge(0,'N','f'),FSAEdge(0,'N','i'),FSAEdge(0,'N',','),FSAEdge(0,'N','.'),FSAEdge(0,'N',"'"),
            FSAEdge(0,'A','a'),FSAEdge(0,'T','t'),FSAEdge(0,'P','p'),
            FSAEdge('N','N','f'),FSAEdge('N','N','i'),
            FSAEdge('N','A','a'),FSAEdge('N','T','t'),FSAEdge('N','P','p'),
            FSAEdge('T','T','t'),FSAEdge('T','N','f'),FSAEdge('T','N','i'),
            FSAEdge('T','P','p'),FSAEdge('T','A','a',["bs"]),
            FSAEdge('P','P','p'),FSAEdge('P','N','f'),FSAEdge('P','N','i',["bs"]),
            FSAEdge('P','A','a'),FSAEdge('P','T','t'),
            FSAEdge('A','A','a'),FSAEdge('A','N','i'),
            FSAEdge('A','T','t',["bs"]),FSAEdge('A','T','f'),
            FSAEdge('A','P','p')
            ])
        for state in ['A','P','T','N']:
            expectedFSA.addEdge(state,state,'.')
            expectedFSA.addEdge(state,state,',')
            expectedFSA.addEdge(state,state,"'")
            expectedFSA.addEdge(state,state,"H")
            expectedFSA.addEdge(state,state,"")
        
        actualFSA = self.phonology.badStrings()

        self.assertTrue(actualFSA.equivalent(expectedFSA), "badStrings FSA isn't working correctly")