import random

def createBdd(size, variable, value):
    bdd = "Bdd('("
    conditions = []
    for i in range(1, size + 1):
        conditions.append(f"{variable}={value}")
    bdd += " and ".join(conditions) + ")')"
    return bdd

def createBddWithRandomVariables(size, dictSize, dictNumPossibilities):
    bdd = "Bdd('("
    conditions = []
    for i in range(1, size + 1):
        conditions.append(f"{generateRandDictValue(dictSize)}={i%dictNumPossibilities}")
    bdd += " and ".join(conditions) + ")')"
    return bdd

def getDictValue(i, dictSize):
    index = i % dictSize
    char = chr(97 + (index // (26*26))) + chr(97 + ((index // 26) % 26)) + chr(97 + (index % 26))
    return char

def generateRandDictValue(dictSize):
    highestLetterString = chr(97 + (dictSize // (26*26))) + chr(97 + ((dictSize // 26) % 26)) + chr(97 + (dictSize % 26) - 1)
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