import time
import src.controller as controller
from src.FSA import FSA
from src.Phonology import Phonology
from src.Phonotactics import Phonotactics
from src.Assimilation import Assimilation
from src.Language import Language

cats = {'C':['p','t','k','q','b','d','g','T','K','n','m','N','W','h','f','s','x','Q','r'],'A':['w','y',"j"],'V':['a','e','i','u'],'F':['p','t','k','n','m','N','f','s','x','r'],'P':['p','t','k','q','b','d','g','T','K'],'S':['f','s','x','Q','r']}
ins = {'P':("e","a"),'V':("h","b"),'S':("e","b")}
chgs = {"ai":["aj"],"au":["aw"],"ia":["ja"],"ie":["iy"],"iu":["ju"],"ua":["wa"],"ue":["uy"],"ui":["wi"],"ku":['q'],"xu":['Q'],"Nu":['W'],'b':['mb'],'d':['nd'],'g':['Ng'],'W':['NW']}
undel = "q,T,K"
order = ["harm",'pen',"bs",'del','ins','chg']
geminate = "A+F"
phonotax = Phonotactics("r",2,2,
    FSA.fromRegex("[[C|A]V|VA]"),
    FSA.fromRegex("[C[[AV|VA]*F|V{F}]|AV{F|A}]"),
    FSA.fromRegex("[(C)AV|CV[A|*F]]"),
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
    words = text.strip().split()
    if len(words) == 2 and words[0] in lang.conjugations:
            entry = lang.conjugate(words[0],words[1])
            print controller.toVerboseString(entry)
    else:
        for word in words:
            entry = lang.entry(word)
            print controller.toVerboseString(entry)
    text = raw_input("underlying ")