from numpy.polynomial import Polynomial as P
import statistics as stat
import matplotlib.pyplot as plt
import connection as c
import bddFunctions as bf
import dictFunctions as df
import tableDataFunctions as tdf
import tableFunctions as tf
import queryFunctions as qf

### -------------------------- createFunctions.py -------------------------- ###

dictionarySize = 1000
rowCount = 252
amountOfTests = 100
schemaName = "testSchema"
amountOfPossibilities = 10
bddSize = 1
runsPerInput = 100

def generalSetup():
    conn = c.connect()

    df.dropDictionary(conn, schemaName)
    df.createDictionary(conn, schemaName)
    df.addDictionaryEntries(conn, schemaName, dictionarySize // amountOfPossibilities, amountOfPossibilities)

    tf.drop_table(conn, schemaName, "with")
    tf.create_table(conn, schemaName, "with")
    tf.add_column(conn, schemaName, "with", "probability", "FLOAT")

    tf.drop_table(conn, schemaName, "without")
    tf.create_table(conn, schemaName, "without")

    conn.commit()
    c.close(conn)


def setup(i):
    conn = c.connect()

    tdf.insertRowsWithCache(conn, schemaName, "with", rowCount, dictionarySize // amountOfPossibilities, amountOfPossibilities, bddSize)
    tdf.insertRows(conn, schemaName, "without", rowCount, dictionarySize // amountOfPossibilities, amountOfPossibilities, bddSize)

    conn.commit()
    c.close(conn)

    print("set up " + str(rowCount * (i+1)) + " rows!")

def time_function(queryfunction, tableName, i, j):
    conn = c.connect()
    time = queryfunction(conn, schemaName, tableName)
    conn.commit()
    c.close(conn)

    print("rowcount = " + str(j) + ", run " + str(i) + ", " + tableName + " = " + str(time))
    return time

def plot_function(results):
    x_values = [rowCount * i for i in range(1, len(results) + 1)]
    plt.plot(x_values, results, label="results")  # plot the original dataset

    polynomial = P.fit(x_values, results, 2) # 2 is the degree of the polynomial
    polynomial2 = P.fit(x_values, results, 1) # 1 is the degree of the polynomial
    print(polynomial)
    print(polynomial2)
    fx, fy = polynomial.linspace(100)  # generate 100 sample points on this graph
    fx2, fy2 = polynomial2.linspace(100)  # generate 100 sample points on this graph
    plt.plot(fx, fy, label="2nd degree")  # plot the calculated polynomial
    plt.plot(fx2, fy2, label = "1st degree")  # plot the calculated polynomial
    plt.xlabel('Amount of rows')
    plt.ylabel('Milliseconds')
    plt.title('Generate function for calculating probability')
    plt.legend()
    plt.show()

def runTest():
    generalSetup()
    results = []

    for i in range(amountOfTests):
        setup(i)
        tempResults = []
        for j in range(runsPerInput):
            withRes = time_function(qf.updateDictionaryWithCache, "with", j, i)
            withoutRes = time_function(qf.updateDictionary, "without", j, i)
            tempResults.append(withoutRes - withRes)
        results.append(stat.mean(tempResults))

    plot_function(results)

runTest()