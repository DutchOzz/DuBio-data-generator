import random

def createBdd(size, variable):
    bdd = "Bdd('("
    conditions = []
    for i in range(1, size + 1):
        conditions.append(f"{variable}={i}")
    bdd += " and ".join(conditions) + ")')"
    return bdd

def createBddWithRandomVariables(size, dictSize, dictNumPossibilities):
    bdd = "Bdd('("
    conditions = []
    for i in range(1, size + 1):
        conditions.append(f"{generateRandDictValue(dictSize)}={1}")
    bdd += " and ".join(conditions) + ")')"
    return bdd


def generateRandDictValue(dictSize):
    highestLetterString = chr(97 + (dictSize // (26*26))) + chr(97 + ((dictSize // 26) % 26)) + chr(97 + (dictSize % 26))
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