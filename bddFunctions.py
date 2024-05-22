import random

def createBdd(size, value, dictSize, combiner):
    variable = 'aaa' # optimisable
    if (size == 1):
        return f"Bdd('({variable}={value})')"
    else:
        bdd = "Bdd('("
        conditions = []

        for i in range(1, size + 1):
            conditions.append(f"{variable}={value}")
            if (i != size):
                variable = incrementVariable(variable, dictSize)

        match combiner:
            case '&':
                bdd += " & ".join(conditions) + ")')"
            case '|':
                bdd += " | ".join(conditions) + ")')"
            case '&!':
                bdd += " & ".join([f"!{condition}" for condition in conditions]) + ")')"
            case '|!':
                bdd += " | ".join([f"!{condition}" for condition in conditions]) + ")')"
        return bdd

def incrementVariable(variable, dictSize):
    ordA = 97
    index = (ord(variable[0]) - ordA) * 26 * 26 + (ord(variable[1]) - ordA) * 26 + ord(variable[2]) - ordA
    index += 1
    return getDictValue(index, dictSize)

def getDictValue(i, dictSize):
    index = i % dictSize
    char = chr(97 + (index // (26*26))) + chr(97 + ((index // 26) % 26)) + chr(97 + (index % 26))
    return char