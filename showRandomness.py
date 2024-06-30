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

dictionarySize = 2520
rowCount = 2520
columnAmount = 2
schemaName = "testSchema2"
amountOfTests = 300
amountOfPossibilities = 10

bddSize = 1
randomNess = False

def setup():
    conn = c.connect()

    df.dropDictionary(conn, schemaName)
    df.createDictionary(conn, schemaName)
    df.addDictionaryEntries(conn, schemaName, dictionarySize // amountOfPossibilities, amountOfPossibilities)

    tf.drop_table(conn, schemaName, "with2")
    tf.create_table(conn, schemaName, "with2", columnAmount)
    tdf.insertRows(conn, schemaName, "with2", columnAmount, rowCount, dictionarySize // amountOfPossibilities, amountOfPossibilities, bddSize)

    conn.commit()
    c.close(conn)

def time_function():
    conn = c.connect()
    time  = qf.calculateProbabilities(conn, schemaName, "with2")
    conn.commit()
    c.close(conn)

    return time

def plot_function(functionOutputs):
    x_values = range(1, amountOfTests + 1)
    y_values = functionOutputs
    plt.plot(x_values, y_values)
    plt.xlabel('Run')
    plt.ylabel('Milliseconds')
    plt.title('Function Plot')
    plt.grid(True)
    plt.show()

def polt_histogram(functionOutputs):
    plt.hist(functionOutputs, bins=20)
    plt.xlabel('Milliseconds')
    plt.ylabel('Frequency')
    plt.title('Function Plot')
    plt.grid(True)
    plt.show()

def runTest():
    functionOutputs = []
    setup()
    print("set up!")
    for i in range(1, amountOfTests + 1):
        functionOutputs.append(time_function())
        print("run " + str(i) + " done!")
    polt_histogram(functionOutputs)

runTest()