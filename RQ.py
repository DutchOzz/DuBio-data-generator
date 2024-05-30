from numpy.polynomial import Polynomial as P
import matplotlib.pyplot as plt
import connection as c
import dictFunctions as df
import tableDataFunctions as tdf
import tableFunctions as tf
import queryFunctions as qf
import RQcreateFunction as rq

runsPerInput = 100
rowCountRange = [252*i for i in range(1, 101)]
bddSizeRange = list(range(1, 11))
dictionarySizeRange = [2520*i for i in range(1, 11)]
amountOfPossibilitiesRange = list(range(1, 10))
columnAmountRange = list(range(2, 11))

r = rowCountRange[0]
b = bddSizeRange[0]
d = dictionarySizeRange[0]
a = amountOfPossibilitiesRange[0]
v = columnAmountRange[0]

def selectTable():
    results = []
    rq.setupDictionary(d, a)
    conn.commit()
    conn.close()
    rowcount = 2520


    # bddSize
    # dictionarySize
    # amountOfPossibilities
    # columnAmount



def runTests():
    #calculateProbabilities()
    #smartUpdateDictionary()
    selectTable()

# runTests()