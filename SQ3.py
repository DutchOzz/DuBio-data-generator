import matplotlib.pyplot as plt
import connection as c
import bddFunctions as bf
import dictFunctions as df
import tableDataFunctions as tdf
import tableFunctions as tf
import queryFunctions as qf

### -------------------------- SQ3.py -------------------------- ###
# This tests the time taken to calculate the probabilities of a table 
#    with a varying amount of possibilities per variable in the dictionary
# The time taken to calculate the probabilities is measured and plotted against the amount of possibilities

dictionarySize = 2520
rowCount = 2520
schemaName = "testSchema"
maxAmountOfPossilibities = 20
bddSize = 1
runsPerInput = 100

def setup(amountOfPossibilities):
    conn = c.connect()

    df.dropDictionary(conn, schemaName)
    df.createDictionary(conn, schemaName)
    df.addDictionaryEntries(conn, schemaName, dictionarySize // amountOfPossibilities, amountOfPossibilities)

    tf.drop_table(conn, schemaName, "drives")
    tf.create_table(conn, schemaName, "drives")
    tdf.insertRows(conn, schemaName, "drives", rowCount, dictionarySize // amountOfPossibilities, amountOfPossibilities, bddSize)

    conn.commit()
    c.close(conn)

def time_function(input, runNumber):
    conn = c.connect()
    time = qf.calculateProbabilities(conn, schemaName, "drives")
    conn.commit()
    c.close(conn)

    print("input: ", input, "run#: ", runNumber, "time: ", time)
    return time

def plot_function(functionOutputs):
    x_values = range(1, maxAmountOfPossilibities + 1)
    y_values = functionOutputs
    plt.plot(x_values, y_values)
    plt.xlabel('Amount of possibilities')
    plt.ylabel('Milliseconds')
    plt.title('Function Plot')
    plt.grid(True)
    plt.show()

def runTest():
    averageOutputs = []
    for i in range(1, maxAmountOfPossilibities + 1):
        setup(i)
        functionOutputs = []
        for j in range(runsPerInput):
            functionOutputs.append(time_function(i, j))
        averageOutputs.append(sum(functionOutputs) / len(functionOutputs))
    plot_function(averageOutputs)

runTest()