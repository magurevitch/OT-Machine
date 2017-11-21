import unittest
import sys
sys.path.append('../')

from src.orthography import Orthography

class TestOrthographyMethods(unittest.TestCase):
    def setUp(self):
        map = {
            "ng":"N",
            "nng": "NN",
            "ngg": "g",
            "nngg": "Ng",
            "ngl":"h",
            "ok":"uk",
            "not":"nir"
            }
        self.orthography = Orthography(map)
        
    def tearDown(self):
        del self.orthography
        
    def test_decode(self):
        map = {
            "a":"a",
            "n":"n",
            "ng":"N",
            "nng": "NN",
            "ngg": "g",
            "ngl":"h",
            "nngg": "Ng",
            "ok":"uk",
            "not":"nir",
            "no":"no",
            "nok":"nuk",
            "noo":"noo",
            "nong":"noN",
            "nnot":"nnir",
            "nngok":"NNuk",
            "nngl":"NNl",
            "anga":"aNa",
            "annga": "aNNa",
            "angga": "aga",
            "anngga": "aNga",
            "aoka":"auka",
            "anota":"anira",
            "anoa":"anoa"
            }
        for (input,output) in map.items():
            #print(input + " decoding to " + output + ", getting " + self.orthography.decode(input))
            self.assertEqual(output, self.orthography.decode(input), input + " not decoding to " + output)
            
    def test_encode(self):
        map = {
            "a":"a",
            "n":"n",
            "ng":"N",
            "nng": "NN",
            "ngg": "g",
            "nngg": "Ng",
            "ok":"uk",
            "not":"nir",
            "no":"no",
            "nok":"nuk",
            "noo":"noo",
            "nong":"noN",
            "nnot":"nnir",
            "nngok":"NNuk",
            "nngl":"NNl",
            "anga":"aNa",
            "annga": "aNNa",
            "angga": "aga",
            "anngga": "aNga",
            "aoka":"auka",
            "anota":"anira",
            "anoa":"anoa"
            }
        for (input,output) in map.items():
            #print(output + " encoding to " + input + ", getting " + self.orthography.encode(output))
            self.assertEqual(input, self.orthography.encode(output), output + " not encoding to " + input)