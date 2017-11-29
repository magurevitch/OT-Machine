import time
import collections

class Language:
    def __init__(self,phono,conjugations,orthographies={}):
        self.phono = phono
        self.conjugations = conjugations
        self.orthographies = orthographies
        
    def conjugate(self,conj,word,orthography=False,removeProsody = False):
        response = {"conjugation":conj,
                 "forms": collections.OrderedDict([(name,self.entry(form.replace('_',word),orthography,removeProsody))
                        for (name,form) in self.conjugations[conj]])}
        if orthography:
            response["root"] = self.orthographies[orthography].encode(word)
        else:
            response["root"] = word
        
        response["response time"] = sum([entry["response time"] for entry in response["forms"].values()])
        response["status"] = all([entry["status"] for entry in response["forms"].values()])
        return response

    def findOptions(self, word ,orthography):
        if orthography:
            word = self.orthographies[orthography].decode(word)
        options = self.phono.underlyingInventory.borrow(word).traverse()
        if orthography:
            map(lambda word: self.orthographies[orthography].encode(word), options)
        return options

    def bestConjugation(self,conj,word,orthography=False,removeProsody=False):
        options = self.findOptions(word, orthography)
        conjugated = map(lambda word: self.conjugate(conj, word, orthography, removeProsody),options)
        minWeight = False
        minConjugations = []
        for conjugation in conjugated:
            if conjugation['status']:
                totalWeight = sum([form['weight'] for form in conjugation['forms'].values()],zeroWeight)
                if not(minWeight) or totalWeight < minWeight:
                    minWeight = totalWeight
                    minConjugations = [conjugation]
                elif totalWeight == minWeight:
                    minConjugations += [conjugation]
        if minWeight:
            return minConjugations
        return False
        
    def entry(self,word,orthography = False,removeProsody = False,borrow=False):
        begin = time.time()
        if orthography:
            word = self.orthographies[orthography].decode(word)
        (weight,surfaceForms) = self.phono.best(word,borrow)
        if removeProsody:
            surfaceForms = map(lambda x: x.replace(".","").replace("'","").replace(",",""),surfaceForms)
        if orthography:
            surfaceForms = map(lambda x: self.orthographies[orthography].encode(x),surfaceForms)
        timeToGenerate = time.time() - begin
        
        status = bool(surfaceForms)
        
        if orthography:
            word = self.orthographies[orthography].encode(word)
        
        return {"underlying":word,"status":status,"weight":weight,
                "response time":timeToGenerate,"surface forms":surfaceForms}