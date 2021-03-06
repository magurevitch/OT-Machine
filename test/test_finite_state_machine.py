import unittest
import sys
sys.path.append('../')

from src.fsa import FSA, FSAEdge
from src.fst import FST, FSTEdge
from src.weight import Weight

class TestFSTMethods(unittest.TestCase):
    def test_product(self):
        expectedFSA = FSA(0,[0,2,4],[0,1,2,3,4,5],[
            FSAEdge(0,1,'a'),FSAEdge(1,0,'b'),
            FSAEdge(1,2,"",['del']),FSAEdge(0,3,"",['del']),
            FSAEdge(2,3,"",['del']),FSAEdge(3,2,"",['del']),
            FSAEdge(2,5,'c'),FSAEdge(3,4,'d'),
            FSAEdge(4,5,'c'),FSAEdge(5,4,'d')
            ])
        
        productFSA = FSA(0,[0],[0,1],[FSAEdge(0,1,'a'),FSAEdge(1,0,'b')])
        productFST = FST(0,[0,1,2],[0,1,2],[
            FSTEdge(0,0,'a','a'),FSTEdge(0,1,'a',"",['del']),
            FSTEdge(1,1,'a',"",['del']),FSTEdge(1,2,'a','c'),FSTEdge(2,2,'a','c'),
            FSTEdge(0,0,'b','b'),FSTEdge(0,1,'b',"",['del']),
            FSTEdge(1,1,'b',"",['del']),FSTEdge(1,2,'b','d'),FSTEdge(2,2,'b','d'),
            ])
        
        actualFSA = productFST.product(productFSA)
        self.assertTrue(actualFSA.equivalent(expectedFSA), "FST product is not working correctly")
    
    def testSequentialMultiproduct(self):
        fst1 = FST(0,[1],[0,1],[
            FSTEdge(0,0,"a","a"),
            FSTEdge(0,1,"a","b")
            ])
        
        fst2 = FST(0,[1],[0,1],[
            FSTEdge(0,1,"a","z"),
            FSTEdge(0,1,"b","c")
            ])
        
        fst3 = FST(0,[1],[0,1],[
            FSTEdge(0,1,"z","y"),
            FSTEdge(0,1,"c","c"),
            FSTEdge(0,1,"c","d")
                   ])
        
        expectedFst = FST((0,0,0),[(1,1,1)],[(0,0,0),(1,1,1),(0,1,1)],
                          [FSTEdge((0,0,0),(0,1,1),"a","y"),
                           FSTEdge((0,0,0),(1,1,1),"a","c"),
                           FSTEdge((0,0,0),(1,1,1),"a","d")
                           ])
                           
        actualFST = fst1.sequentialMultiproduct([fst2,fst3])
        
        self.assertEqual(actualFST.start,expectedFst.start,"fst sequential multiproduct not doing starts")
        self.assertEqual(actualFST.ends,expectedFst.ends,"fst sequential multiproduct not doing ends")
        self.assertEqual(actualFST.states,expectedFst.states,"fst sequential multiproduct not doing states")
        self.assertEqual(set(actualFST.edges),set(expectedFst.edges),"fst sequential multiproduct not doing edges")
        
class TestFSAMethods(unittest.TestCase):
    def test_determinize(self):
        nfsaEdges = [
            FSAEdge(0,1,""),
            FSAEdge(0,2,'a'),
            FSAEdge(1,0,'a'),
            FSAEdge(2,1,'b'),
            FSAEdge(2,2,""),
            FSAEdge(2,3,""),
            FSAEdge(3,3,'b'),
            FSAEdge(3,4,""),
            FSAEdge(3,5,'b'),
            FSAEdge(4,1,'b'),
            FSAEdge(5,2,'a'),
            FSAEdge(5,2,'b'),
            FSAEdge(5,4,'a'),
            FSAEdge(5,5,'c')
            ]
        nfsa = FSA(0,[2],[0,1,2,3,4,5],nfsaEdges)
        
        expectedEdges = [
            FSAEdge((0,1),(0,1,2,3,4),'a'),
            FSAEdge((0,1,2,3,4),(0,1,2,3,4),'a'),
            FSAEdge((0,1,2,3,4),(1,3,4,5),'b'),
            FSAEdge((1,3,4,5),(0,1,2,3,4),'a'),
            FSAEdge((1,3,4,5),(1,2,3,4,5),'b'),
            FSAEdge((1,3,4,5),(5,),'c'),
            FSAEdge((1,2,3,4,5),(0,1,2,3,4),'a'),
            FSAEdge((1,2,3,4,5),(1,2,3,4,5),'b'),
            FSAEdge((1,2,3,4,5),(5,),'c'),
            FSAEdge((5,),(2,3,4),'a'),
            FSAEdge((5,),(2,3,4),'b'),
            FSAEdge((5,),(5,),'c'),
            FSAEdge((2,3,4),(1,3,4,5),'b')
            ]
        
        expectedFSA = FSA((0,1),
                          [(0,1,2,3,4),(1,2,3,4,5),(2,3,4)],
                          [(0,1),(0,1,2,3,4),(1,3,4,5),(1,2,3,4,5),(5,),(2,3,4)],
                          expectedEdges)
        
        actualFSA = nfsa.determinize()
        
        self.assertEqual(actualFSA.start, expectedFSA.start,
                         "determinizing an FSA start is not working")
        self.assertEqual(
            set(actualFSA.ends), set(expectedFSA.ends),
            "determinizing an FSA ends is not working")
        self.assertEqual(
            set(actualFSA.states), set(expectedFSA.states),
            "determinizing an FSA states is not working")
        self.assertEqual(
            set(actualFSA.edges), set(expectedFSA.edges),
            "determinizing an FSA edges is not working")
        
    def test_equivalent(self):
        fsa1Edges =[
            FSAEdge(0,1,""),
            FSAEdge(0,2,'a'),
            FSAEdge(1,0,'a'),
            FSAEdge(2,1,'b'),
            FSAEdge(2,2,""),
            FSAEdge(2,3,""),
            FSAEdge(3,3,'b'),
            FSAEdge(3,4,""),
            FSAEdge(3,5,'b'),
            FSAEdge(4,1,'b'),
            FSAEdge(5,2,'a'),
            FSAEdge(5,2,'b'),
            FSAEdge(5,4,'a'),
            FSAEdge(5,5,'c')
            ]
        fsa1 = FSA(0,[2],[0,1,2,3,4,5],fsa1Edges)
        
        fsa2Edges = [
            FSAEdge('A','A',""),
            FSAEdge('A','B','a'),
            FSAEdge('B','C','b'),
            FSAEdge('B','H',""),
            FSAEdge('C','B','a'),
            FSAEdge('C','D','b'),
            FSAEdge('C','E','c'),
            FSAEdge('D','B','a'),
            FSAEdge('D','E','c'),
            FSAEdge('D','G',""),
            FSAEdge('E','E','c'),
            FSAEdge('E','F','a'),
            FSAEdge('E','F','b'),
            FSAEdge('F','C','b'),
            FSAEdge('G','D','b'),
            FSAEdge('H','B','a')
            ]
        
        fsa2 = FSA('A',['B','D','F','G'],['A','B','C','D','E','F','G','H'],fsa2Edges)
        
        self.assertTrue(fsa1.equivalent(fsa2), "FSA equivalence is not working")
        self.assertTrue(fsa2.equivalent(fsa1), "FSA equivalence is not symmetrical")
        
    def test_equivalence_false(self):
        fsa1 = FSA(0,[1,2],[0,1,2],
                   [FSAEdge(0,1,'a'),FSAEdge(0,2,'b'),FSAEdge(1,2,'c')])
        fsa2 = FSA(0,[1,2],[0,1,2],
                   [FSAEdge(0,1,'b'),FSAEdge(0,2,'a'),FSAEdge(1,2,'c')])
        
        self.assertFalse(fsa1.equivalent(fsa2), "FSA equivalence is not giving false")
        
    def test_equivalence_different_ends(self):
        fsa1 = FSA(0,[1,2],[0,1,2],
                   [FSAEdge(0,1,'a'),FSAEdge(0,2,'b'),FSAEdge(1,2,'c')])
        fsa2 = FSA(0,[0,2],[0,1,2],
                   [FSAEdge(0,1,'a'),FSAEdge(0,2,'b'),FSAEdge(1,2,'c')])
        
        self.assertFalse(fsa1.equivalent(fsa2), "FSA equivalence is not giving false")
        
        
    def test_product_simple(self):
        fsa1 = FSA(0,[1],[0,1],[FSAEdge(0,1,'a'),FSAEdge(1,0,'b'),
                                FSAEdge(0,0,""),FSAEdge(1,1,"")])
        fsa2 = FSA(0,[3],[0,1,2,3],[])
        for num in range(3):
            for symbol in ['a','b','c']:
                fsa2.addEdge(num,num+1,symbol,[])
            fsa2.addEdge(num,num+1,"",['del'])
        actualFSA = fsa1.product(fsa2)
        symmetricFSA = fsa2.product(fsa1)
        
        expectedFSA = FSA(0,[5],[0,1,2,3,4,5],[
            FSAEdge(0,1,'a'),FSAEdge(0,2,"",['del']),
            FSAEdge(1,3,"",['del']),FSAEdge(1,4,'b'),
            FSAEdge(2,3,'a'),FSAEdge(2,4,"",['del']),
            FSAEdge(4,5,'a'),FSAEdge(3,5,"",['del'])
            ])
        
        self.assertTrue(actualFSA.equivalent(expectedFSA),"simple product is not working")
        self.assertTrue(actualFSA.equivalent(symmetricFSA),"FSA product is not symmetrical")
        self.assertTrue(fsa1.multiproduct([fsa2]).equivalent(expectedFSA), "multiproduct doesn't work")
        
    def test_product_blanks(self):
        fsa1 = FSA(0,[2],[0,1,2],[
            FSAEdge(0,1,"",['pen']),
            FSAEdge(0,2,'b'),
            FSAEdge(1,2,'a'),
            FSAEdge(1,2,'c',['ins'])
            ])
        fsa2 = FSA(0,[2],[0,1,2],[
            FSAEdge(0,1,"",['del']),
            FSAEdge(0,2,'a'),
            FSAEdge(1,2,'b'),
            FSAEdge(1,2,'c',['ins'])
            ])
        for num in range(3):
            fsa1.addEdge(num,num,"")
            fsa2.addEdge(num,num,"")
        
        actualFSA = fsa1.product(fsa2)
        symmetricFSA = fsa2.product(fsa1)
        
        expectedFSA = FSA(0,[4],[0,1,2,3,4],[
            FSAEdge(0,1,"",['del']),FSAEdge(0,2,"",['pen']),
            FSAEdge(2,3,"",['del']),FSAEdge(1,3,"",['pen']),
            FSAEdge(1,4,'b'),FSAEdge(2,4,'a'),
            FSAEdge(3,4,'c',['ins','ins'])
            ])
        for num in range(5):
            expectedFSA.addEdge(num,num,"")
        
        self.assertTrue(actualFSA.equivalent(expectedFSA),"blanks product is not working")
        self.assertTrue(actualFSA.equivalent(symmetricFSA),"FSA product is not symmetrical")
        self.assertTrue(fsa1.multiproduct([fsa2]).equivalent(expectedFSA), "multiproduct doesn't work")
        
    def test_replace(self):
        innerFSA = FSA('A',['B','C'],['A','B','C'],[
            FSAEdge('A','B','b'),FSAEdge('A','C','c'),FSAEdge('B','C','c')
            ])
        outerFSA = FSA(0,[2,3],[0,1,2,3],[
            FSAEdge(0,1,'a'),FSAEdge(1,2,'d'),FSAEdge(1,3,'e')
            ])
        actualFSA = outerFSA.replace(1,innerFSA)
        
        expectedFSA = FSA(0,[4,5],[0,1,2,3,4,5],[
            FSAEdge(0,1,'a'),FSAEdge(1,2,'b'),
            FSAEdge(1,3,'c'),FSAEdge(2,3,'c'),
            FSAEdge(2,4,'d'),FSAEdge(3,4,'d'),
            FSAEdge(2,5,'e'),FSAEdge(3,5,'e')
            ])
        
        self.assertTrue(actualFSA.equivalent(expectedFSA), "FSA replace is not working")
        
    def test_dijkstra(self):
        fsa = FSA(0,[3],[0,1,2,3],[
            FSAEdge(0,1,'a',['pen','pen','pen']),
            FSAEdge(0,2,'b',['pen']),
            FSAEdge(2,1,'c',['pen']),
            FSAEdge(2,3,'d',['pen','pen']),
            FSAEdge(1,3,'e',['pen'])
            ])
        
        (weight,paths) = fsa.dijkstra()
        
        self.assertEqual(weight,Weight(['pen','pen','pen']),"Dijkstra's goes down the correct weights")
        self.assertEqual(set(paths),set(['bce','bd']),"Dijkstra's goes down the correct paths")
        
    def test_from_regex(self):
        expectedFSA = FSA(0,[5],[0,1,2,3,4,5],[
            FSAEdge(0,1,'A'),FSAEdge(0,1,'B'),FSAEdge(0,1,""),
            FSAEdge(1,2,'C'),FSAEdge(1,2,"",['pen']),
            FSAEdge(0,3,'D',['pen']),FSAEdge(0,3,""),
            FSAEdge(3,4,'E'),FSAEdge(4,2,'F',['pen']),
            FSAEdge(2,5,'G')
            ])
        
        actualFSA = FSA.fromRegex("[(A|B){C}|*DE#F]G")
        
        self.assertTrue(actualFSA.equivalent(expectedFSA), "regex to FSA is not working")
        
    def test_traverse(self):
        expectedElements = ["abd","abe","cd","ce","cid","cie"]
        
        fsa = FSA(0,[3,4],[0,1,2,3,4],[])
        fsa.addEdges([
            (0,1,"a"),(1,2,"b"),(0,2,"c"),(2,3,"d"),(2,4,"e"),(2,2,"i")
            ])
        
        actualElements = sorted(fsa.traverse())
        
        self.assertEqual(expectedElements,actualElements,"traverse isn't working correctly")