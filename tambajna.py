import src.controller as controller
import json

file = open("static/tambajna_phonology.txt")
language = controller.makeLanguage(json.loads(file.read()))
file.close()

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
    orthography = "typing" if "t" in flags else False
    if 'b' in flags and conj in language.conjugations:
        words = words[1:]
        for word in words:
            entries = language.bestConjugation(conj,word,orthography,'r' in flags)
            if entries:
                print("Best borrowings of", word)
                for entry in entries:
                    print(controller.toForm[output](entry))
            else:
                print("No way to borrow", word)
    else:
        if conj in language.conjugations:
            words = words[1:]
            genFunction = lambda word: language.conjugate(conj, word, orthography,'r' in flags)
        else:
            genFunction = lambda word: language.entry(word,orthography,'r' in flags,'b' in flags)
        for word in words:
            entry = genFunction(word)
            print(controller.toForm[output](entry))
    text = input("underlying ")