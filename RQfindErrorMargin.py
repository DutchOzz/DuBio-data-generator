import connection as c
import bddFunctions as bf
import dictFunctions as df
import tableDataFunctions as tdf
import tableFunctions as tf
import queryFunctions as qf
import RQcreateFunction as rqf
import numpy as np
import statistics as stat
schemaName = "testSchema"

# -------------- Calculate probabilities -------------- #

# Set base mean
baseMean = 232.4

# queries
withQuery = qf.getCachedProbabilities
withoutQuery = qf.calculateProbabilities
queryRunAmount = 5

# functions
rowCountFunction = lambda b: 0.091 * b + 3.24
dictSizeFunction = lambda b: 2**np.floor(np.log2(b))/7.36 - (0.06175* (b- 2**np.floor(np.log2(b))))
amountOfPossibilitiesFunction = lambda b: 10**(-1.28 * (np.log10((b))) + 2.61) + 229.7
bddSizeFunction = lambda b: 0.7 * b + 229.3
columnAmountFunction = lambda b: baseMean

# # -------------- Update dictionary -------------- #

# # Set base mean
# baseMean = -321

# # queries
# withQuery = qf.getCachedProbabilities
# withoutQuery = qf.calculateProbabilities
# queryRunAmount = 5

# # functions
# rowCountFunction = lambda b: -0.0956484 * b - 11.1659
# dictSizeFunction = lambda b: 2**np.floor(np.log2(b))/-6.94 + (0.0659* (b- 2**np.floor(np.log2(b))))
# amountOfPossibilitiesFunction = lambda b: -334 - 386/b^100 # = 720-334/b^100 + 334 * - 1
# bddSizeFunction = lambda b: baseMean
# columnAmountFunction = lambda b: baseMean


def runQueries(v, d, a, b, r):
    rqf.setupTables(v)
    rqf.addRows(v, d, a, b, r)
    rqf.setupDictionary(d, a)

    conn = c.connect()

    withCache = withQuery(conn, schemaName, "with2")
    withoutCache = withoutQuery(conn, schemaName, "without")
    conn.commit()

    tempResults = []
    for i in range(queryRunAmount):
        withCache = withQuery(conn, schemaName, "with2")
        withoutCache = withoutQuery(conn, schemaName, "without")
        conn.commit()
        tempResults.append(withoutCache - withCache)

    c.close(conn)
    return stat.mean(tempResults)

def runFunctions(v, d, a, b, r):
    timessed = rowCountFunction(r) / baseMean * dictSizeFunction(d) / baseMean * amountOfPossibilitiesFunction(a) / baseMean * bddSizeFunction(b) / baseMean * columnAmountFunction(v) / baseMean
    return baseMean * timessed

def findErrorMargin():
    # Set values
    rList = (10, 50, 100, 500, 1000, 5000, 10000, 50000, 100000)
    b = 1
    dList = (10, 50, 100, 500, 1000)
    aList = (1, 5, 10)
    v = 2
    with open('resultsErrorMargin.txt', 'a') as file:
        file.write("Results for error margin Calculate Probability\n")
        for r in rList:
            for d in dList:     
                for a in aList:
                    print(f"r: {r}, b: {b}, d: {d}, a: {a}")
                    if not (d/a > 17000):
                        file.write(f"r: {r}, b: {b}, d: {d}, a: {a}, v: {v}, function: {runFunctions(v, d, a, b, r)}, result: {runQueries(v, d, a, b, r)}\n")


findErrorMargin()
