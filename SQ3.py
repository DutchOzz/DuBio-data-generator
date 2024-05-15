import time
import matplotlib.pyplot as plt
import connection as c
import bddFunctions as bf
import dictFunctions as df
import tableDataFunctions as tdf
import tableFunctions as tf
import queryFunctions as qf

dictionarySize = 1000
rowCount = 2520
schemaName = "testSchema"
maxAmountOfPossilibities = 10
bddSize = 1
randomNess = False

def setup(amountOfPossibilities):
    conn = c.connect()

    df.dropDictionary(conn, schemaName)
    df.createDictionary(conn, schemaName)
    df.addDictionaryEntries(conn, schemaName, dictionarySize, amountOfPossibilities)

    tf.drop_table(conn, schemaName, "drives")
    tf.create_table(conn, schemaName, "drives")
    if (randomNess):
        tdf.insertRowsRandomBdd(conn, schemaName, "drives", rowCount, dictionarySize, amountOfPossibilities, bddSize)
    else:
        tdf.insertRowsNoRandomness(conn, schemaName, "drives", rowCount, dictionarySize, amountOfPossibilities, bddSize)

    conn.commit()
    c.close(conn)

def time_function(input):
    start = time.time()

    conn = c.connect()
    qf.calculateProbabilities(conn, schemaName, "drives")
    conn.commit()
    c.close(conn)

    end = time.time()
    length = end - start
    print("input: ", input, "time: ", length)
    return length


def plot_function(functionOutputs):
    x_values = range(1, maxAmountOfPossilibities + 1)
    y_values = functionOutputs
    plt.plot(x_values, y_values)
    plt.xlabel('Input')
    plt.ylabel('Output')
    plt.title('Function Plot')
    plt.grid(True)
    plt.show()

def runTest():
    functionOutputs = []
    for i in range(1, maxAmountOfPossilibities + 1):
        setup(i)
        functionOutputs.append(time_function(i))
    plot_function(functionOutputs)

runTest()