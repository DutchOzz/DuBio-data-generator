import time
import matplotlib.pyplot as plt
import connection as c
import bddFunctions as bf
import dictFunctions as df
import tableDataFunctions as tdf
import tableFunctions as tf
import queryFunctions as qf

### -------------------------- showRandomness.py -------------------------- ###
# This tests the time taken to calculate the probabilities of a table
# The time taken to calculate the probabilities is measured and plotted against the run number

dictionarySize = 1000
rowCount = 2520
schemaName = "testSchema"
amountOfTests = 300
amountOfPossibilities = 1
bddSize = 1
randomNess = False

def setup(amountOfPossibilities):
    conn = c.connect()

    df.dropDictionary(conn, schemaName)
    df.createDictionary(conn, schemaName)
    df.addDictionaryEntries(conn, schemaName, dictionarySize // amountOfPossibilities, amountOfPossibilities)

    tf.drop_table(conn, schemaName, "drives")
    tf.create_table(conn, schemaName, "drives")
    tdf.insertRowsNoRandomness(conn, schemaName, "drives", rowCount, dictionarySize // amountOfPossibilities, amountOfPossibilities, bddSize)

    conn.commit()
    c.close(conn)

def time_function():
    conn = c.connect()
    time  = qf.calculateProbabilities(conn, schemaName, "drives")
    conn.commit()
    c.close(conn)

    return time

def plot_function(functionOutputs):
    x_values = range(1, amountOfTests + 1)
    y_values = functionOutputs
    plt.plot(x_values, y_values)
    plt.xlabel('Run')
    plt.ylabel('Seconds')
    plt.title('Function Plot')
    plt.grid(True)
    plt.show()

def runTest():
    functionOutputs = []
    setup(amountOfPossibilities)
    for i in range(1, amountOfTests + 1):
        functionOutputs.append(time_function())
    plot_function(functionOutputs)

runTest()