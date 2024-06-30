import connection as c
import bddFunctions as bf
import dictFunctions as df
import tableDataFunctions as tdf
import tableFunctions as tf
import queryFunctions as qf
import RQcreateFunction as rqf
import numpy as np
import random as rand

schemaName = "testSchema"

# Set values
b = 1
v = 2
aList = (1, 10)
dList = (1, 4)
rList = (1, 4)
queryRunAmount = 8000

def runQueries(r, d, a):
    rqf.setupTables(v)
    rqf.addRows(v, d, a, b, r)
    rqf.setupDictionary(d, a)
    conn = c.connect()
    withCache = qf.getCachedProbabilities(conn, schemaName, "with2")
    withoutCache = qf.calculateProbabilities(conn, schemaName, "without")
    withCache2 = qf.updateDictionaryWithCache(conn, schemaName, "with2", a)
    withoutCache2 = qf.updateDictionary(conn, schemaName, "without", a)

    conn.commit()
    c.close(conn)

    # mistake made, corrected in RQanalyse.py it should be without-with
    return (withCache - withoutCache, withCache2 - withoutCache2)

def runRandom():
    with open("RQcompareRandomVariables.txt", "a") as file:
        for i in range(queryRunAmount):
            print("Run " + str(i))
            a = rand.randint(aList[0], aList[1])
            d = 10**rand.uniform(dList[0], dList[1])
            r = 10**rand.uniform(rList[0], rList[1])
            d -= d % a
            r -= r % a
            print("a = " + str(int(a)) + ", d = " + str(int(d)) + ", r = " + str(int(r)))
            result = runQueries(int(r), int(d), int(a))
            file.write("a=" + str(a) + ",d=" + str(d) + ",r=" + str(r) + ",calProb=" + str(result[0]) + ",updCache=" + str(result[1]) + ",ratio=" + str(result[1] / result[0]) + "\n")
        
runRandom()

