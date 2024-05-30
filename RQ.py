from numpy.polynomial import Polynomial as P
import matplotlib.pyplot as plt
import connection as c
import dictFunctions as df
import tableDataFunctions as tdf
import tableFunctions as tf
import queryFunctions as qf
import RQcreateFunction as rq

schemaName = "testSchema"
runsPerInput = 100
rowCountRange = [252*i for i in range(1, 101)]
bddSizeRange = list(range(1, 11))
dictionarySizeRange = [2520*i for i in range(1, 11)]
amountOfPossibilitiesRange = list(range(1, 10))
columnAmountRange = list(range(2, 11))

#default values
r = rowCountRange[0] * 10
b = bddSizeRange[0]
d = dictionarySizeRange[0]
a = 5 #amountOfPossibilities
v = columnAmountRange[0]

def selectTable():
    #rowcount
    rq.setupDictionary(d, a)
    rq.setupTables(v)

    conn = c.connect()
    results = []
    for rowCount in rowCountRange:
        rq.addRows(v, d, a, b, rowCountRange[0])
        withCache = qf.selectTable(conn, schemaName, "with")
        withoutCache = qf.selectTable(conn, schemaName, "without")
        results.append(withoutCache - withCache)
        conn.commit()
    conn.close()
    rq.plot_function(results, rowCountRange, "Row count", "Select table")

    # bddSize
    rq.setupDictionary(d, a)

    conn = c.connect()
    results = []
    for bddSize in bddSizeRange:
        rq.setupTables(v)
        rq.addRows(v, d, a, bddSize, r)
        withCache = qf.selectTable(conn, schemaName, "with")
        withoutCache = qf.selectTable(conn, schemaName, "without")
        results.append(withoutCache - withCache)
        conn.commit()
    conn.close()
    rq.plot_function(results, bddSizeRange, "BDD size", "Select table")

    # dictionarySize
    rq.setupTables(v)
    rq.addRows(v, d, a, b, r)

    conn = c.connect()
    results = []
    for dictionarySize in dictionarySizeRange:
        rq.setupDictionary(dictionarySize, a)
        withCache = qf.selectTable(conn, schemaName, "with")
        withoutCache = qf.selectTable(conn, schemaName, "without")
        results.append(withoutCache - withCache)
        conn.commit()
    conn.close()
    rq.plot_function(results, dictionarySizeRange, "Dictionary size", "Select table")

    # amountOfPossibilities
    rq.setupTables(v)
    rq.addRows(v, d, a, b, r)

    conn = c.connect()
    results = []
    for amountOfPossibilities in amountOfPossibilitiesRange:
        rq.setupDictionary(d, amountOfPossibilities)
        withCache = qf.selectTable(conn, schemaName, "with")
        withoutCache = qf.selectTable(conn, schemaName, "without")
        results.append(withoutCache - withCache)
        conn.commit()
    conn.close()
    rq.plot_function(results, amountOfPossibilitiesRange, "Amount of possibilities", "Select table")

    # columnAmount
    rq.setupDictionary(d, a)
    for columnAmount in columnAmountRange:
        rq.setupTables(columnAmount)
        rq.addRows(columnAmount, d, a, b, r)
        withCache = qf.selectTable(conn, schemaName, "with")
        withoutCache = qf.selectTable(conn, schemaName, "without")
        results.append(withoutCache - withCache)
        conn.commit()
    conn.close()
    rq.plot_function(results, columnAmountRange, "Column amount", "Select table")

def runTests():
    #calculateProbabilities()
    #smartUpdateDictionary()
    selectTable()

runTests()