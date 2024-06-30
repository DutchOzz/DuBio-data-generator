import connection as c
import bddFunctions as bf
import dictFunctions as df
import tableDataFunctions as tdf
import tableFunctions as tf
import queryFunctions as qf
import RQcreateFunction as rqf
import numpy as np

schemaName = "testSchema"

# Set values
r = 10
b = 1
d = 10
a = 10
v = 2

# -------------- Calculate probabilities -------------- #

# Set base mean
# baseMean = 232.4

# # queries
withQuery = qf.getCachedProbabilities
withoutQuery = qf.calculateProbabilities
queryRunAmount = 5

# # functions
# rowCountFunction = lambda b: 0.091 * b + 3.24
# dictSizeFunction = lambda b: 2**np.floor(np.log2(b))/7.36 - (0.06175* (b- 2**np.floor(np.log2(b))))
# amountOfPossibilitiesFunction = lambda b: 10**(-1.28 * (np.log10((b))) + 2.61) + 229.7
# bddSizeFunction = lambda b: 0.7 * b + 229.3
# columnAmountFunction = lambda b: baseMean

# -------------- Update dictionary -------------- #

# Set base mean
baseMean = -300

# queries
# withQuery = qf.updateDictionaryWithCache
# withoutQuery = qf.updateDictionary
# queryRunAmount = 5

# functions
rowCountFunction = lambda b: -0.0956484 * b - 11.1659
dictSizeFunction = lambda b: 2**np.floor(np.log2(b))/-6.94 + (0.0659* (b- 2**np.floor(np.log2(b))))
amountOfPossibilitiesFunction = lambda b: -334 - 386/b**100 # = 720-334/b^100 + 334 * - 1
bddSizeFunction = lambda b: baseMean
columnAmountFunction = lambda b: baseMean


def runQueries():
    rqf.setupTables(v)
    rqf.addRows(v, d, a, b, r)
    rqf.setupDictionary(d, a)

    conn = c.connect()
    for i in range(queryRunAmount):
        withCache = withQuery(conn, schemaName, "with2")
        withoutCache = withoutQuery(conn, schemaName, "without")
        conn.commit()
        print("result = " + str(withoutCache - withCache))

    c.close(conn)

def runFunctions():
    print("r: " + str(rowCountFunction(r)))
    print("d: " + str(dictSizeFunction(d)))
    print("a: " + str(amountOfPossibilitiesFunction(a)))
    print("b: " + str(bddSizeFunction(b)))
    print("v: " + str(columnAmountFunction(v)))

    timessed = rowCountFunction(r) / baseMean * dictSizeFunction(d) / baseMean * amountOfPossibilitiesFunction(a) / baseMean * bddSizeFunction(b) / baseMean * columnAmountFunction(v) / baseMean
    print(timessed)
    print(baseMean * timessed)

runQueries()
runFunctions()

