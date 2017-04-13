from Language import Language
from Phonotactics import Phonotactics
from Assimilation import Assimilation
from FSA import FSA
from Phonology import Phonology

def toString(entry):
    string = ""
    if "conjugation" in entry:
        for form in entry["forms"]:
            string += "\n" + form + ":\n"
            string += "  " + toString(entry["forms"][form]).replace("\n","\n  ")
        string = string[1:]
    else:
        if entry["status"]:
            string += "- " + "\n- ".join(entry["surface forms"])
        else:
            string += "No surface forms"
    return string

def toVerboseString(entry):
    if "conjugation" in entry:
        string = "conjugating " + entry["root"]
        string += " as " + entry["conjugation"] + "\n"
        if entry["status"]:
            string += "Forms:"
        else:
            string += "Couldn't get all forms:"
        for form in entry["forms"]:
            string += "\n  " + form + ":\n"
            string += "    " + toVerboseString(entry["forms"][form]).replace("\n","\n    ")
        string += "\ntotal response time: " + str(entry["response time"])
    else:
        string = "Underlying form: " + entry["underlying"] + "\n"
        if entry["status"]:
            string += "Surface forms:\n"
            for form in entry["surface forms"]:
                string += "  - " + form + "\n"
            string += "Weights: " + entry["weight"] + "\n"
            string += "Response time: " + str(entry["response time"])
        else:
            string += "No surface forms"
    return string

def makeLanguage(dictionary):
    
    dictPhonotax = dictionary["phonotactics"]
    phonotactics = Phonotactics(
        dictPhonotax["side"],dictPhonotax["placement"],dictPhonotax["foot"],
        FSA.fromRegex(dictPhonotax["unstressed"]),
        FSA.fromRegex(dictPhonotax["primary stress"]),
        FSA.fromRegex(dictPhonotax["secondary stress"]),
        FSA.fromRegex(dictPhonotax["bad edge"])
        )
    harmonies = [Assimilation(entry["lists"],entry["tier"]) for entry in dictionary["harmonies"]]
    
    phonology = Phonology(
        dictionary["categories"],dictionary["insertions"],dictionary["changes"],
        dictionary["undeletables"],phonotactics,dictionary["order"],
        dictionary["geminates"],dictionary["codas"],dictionary["vowels"],
        harmonies,dictionary["bad strings"]
        )
    
    return Language(phonology,dictionary["conjugations"])

toForm = {
    "String": toString,
    "Verbose String": toVerboseString
    }