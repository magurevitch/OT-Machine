import src.controller as controller

dictionary = {}

print("welcome to my OT machine!")
print("let's first figure out your language")
print("if you want my conlang, write 'Tambajna' and 'harmony' gives a langauge that tests out some things about the machine")
print("if you want your own lang, please use one syllable per phoneme, no _ or .")
text = input("and your categories as symbol : phonemes in that category, one at a time ")
if text == "tambajna":
    file = open("src/tambajna_phonology.txt")
    dictionary = eval(file.read())
    file.close()
elif text == "harmony":
    dictionary["categories"] = {'C':['p', 't', 'k', 'n', 'm'], 'V':['a', 'e', 'i', 'u']}
    dictionary["insertions"] = {}
    dictionary["changes"] = {'pa':['pu'], 'ti':['ta', 'ki']}
    dictionary["undeletables"] = []
    dictionary["order"] = ['pen', 'del', 'ins', "harm", 'chg', "bs"]
    dictionary["geminates"] = []
    dictionary["phonotactics"] = {"side":"None","foot":0,"placement":0,"unstressed":"CV(C)",
                                  "bad edge":False,"primary stress":False,"secondary stress": False,
                                  "can insert": False, "can delete": False}
    dictionary["codas"] = {'m':['n'], 'n':['m'], 't':['p', 'k'], 'p':['t'], 'k':['t']}
    dictionary["vowels"] = ['V']
    dictionary["harmonies"] = [
        {"tier":False,"lists":[['p','m'],['n','t'],['k']],"dissimilation":False},
        {"tier":[],"lists":[['u','i'],['a']],"dissimilation":False}
        ]
    dictionary["bad strings"] = []
    dictionary["traces"] = {}
    dictionary["tambajna finish"] = False
    dictionary["conjugations"] = {}
else:
    print("write next to go onto the next step")
    dictionary["categories"] = {}
    while text != "next":
        new = text.strip().replace(" ","").split(':')
        dictionary["categories"][new[0]] = new[1].replace(" ","").split(',')
        text = input("more? ")
    print("now it is time to say what phonemes can be inserted, with next to continue")
    dictionary["insertions"] = {}
    text = input("write as symbol/category : what to insert, before or after ")
    while text != "next":
        new = text.strip().replace(" ","").split(':')
        dictionary["insertions"][new[0]] = tuple(new[1].replace(" ","").split(',')[0:2])
        text = input("more? ")
    dictionary["changes"] = {}
    text = input("now changes, written as before:after, with ending forms split by comma, next to continue ")
    while text != "next":
        new = text.strip().replace(" ","").split(':')
        dictionary["changes"][new[0]] = new[1].replace(" ","").split(',')
        text = input("more? ")
    dictionary["undeletables"] = input("now phonemes that can't be deleted ")
    print("What traces are left behind by deleting a sound or category of sounds?")
    dictionary["traces"] = {}
    text = raw_input("insert as symbol:trace, with next to continue ")
    while text != "next":
        new = text.strip().replace(" ","").split(':')
        dictionary["traces"][new[0]] = new[1]
        text = raw_input("more? ")
    print("order of (pen)alty, (del)eltion, (ins)ertion, (ch)an(g)e, (harm)ony, and (b)ad (s)tring")
    dictionary["order"] = input("like pen,del,ins,chg,harm,bs ").strip().replace(" ","").split(',')
    dictionary["geminates"] = input("what symbols or categories can be geminated across syllable boundaries to fix things? ")
    dictionary["bad strings"] = input("what strings are considered bad? Separate by commas ").replace(" ","").split(',')
    print("time to make the phonotactics!")
    dictionary["phonotactics"] = {}
    dictionary["phonotactics"]["side"] = input("does it decide stress from the right, left, or none? ")
    if "l" in dictionary["phonotactics"]["side"].lower() or "r" in dictionary["phonotactics"]["side"].lower():
        dictionary["phonotactics"]["placement"] = int(input("what syllable has primary stress? "))
        print("how many unstressed between secondary stressed syllables")
        dictionary["phonotactics"]["foot"] = int(input("or 0 for no secondary stress? "))
        print("each symbol is a phoneme or a category")
        print("now for the syllable structure, with some unique syntax")
        print("* before a symbol means either don't have the symbol or have the thing with a penalty")
        print("# before a symbol means take a penalty")
        print("[sym|sym|sym] means choose between the symbols")
        print("(sym) means have the symbol or not, no penalties")
        print("{sym} means you can have or not have the symbol, and not having gives a penalty")
        print("() and {} can work like [] with the |")
        print("so {C|A}V(V)*C is how syllable structure looks")
        print("writing false means that you don't have that structure, and it uses the next best thing")
        text = input("primary stresed syllables? ")
        dictionary["phonotactics"]["primary stress"] = text.strip() if "false" not in text.lower() else False
        text = input("secondary stressed syllables? ")
        dictionary["phonotactics"]["secondary stress"] = text.strip() if "false" not in text.lower() else False
        text = input("syllables on the hanging edge? ")
        dictionary["phonotactics"]["bad edge"] = text.strip() if "false" not in text.lower() else False
        dictionary["phonotactics"]["unstressed"] = input("necessary: unstressed syllables? ").strip()
        dictionary["phonotactics"]["can insert"] = input("can I have an extra unstressed syllable? ").lower() not in "nofalse"
        dictionary["phonotactics"]["can delete"] = input("can I drop an unstressed syllable? ").lower() not in "nofalse"
    else:
        for element in ["placement","foot","primary stress","secondary stress","bad edge","can insert","can delete"]:
            dictionary["phonotactics"][element] = False
        print("now for the syllable structure, with some unique syntax")
        print("* before a symbol means either don't have the symbol or have the thing with a penalty")
        print("# before a symbol means take a penalty")
        print("[sym|sym|sym] means choose between the symbols")
        print("(sym) means have the symbol or not, no penalties")
        print("{sym} means you can have or not have the symbol, and not having gives a penalty")
        print("() and {} can work like [] with the |")
        print("so {C|A}V(V)*C is how syllable structure looks")
        print("writing false means that you don't have that structure, and it uses the next best thing")
        dictionary["phonotactics"]["unstressed"] = input("syllable structure ").strip()
    print("what changes can be made in the coda?")
    text = input("insert as changes: ")
    dictionary["codas"] = {}
    while text != "next":
        new = text.strip().replace(" ","").split(':')
        dictionary["codas"][new[0]] = new[1].replace(" ","").split(',')
        text = input("more? ")
    dictionary["vowels"] = input("what comes before codas? ").replace(" ","").split(',')
    print("we are now building harmony classes, if any")
    dictionary["harmonies"] = []
    harmdict = {"lists":[],"tier":False}
    print("to finish a harmony class, write done or tier, and if non-opaque things occupy their own tier, and then space and then what is in the tier")
    text = input("next to skip, or type in an assimilation class ")
    while text != "next":
        if "done" in text:
            harmdict["dissimilation"] = input("Is this a dissmilation, as opposed to an assimilation? ").lower() not in "nofalse"
            dictionary["harmonies"] += [harmdict]
            harmdict = {"lists":[],"tier":False}
        elif "tier" in text:
            split = text.replace(" ","").split()
            if len(split) == 1:
                harmdict["tier"] = []
            else:
                harmdict["tier"] = split[1] + [seg for cat in split()[1] for seg in cats[cat] if cat in cats]
            harmdict["dissimilation"] = input("Is this a dissmilation, as opposed to an assimilation? ").lower() not in "nofalse"
            dictionary["harmonies"] += [harmdict]
            harmdict = {"lists":[],"tier":False}
        else:
            harmdict["lists"] += [list(text)]
<<<<<<< HEAD
        text = raw_input("next to skip, or type in an assimilation class ")
    dictionary["tambajna finish"] = False
    print "now put in the conjugations"
=======
        text = input("next to skip, or type in an assimilation class ")
    print("now put in the conjugations")
>>>>>>> forward ported it to python3
    dictionary["conjugations"] = {}
    while text != "next":
        names = input("insert names of conjugations, split by commas ").replace(" ","").split(",")
        forms = input("insert forms  of conjugations, split by commas, corresponding to names, and with _ for where the root goes ").replace(" ","").split(",")
        dictionary["conjugations"][text] = zip(names, forms)
        text = input("next to end, or put in the name of a conjugation")

language = controller.makeLanguage(dictionary)

print("put in an underlying form to see a surface form, . to finish ")
print("use flag -s to show a short string, -x to output xml, and default is a verbose string")
text = input("underlying ")
while text != ".":
    words = text.strip().replace(" ",",").split(',')
    flags = " ".join([word.replace("-","") for word in words if word[0] == '-'])
    words = [word for word in words if word[0] != '-']
    conj = words[0]
    output = 'Verbose String'
    if "s" in flags:
        output = 'String'
    elif "x" in flags:
        output = 'XML'
    genFunction = language.entry
    if conj in language.conjugations:
        genFunction = lambda entry: language.conjugate(conj,entry)
        words = words[1:]
    for word in words:
        entry = genFunction(word)
        print(controller.toForm[output](entry))
    text = input("underlying ")