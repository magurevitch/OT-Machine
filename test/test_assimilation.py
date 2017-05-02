import unittest
import sys
sys.path.append('../')

from src.fsa import FSA, FSAEdge
from src.assimilation import Assimilation

class TestAssimilationMethods(unittest.TestCase):
    def test_local_harmony(self):
        states = ['Neutral','p','t','m','n']
        edges = [
            FSAEdge('p','m','m',[]),
            FSAEdge('m','p','p',[]),
            FSAEdge('n','t','t',[]),
            FSAEdge('t','n','n',[]),
            FSAEdge('p','n','n',['harm']),
            FSAEdge('n','p','p',['harm']),
            FSAEdge('p','t','t',['harm']),
            FSAEdge('t','p','p',['harm']),
            FSAEdge('m','n','n',['harm']),
            FSAEdge('n','m','m',['harm']),
            FSAEdge('m','t','t',['harm']),
            FSAEdge('t','m','m',['harm'])
        ]
        expectedFSA = FSA('Neutral',states,states,edges)
        for state in states:
            expectedFSA.addEdge(state,'Neutral','a',[])
            expectedFSA.addEdge(state,state,'_',[])
            expectedFSA.addEdge(state,state,'.',[])
            if state != 'Neutral':
                expectedFSA.addEdge('Neutral',state,state,[])
                expectedFSA.addEdge(state,state,state,[])
        localHarmony = Assimilation([['m','p'],['n','t']],False)
        
        symbols = set(['m','p','n','t','a'])
        actualFSA = localHarmony.harmonyFSA(symbols)
        
        self.assertEqual(actualFSA, expectedFSA, "local harmony is not functioning correctly")
        
    def test_transparent_harmony(self):
        states = ['Neutral','e','i','o','u']
        edges = [
            FSAEdge('u','i','i'),
            FSAEdge('i','u','u'),
            FSAEdge('e','o','o'),
            FSAEdge('o','e','e'),
            FSAEdge('e','i','i',['harm']),
            FSAEdge('i','e','e',['harm']),
            FSAEdge('o','i','i',['harm']),
            FSAEdge('i','o','o',['harm']),
            FSAEdge('e','u','u',['harm']),
            FSAEdge('u','e','e',['harm']),
            FSAEdge('o','u','u',['harm']),
            FSAEdge('u','o','o',['harm'])
        ]
        expectedFSA = FSA('Neutral',states,states,edges)
        for state in states:
            expectedFSA.addEdge(state,state,'a')
            expectedFSA.addEdge(state,state,'_')
            expectedFSA.addEdge(state,state,'.')
            if state != 'Neutral':
                expectedFSA.addEdge('Neutral',state,state,[])
                expectedFSA.addEdge(state,state,state,[])
        transparentHarmony = Assimilation([['i','u'],['e','o']],[])
        
        symbols = set(['a','e','i','o','u'])
        actualFSA = transparentHarmony.harmonyFSA(symbols)
        
        self.assertEqual(actualFSA, expectedFSA, "tiered harmony with only transparents is not functioning correctly")
        
    def test_opaque_harmony(self):
        states = ['Neutral','e','i','o','u']
        edges = [
            FSAEdge('u','i','i'),
            FSAEdge('i','u','u'),
            FSAEdge('e','o','o'),
            FSAEdge('o','e','e'),
            FSAEdge('e','i','i',['harm']),
            FSAEdge('i','e','e',['harm']),
            FSAEdge('o','i','i',['harm']),
            FSAEdge('i','o','o',['harm']),
            FSAEdge('e','u','u',['harm']),
            FSAEdge('u','e','e',['harm']),
            FSAEdge('o','u','u',['harm']),
            FSAEdge('u','o','o',['harm'])
        ]
        expectedFSA = FSA('Neutral',states,states,edges)
        for state in states:
            expectedFSA.addEdge(state,'Neutral','a')
            expectedFSA.addEdge(state,state,'y')
            expectedFSA.addEdge(state,state,'_')
            expectedFSA.addEdge(state,state,'.')
            if state != 'Neutral':
                expectedFSA.addEdge('Neutral',state,state)
                expectedFSA.addEdge(state,state,state)
        opaqueHarmony = Assimilation([['i','u'],['e','o']],['a'])
        
        symbols = set(['a','e','i','o','u','y'])
        actualFSA = opaqueHarmony.harmonyFSA(symbols)
        
        self.assertEqual(actualFSA, expectedFSA, "tiered harmony with opaques is not functioning correctly")
        
    def test_dissimilation_local(self):
        states = ['Neutral','t','d']
        edges = [
            FSAEdge('Neutral','t','t'),
            FSAEdge('Neutral','d','d'),
            FSAEdge('t','d','d',['harm']),
            FSAEdge('d','t','t',['harm']),
            FSAEdge('t','t','t'),
            FSAEdge('d','d','d')
        ]
        expectedFSA = FSA('Neutral',states,states,edges)
        for state in states:
            expectedFSA.addEdge(state,'Neutral','a',[])
            expectedFSA.addEdge(state,state,'_',[])
            expectedFSA.addEdge(state,state,'.',[])
            if state != 'Neutral':
                expectedFSA.addEdge('Neutral',state,state,[])
                expectedFSA.addEdge(state,state,state,[])
        localHarmony = Assimilation([['t','d']],False,True)
        
        symbols = set(['t','d','a'])
        actualFSA = localHarmony.harmonyFSA(symbols)
        
        self.assertEqual(actualFSA, expectedFSA, "local dissimilation is not functioning correctly")
        
    def test_dissimilation_long_distance(self):
        states = ['Neutral','t','d']
        edges = [
            FSAEdge('Neutral','t','t'),
            FSAEdge('Neutral','d','d'),
            FSAEdge('t','d','d',['harm']),
            FSAEdge('d','t','t',['harm']),
            FSAEdge('t','t','t'),
            FSAEdge('d','d','d')
        ]
        expectedFSA = FSA('Neutral',states,states,edges)
        for state in states:
            expectedFSA.addEdge(state,'Neutral','s')
            expectedFSA.addEdge(state,state,'a')
            expectedFSA.addEdge(state,state,'_')
            expectedFSA.addEdge(state,state,'.')
            if state != 'Neutral':
                expectedFSA.addEdge('Neutral',state,state)
                expectedFSA.addEdge(state,state,state)
        opaqueHarmony = Assimilation([['t','d']],['s'],True)
        
        symbols = set(['t','d','a','s'])
        actualFSA = opaqueHarmony.harmonyFSA(symbols)
        
        self.assertEqual(actualFSA, expectedFSA, "tiered dissimilation with opaques is not functioning correctly")
