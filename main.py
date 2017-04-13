import time
import src.controller as controller
from src.FSA import FSA
from src.Phonology import Phonology
from src.Phonotactics import Phonotactics
from src.Assimilation import Assimilation
from src.Language import Language

print "welcome to my OT machine!"
print "let's first figure out your language"
print "if you want my conlang-in-progress, write 'default'"
print "if you want your own lang, please use one syllable per phoneme, no _ or ."
text = raw_input("and your categories as symbol : phonemes in that category, one at a time ")
if text == "default":
    cats = {'C':['p', 't', 'k', 'q', 'b', 'd', 'g', 'T', 'K', 'n', 'm', 'N', 'W', 'h', 'f', 's', 'x', 'Q', 'r'], 'A':['w', 'y', "j"], 'V':['a', 'e', 'i', 'u'], 'F':['p', 't', 'k', 'n', 'm', 'N', 'f', 's', 'x', 'r'], 'P':['p', 't', 'k', 'q', 'b', 'd', 'g', 'T', 'K'], 'S':['f', 's', 'x', 'Q', 'r']}
    ins = {'P':("e", "a"), 'V':("h", "b"), 'S':("e", "b")}
    chgs = {"ai":["aj"], "au":["aw"], "ia":["ja"], "ie":["iy"], "iu":["ju"], "ua":["wa"], "ue":["uy"], "ui":["wi"], "ku":['q'], "xu":['Q'], "Nu":['W'], 'b':['mb'], 'd':['nd'], 'g':['Ng'], 'W':['NW']}
    undel = "q,T,K"
    order = ["harm", 'pen', "bs", 'del', 'ins', 'chg']
    geminate = "A+F"
    phonotax = Phonotactics("r",2,2,
                            FSA.fromRegex("[[C|A]V|VA]"),
                            FSA.fromRegex("[C[[AV|VA]*F|V{F}]|AV{F|A}]"),
                            FSA.fromRegex("[(C)AV|CV[A|*F]]"),
                            False)
    codas = {'m':['n'], 'n':['m', 'N'], 'N':['n']}
    vowels = 'V'
    harmonies = [Assimilation([['h'], ['r', 'n', 'd'], ['r', 'n', 't', 's', 'T'], ['r', 'm', 'b'], ['r', 'm', 'p', 'f'], ['r', 'N', 'g'], ['r', 'N', 'W', 'k', 'q', 'x', 'Q', 'K'], ['r', 'p', 't', 'k', 'q', 'T', 'K', 's', 'f', 'x', 'Q']], False)]
    badstrings = ["rer", "rar", "rur", "rir"]
    conjugations = {'N':
        zip(["Null", "Abs", "Erg", "Gen", "SL", "DL", "Dat", "Adj"],
        ["_", "_a", "_ru", "_t", "_bi", "_KiW", "_usa", "_fe"])}
elif text == "harmony":
    cats = {'C':['p', 't', 'k', 'n', 'm'], 'V':['a', 'e', 'i', 'u']}
    ins = {}
    chgs = {'pa':['pu'], 'ti':['ta', 'ki']}
    undel = ""
    order = ['pen', 'del', 'ins', "harm", 'chg', "bs"]
    geminate = ""
    phonotax = Phonotactics("n", 0, 0, FSA.fromRegex("CV(C)"), False, False, False)
    codas = {'m':['n'], 'n':['m'], 't':['p', 'k'], 'p':['t'], 'k':['t']}
    vowels = 'V'
    harmonies = [Assimilation([['p', 'm'], ['n', 't'], ['k']], False), Assimilation([['u', 'i'], ['a']], ['u', 'i','a'])]
    badstrings = False
    conjugations = {}
else:
    print "write next to go onto the next step"
    cats = {}
    while text != "next":
        new = text.strip().split(':')
        cats[new[0]] = new[1].split(',')
        text = raw_input("more? ")
    print "now it is time to say what phonemes can be inserted, with next to continue"
    ins = {}
    text = raw_input("write as symbol/category : what to insert, before or after ")
    while text != "next":
        new = text.strip().split(':')
        new1 = new[1].split(',')
        ins[new[0]] = (new1[0], new1[1])
        text = raw_input("more? ")
    chgs = {}
    text = raw_input("now changes, written as before:after, with ending forms split by comma, next to continue ")
    while text != "next":
        new = text.strip().split(':')
        chgs[new[0]] = new[1].split(',')
        text = raw_input("more? ")
    undel = raw_input("now phonemes that can't be deleted ")
    print "order of (pen)alty, (del)eltion, (ins)ertion, (ch)an(g)e, (harm)ony, and (b)ad (s)tring"
    order = raw_input("like pen,del,ins,chg,harm ").strip().split(',')
    geminate = raw_input("what symbols or categories can be geminated across syllable boundaries to fix things? ")
    badstrings = raw_input("what strings are considered bad? Separate by commas ")
    if "false" in badstrings.lower():
        badstrings = False
    else:
        badstrings = badstrings.split(",")
    print "time to make the phonotactics!"
    side = raw_input("does it decide stress from the right, left, or none? ")
    if "l" in side.lower() or "r" in side.lower():
        place = int(raw_input("what syllable has primary stress? "))
        print "how many unstressed between secondary stressed syllables"
        foot = int(raw_input("or 0 for no secondary stress? "))
        print "each symbol is a phoneme or a category"
        print "now for the syllable structure, with some unique syntax"
        print "* before a symbol means either don't have the symbol or have the thing with a penalty"
        print "# before a symbol means take a penalty"
        print "[sym|sym|sym] means choose between the symbols"
        print "(sym) means have the symbol or not, no penalties"
        print "{sym} means you can have or not have the symbol, and not having gives a penalty"
        print "() and {} can work like [] with the |"
        print "so {C|A}V(V)*C is how syllable structure looks"
        print "writing false means that you don't have that structure, and it uses the next best thing"
        text = raw_input("primary stresed syllables? ")
        psphon = False
        if "false" not in text.lower():
            psphon = FSA.fromRegex(text.strip())
        text = raw_input("secondary stressed syllables? ")
        ssphon = False
        if "false" not in text.lower():
            ssphon = FSA.fromRegex(text.strip())
        text = raw_input("syllables on the hanging edge? ")
        bephon = False
        if "false" not in text.lower():
            bephon = FSA.fromRegex(text.strip())
        usphon = FSA.fromRegex(raw_input("necessary: unstressed syllables? "))
    else:
        place = foot = psphon = ssphon = bephon = False
        print "now for the syllable structure, with some unique syntax"
        print "* before a symbol means either don't have the symbol or have the thing with a penalty"
        print "# before a symbol means take a penalty"
        print "[sym|sym|sym] means choose between the symbols"
        print "(sym) means have the symbol or not, no penalties"
        print "{sym} means you can have or not have the symbol, and not having gives a penalty"
        print "() and {} can work like [] with the |"
        print "so {C|A}V(V)*C is how syllable structure looks"
        print "writing false means that you don't have that structure, and it uses the next best thing"
        usphon = FSA.fromRegex(raw_input("syllable structure? "))
    phonotax = Phonotactics(side, place, foot, usphon, psphon, ssphon, bephon)
    print "what changes can be made in the coda?"
    text = raw_input("insert as changes: ")
    codas = {}
    while text != "next":
        new = text.strip().split(':')
        codas[new[0]] = new[1].split(',')
        text = raw_input("more? ")
    vowels = raw_input("what comes before codas? ")
    print "we are now building harmony classes, if any"
    harmonies = []
    harmclasses = []
    print "to finish a harmony class, write done or tier, and if non-opaque things occupy their own tier, and then space and then what is in the tier"
    text = raw_input("next to skip, or type in an assimilation class ")
    while text != "next":
        if "done" in text:
            harmonies += [Assimilation(harmclasses, False)]
            harmclasses = []
        elif "tier" in text:
            split = text.split()
            if len(split) == 1:
                tier = []
            else:
                tier = split[1] + [seg for cat in split()[1] for seg in cats[cat] if cat in cats]
            harmonies += [Assimilation(harmclasses, tier)]
            harmclasses = []
        else:
            harmclasses += [list(text)]
        text = raw_input("next to skip, or type in an assimilation class ")
    print "now put in the conjugations"
    while text != "next":
        names = raw_input("insert names of conjugations, split by commas ").split(",")
        forms = raw_input("insert forms  of conjugations, split by commas, corresponding to names, and with _ for where the root goes ").split(",")
        conjugations[text] = zip(names, forms)

phono = Phonology(cats, ins, chgs, undel, phonotax, order, geminate, codas, vowels, harmonies, badstrings)
    

print "summarizing:"
phono.prettyprint()

lang = Language(phono, conjugations)

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
