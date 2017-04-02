import time
from FSA import FSA
from Phonology import Phonology
from Phonotactics import Phonotactics
from Assimilation import Assimilation
from Language import Language

cats = {'C':['p','t','k','q','b','d','g','T','K','n','m','N','W','h','f','s','x','Q','r'],'A':['w','y',"j"],'V':['a','e','i','u'],'F':['p','t','k','n','m','N','f','s','x','r'],'P':['p','t','k','q','b','d','g','T','K'],'S':['f','s','x','Q','r']}
ins = {'P':("e","a"),'V':("h","b"),'S':("e","b")}
chgs = {"ai":["aj"],"au":["aw"],"ia":["ja"],"ie":["iy"],"iu":["ju"],"ua":["wa"],"ue":["uy"],"ui":["wi"],"ku":['q'],"xu":['Q'],"Nu":['W'],'b':['mb'],'d':['nd'],'g':['Ng'],'W':['NW']}
undel = "q,T,K"
order = ["harm",'pen',"bs",'del','ins','chg']
geminate = "A+F"
phonotax = Phonotactics("r",2,2,
    FSA.fromRegex("[CV|*C[AV|VA]]"),
    FSA.fromRegex("[CAV*F|AV(F)|{C}[VA*F|V{F}]]"),
    FSA.fromRegex("{C}[AV|V[A|*F]]"),
    False)
codas = {'m':['n'],'n':['m','N'],'N':['n']}
vowels = 'V'
harmonies = [Assimilation([['h'],['r','n','d'],['r','n','t','s','T'],['r','m','b'],['r','m','p','f'],['r','N','g'],['r','N','W','k','q','x','Q','K'],['r','p','t','k','q','T','K','s','f','x','Q']],False)]
badstrings = ["rer","rar","rur","rir"]
conjugations = {'N':
    zip(
        ["Null","Abs","Erg","Gen","SL","DL","Dat","Adj"],
        ["_","_a","_ru","_t","_bi","_KiW","_usa","_fe"]
    )}
    
phono = Phonology(cats,ins,chgs,undel,phonotax,order,geminate,codas,vowels,harmonies,badstrings)
    
lang = Language(phono,conjugations)

print "put in an underlying form to see a surface form, . to finish "
text = raw_input("underlying ")
while text != ".":
    if len(text.strip().split()) == 1:
        begin = time.time()
        best = phono.best(text)
        print "dict", best[0]
        print "surface forms:"
        for ps in best[1]:
            print ps
        print "time to generate: ", time.time() - begin
    else:
        text = text.strip().split()
        lang.conjugate(text[1],text[0])
    text = raw_input("underlying ")