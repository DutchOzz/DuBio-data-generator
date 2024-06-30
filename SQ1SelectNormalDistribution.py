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
bddSize = 1

def setup():
    conn = c.connect()

    df.dropDictionary(conn, schemaName)
    df.createDictionary(conn, schemaName)
    df.addDictionaryEntries(conn, schemaName, dictionarySize // amountOfPossibilities, amountOfPossibilities)

    tf.drop_table(conn, schemaName, "with")
    tf.create_table(conn, schemaName, "with")
    tf.add_column(conn, schemaName, "with", "probability", "FLOAT")
    tdf.insertRowsWithCache(conn, schemaName, "with", rowCount, dictionarySize // amountOfPossibilities, amountOfPossibilities, bddSize)

    tf.drop_table(conn, schemaName, "without")
    tf.create_table(conn, schemaName, "without")
    tdf.insertRows(conn, schemaName, "without", rowCount, dictionarySize // amountOfPossibilities, amountOfPossibilities, bddSize)

    conn.commit()
    c.close(conn)

    print("set up " + str(rowCount) + " rows!")

def time_function(queryfunction, tableName, runNumber, conn):
    time = queryfunction(conn, schemaName, tableName)
    conn.commit()
    print("run#: ", runNumber)
    return time

def plotFunction(results):
    print("Mean: ", stat.mean(results))
    print("Standard Deviation: ", stat.stdev(results))
    plt.hist(results, bins=100)
    plt.xlabel('Milliseconds with - without cache')
    plt.ylabel('Amount of Runs')
    plt.title('Function Plot')
    plt.grid(True)
    plt.show()

def runTest():
    setup()
    withResults = []
    withoutResults = []

    conn = c.connect()
    for i in range(runAmount):
        withResults.append(time_function(qf.selectTable, "with", i, conn))
    conn.close()

    conn = c.connect()
    for i in range(runAmount):
        withoutResults.append(time_function(qf.selectTable, "without", i, conn))
    conn.close()

    zipped = zip(withResults, withoutResults)
    results = [i[0] - i[1] for i in zipped]
    plotFunction(results)
    
runTest()
