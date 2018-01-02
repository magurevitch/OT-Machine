from .language import Language
from .phonotactics import Phonotactics
from .assimilation import Assimilation
from .fsa import FSA
from .phonology import Phonology
from .orthography import Orthography
from .underlying_inventory import UnderlyingInventory

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
            string += "Weights: " + str(entry["weight"]) + "\n"
            string += "Response time: " + str(entry["response time"])
        else:
            string += "No surface forms"
    return string

def toXML(entry):
    def helperToXML(entry, indent):
        indentSpaces = indent * " "
        if isinstance(entry, (list,map)):
            between = "</form>\n" + indentSpaces + "<form>"
            return indentSpaces + "<form>" + between.join(entry) + "</form>\n"
        elif isinstance(entry, dict):
            string = ""
            for (key,value) in entry.items():
                string += indentSpaces + "<" + key + ">\n" + helperToXML(value, indent + 1) + indentSpaces + "</" + key + ">\n"
            return string
        return indentSpaces + str(entry) + "\n"
    if "conjugation" in entry:
        return "<conjugationOutput>\n" + helperToXML(entry,1) + "</conjugationOutput>\n"
    else:
        return "<entry>\n" + helperToXML(entry,1) + "</entry>\n"

def makeLanguage(dictionary):
    try:
        if "underlying inventory" in dictionary:
            underlyingInventory = UnderlyingInventory(dictionary["underlying inventory"]["underlying"], dictionary["underlying inventory"]["borrowings"])
        else:
            underlyingInventory = False
        dictPhonotax = dictionary["phonotactics"]
        phonotactics = Phonotactics(
            dictPhonotax["side"],dictPhonotax["placement"],dictPhonotax["foot"],
            FSA.fromRegex(dictPhonotax["unstressed"]),
            FSA.fromRegex(dictPhonotax["primary stress"]),
            FSA.fromRegex(dictPhonotax["secondary stress"]),
            FSA.fromRegex(dictPhonotax["bad edge"]),
            dictPhonotax['can insert'],
            dictPhonotax['can delete']
            )
        harmonies = [Assimilation(entry["lists"],entry["tier"],entry["dissimilation"]) for entry in dictionary["harmonies"]]

        phonology = Phonology(
            underlyingInventory,
            dictionary["categories"],dictionary["insertions"],dictionary["changes"],
            dictionary["undeletables"],phonotactics,dictionary["order"],
            dictionary["geminates"],dictionary["codas"],dictionary["vowels"],
            harmonies,dictionary["bad strings"],dictionary["traces"],dictionary["tambajna finish"]
            )
        
        if "orthographies" in dictionary:
            orthographies = {name:Orthography(ortho) for (name,ortho) in dictionary["orthographies"].items()}
        else:
            orthographies = False
        return Language(phonology,dictionary["conjugations"],orthographies)
    except:
        raise ValueError()

toForm = {
    "String": toString,
    "Verbose String": toVerboseString,
    "XML": toXML
    }