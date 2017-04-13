import time
import collections

class Language:
    def __init__(self,phono,conjugations):
        self.phono = phono
        self.conjugations = conjugations
        
    def conjugate(self,conj,word):
        response = {"root":word,"conjugation":conj,
                 "forms": collections.OrderedDict([(name,self.entry(form.replace('_',word)))
                        for (name,form) in self.conjugations[conj]])}
        response["response time"] = sum([entry["response time"] for entry in response["forms"].values()])
        response["status"] = all([entry["status"] for entry in response["forms"].values()])
        return response
        
    
    def entry(self,word):
        begin = time.time()
        (weight,surfaceForms) = self.phono.best(word)
        timeToGenerate = time.time() - begin
        
        status = bool(surfaceForms)
        
        return {"underlying":word,"status":status,"weight":weight,
                "response time":timeToGenerate,"surface forms":surfaceForms}