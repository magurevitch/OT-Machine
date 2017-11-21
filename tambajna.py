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
    genFunction = language.entry
    if conj in language.conjugations:
        genFunction = lambda entry,orthography,removeProsody: language.conjugate(conj,entry,orthography,removeProsody)
        words = words[1:]
    for word in words:
        entry = genFunction(word,orthography,'r' in flags)
        print(controller.toForm[output](entry))
    text = input("underlying ")