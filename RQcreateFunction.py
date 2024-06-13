from numpy.polynomial import Polynomial as P
import statistics as stat
import matplotlib.pyplot as plt
import connection as c
import dictFunctions as df
import tableDataFunctions as tdf
import tableFunctions as tf

### -------------------------- createFunctions.py -------------------------- ###

schemaName = "testSchema"
runsPerInput = 5

#ranges
rowCountRange = [2520*i for i in range(1, 11)]
bddSizeRange = list(range(1, 11))
dictionarySizeRange = [10*i for i in range(1, 1001)]
amountOfPossibilitiesRange = list(range(1, 11))
columnAmountRange = list(range(2, 11))

#default values, set to be the fastest within the lists
r = rowCountRange[0]
b = bddSizeRange[0]
d = dictionarySizeRange[0]
a = amountOfPossibilitiesRange[-1]
v = columnAmountRange[0]

### -------------------------- SETUP -------------------------- ###

def setupDictionary(dictionarySize, amountOfPossibilities):
    conn = c.connect()

    df.dropDictionary(conn, schemaName)
    df.createDictionary(conn, schemaName)
    df.addDictionaryEntries(conn, schemaName, dictionarySize // amountOfPossibilities, amountOfPossibilities)

    conn.commit()
    c.close(conn)

    print("Dictionary setup complete")

def addDictionaryEntries(dictionarySize, amountOfPossibilities):
    conn = c.connect()

    df.addDictionaryEntries(conn, schemaName, dictionarySize // amountOfPossibilities, amountOfPossibilities)

    conn.commit()
    c.close(conn)

def setupTables(columnAmount):
    conn = c.connect()

    tf.drop_table(conn, schemaName, "with2")
    tf.create_table(conn, schemaName, "with2", columnAmount)
    tf.add_column(conn, schemaName, "with2", "probability", "FLOAT")

    tf.drop_table(conn, schemaName, "without")
    tf.create_table(conn, schemaName, "without", columnAmount)

    conn.commit()
    c.close(conn)

def addRows(columnAmount, dictionarySize, amountOfPossibilities, bddSize, rowCount):
    conn = c.connect()

    tdf.insertRowsWithCache(conn, schemaName, "with2", columnAmount, rowCount, dictionarySize // amountOfPossibilities, amountOfPossibilities, bddSize)
    tdf.insertRows(conn, schemaName, "without", columnAmount, rowCount, dictionarySize // amountOfPossibilities, amountOfPossibilities, bddSize)

    conn.commit()
    c.close(conn)

### -------------------------- RUN QUERY -------------------------- ###

def rowCount(withQuery, withoutQuery):
    setupDictionary(d, a)
    setupTables(v)

    conn = c.connect()
    results = []
    for rowCount in rowCountRange:
        addRows(v, d, a, b, rowCountRange[0])
        results.append(runQuery(conn, withQuery, withoutQuery, rowCount))
    conn.close()
    plot_function(results, rowCountRange, "Row count", "Select table")
    return zip(results, rowCountRange)

def bddSize(withQuery, withoutQuery):
    setupDictionary(d, a)

    conn = c.connect()
    results = []
    for bddSize in bddSizeRange:
        setupTables(v)
        addRows(v, d, a, bddSize, r)
        results.append(runQuery(conn, withQuery, withoutQuery, bddSize))
    conn.close()
    plot_function(results, bddSizeRange, "BDD size", "Select table")
    return zip(results, bddSizeRange)

def dictionarySize(withQuery, withoutQuery):
    setupTables(v)
    addRows(v, d, a, b, r)

    conn = c.connect()
    results = []
    for dictionarySize in dictionarySizeRange:
        setupDictionary(dictionarySize, a)
        results.append(runQuery(conn, withQuery, withoutQuery, dictionarySize))
    conn.close()
    plot_function(results, dictionarySizeRange, "Dictionary size", "Select table")
    return zip(results, dictionarySizeRange)

def amountOfPossibilities(withQuery, withoutQuery):
    conn = c.connect()
    results = []
    for amountOfPossibilities in amountOfPossibilitiesRange:
        setupTables(v)
        addRows(v, d, amountOfPossibilities, b, r)
        setupDictionary(d, amountOfPossibilities)
        results.append(runQuery(conn, withQuery, withoutQuery, amountOfPossibilities))
    conn.close()
    plot_logarithmic(results, amountOfPossibilitiesRange, "Amount of possibilities", "Select table")
    return zip(results, amountOfPossibilitiesRange)

def columnAmount(withQuery, withoutQuery):
    setupDictionary(d, a)

    conn = c.connect()
    results = []
    for columnAmount in columnAmountRange:
        setupTables(columnAmount)
        addRows(columnAmount, d, a, b, r)
        results.append(runQuery(conn, withQuery, withoutQuery, columnAmount))
    conn.close()
    plot_function(results, columnAmountRange, "Column amount", "Select table")
    return zip(results, columnAmountRange)

def runQuery(conn, withQuery, withoutQuery, printNumber):
    tempResults = []
    print("Running query: ", printNumber)
    for i in range(runsPerInput):
        print(printNumber, i)
        withCache = withQuery(conn, schemaName, "with2")
        withoutCache = withoutQuery(conn, schemaName, "without")
        tempResults.append(withoutCache - withCache)
        conn.commit()
    return stat.mean(tempResults)

def analyse(results):
    print("Mean: ", stat.mean(results))
    # print("Standard deviation: ", stat.stdev(results))
    print("first value: " + str(results[0]))
    print("last value: " + str(results[-1]))

### -------------------------- PLOTTING -------------------------- ###
def plot_function(results, x_values, xlabel, title):
    plt.plot(x_values, results, label="results")

    polynomial = P.fit(x_values, results, 1) # 1 is the degree of the polynomial
    fx, fy = polynomial.linspace(100)
    analyse(results)
    analyse(fy)
    plt.plot(fx, fy, label = "1st degree")
    plt.xlabel(xlabel)
    plt.ylabel('Milliseconds')
    plt.title(title)
    plt.legend()
    plt.show()

def plot_logarithmic(results, x_values, xlabel, title):
    plot_function(results, x_values, xlabel, title)
    plt.plot(x_values, results, label="results")
    plt.loglog(x_values, results, label="results")

    polynomial = P.fit(x_values, results, 1) # 1 is the degree of the polynomial
    fx, fy = polynomial.linspace(100)
    analyse(results)
    analyse(fy)
    plt.plot(fx, fy, label = "1st degree")
    print()
    plt.xlabel(xlabel)
    plt.ylabel('Milliseconds')
    plt.title(title)
    plt.legend()
    plt.show()
