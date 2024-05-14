import random

def createBdd(dict, size):
    bdd = ''
    return bdd


def generateRandDictValue(dict_size):
    highestLetterString = chr(97 + (dict_size // (26*26))) + chr(97 + ((dict_size // 26) % 26)) + chr(97 + (dict_size % 26))
    randString = ''
    sameString = True
    for char in highestLetterString:
        if not sameString:
            randString += chr(random.randint(97, ord('z')))
        else:
            newChar = chr(random.randint(97, ord(char)))
            if char != newChar:
                sameString = False
            randString += newChar
    return randString