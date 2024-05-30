from numpy.polynomial import Polynomial as P
import matplotlib.pyplot as plt
import connection as c
import dictFunctions as df
import tableDataFunctions as tdf
import tableFunctions as tf

### -------------------------- createFunctions.py -------------------------- ###

schemaName = "testSchema"

def setupDictionary(dictionarySize, amountOfPossibilities):
    conn = c.connect()

    df.dropDictionary(conn, schemaName)
    df.createDictionary(conn, schemaName)
    df.addDictionaryEntries(conn, schemaName, dictionarySize // amountOfPossibilities, amountOfPossibilities)

    conn.commit()
    c.close(conn)

def addDictionaryEntries(dictionarySize, amountOfPossibilities):
    conn = c.connect()

    df.addDictionaryEntries(conn, schemaName, dictionarySize // amountOfPossibilities, amountOfPossibilities)

    conn.commit()
    c.close(conn)

def setupTables(columnAmount):
    conn = c.connect()

    tf.drop_table(conn, schemaName, "with")
    tf.create_table(conn, schemaName, "with", columnAmount)
    tf.add_column(conn, schemaName, "with", "probability", "FLOAT")

    tf.drop_table(conn, schemaName, "without")
    tf.create_table(conn, schemaName, "without", columnAmount)

    conn.commit()
    c.close(conn)

def addRows(columnAmount, dictionarySize, amountOfPossibilities, bddSize, rowCount):
    conn = c.connect()

    tdf.insertRowsWithCache(conn, schemaName, "with", columnAmount, rowCount, dictionarySize // amountOfPossibilities, amountOfPossibilities, bddSize)
    tdf.insertRows(conn, schemaName, "without", columnAmount, rowCount, dictionarySize // amountOfPossibilities, amountOfPossibilities, bddSize)

    conn.commit()
    c.close(conn)

def plot_function(results, x_values, xlabel, title):
    plt.plot(x_values, results, label="results")

    polynomial = P.fit(x_values, results, 2) # 2 is the degree of the polynomial
    polynomial2 = P.fit(x_values, results, 1)
    fx, fy = polynomial.linspace(100)  # generate 100 sample points on this graph
    fx2, fy2 = polynomial2.linspace(100)
    plt.plot(fx, fy, label="2nd degree")  # plot the calculated polynomial
    plt.plot(fx2, fy2, label = "1st degree")
    print()
    plt.xlabel(xlabel)
    plt.ylabel('Milliseconds')
    plt.title(title)
    plt.legend()
    plt.show()