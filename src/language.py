import time
import collections

class Language:
    def __init__(self,phono,conjugations,orthographies={}):
        self.phono = phono
        self.conjugations = conjugations
        self.orthographies = orthographies
        
    def conjugate(self,conj,word,orthography=False,removeProsody = False):
        response = {"root":word,"conjugation":conj,
                 "forms": collections.OrderedDict([(name,self.entry(form.replace('_',word),orthography,removeProsody))
                        for (name,form) in self.conjugations[conj]])}
        response["response time"] = sum([entry["response time"] for entry in response["forms"].values()])
        response["status"] = all([entry["status"] for entry in response["forms"].values()])
        return response
        
    def entry(self,word,orthography = False,removeProsody = False):
        begin = time.time()
        if orthography:
            word = self.orthographies[orthography].decode(word)
        (weight,surfaceForms) = self.phono.best(word)
        if removeProsody:
            surfaceForms = map(lambda x: x.replace(".","").replace("'","").replace(",",""),surfaceForms)
        if orthography:
            surfaceForms = map(lambda x: self.orthographies[orthography].encode(x),surfaceForms)
        timeToGenerate = time.time() - begin
        
        status = bool(surfaceForms)
        
        return {"underlying":word,"status":status,"weight":weight,
                "response time":timeToGenerate,"surface forms":surfaceForms}