import matplotlib.pyplot as plt
import statistics as stat
import connection as c
import bddFunctions as bf
import dictFunctions as df
import tableDataFunctions as tdf
import tableFunctions as tf
import queryFunctions as qf

dictionarySize = 1000
rowCount = 2520
schemaName = "testSchema"
runAmount = 1000
amountOfPossibilities = 10

def generalSetup():
    conn = c.connect()

    df.dropDictionary(conn, schemaName)
    df.createDictionary(conn, schemaName)
    df.addDictionaryEntries(conn, schemaName, dictionarySize // amountOfPossibilities, amountOfPossibilities)

    conn.commit()
    c.close(conn)

def setup(bddSize, combiner):
    conn = c.connect()

    tf.drop_table(conn, schemaName, "drives")
    tf.create_table(conn, schemaName, "drives")
    tdf.insertRows(conn, schemaName, "drives", rowCount, dictionarySize // amountOfPossibilities, amountOfPossibilities, bddSize, combiner)

    conn.commit()
    c.close(conn)

def time_function(runNumber, conn):
    time = qf.calculateProbabilities(conn, schemaName, "drives")
    conn.commit()
    print("run#: ", runNumber)
    return time

def plotFunction(results):
    print("Mean: ", stat.mean(results))
    print("Standard Deviation: ", stat.stdev(results))
    plt.hist(results, bins=100)
    plt.xlabel('Milliseconds')
    plt.ylabel('Run Amount')
    plt.title('Function Plot')
    plt.grid(True)
    plt.show()

def runTest():
    generalSetup()
    andResults = []
    orResults = []

    setup(9, '&')
    conn = c.connect()
    for i in range(runAmount):
        andResults.append(time_function(i, conn))
    conn.close()

    setup(9, '|')
    conn = c.connect()
    for i in range(runAmount):
        orResults.append(time_function(i, conn))
    conn.close()

    zipped = zip(andResults, orResults)
    results = [i[0] - i[1] for i in zipped]
    plotFunction(results)
    
runTest()
