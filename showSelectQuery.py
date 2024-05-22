import matplotlib.pyplot as plt
import statistics as stat
import connection as c
import bddFunctions as bf
import dictFunctions as df
import tableDataFunctions as tdf
import tableFunctions as tf
import queryFunctions as qf

### -------------------------- showSelectQuery.py -------------------------- ###
# This tests the time taken to selct a table with and without cache
# The time taken to select the table is measured and plotted against the amount of rows in the table

dictionarySize = 1000
rowCounts = [2520, 2520*2, 2520*3, 2520*4, 2520*5, 2520*6, 2520*7, 2520*8, 2520*9, 2520*10]
schemaName = "testSchema"
amountOfPossibilities = 10
bddSize = 1
runsPerInput = 200
amountOfTests = 20


def setup(rowCount):
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

def time_function(queryfunction, tableName, i):
    conn = c.connect()
    time = queryfunction(conn, schemaName, tableName)
    conn.commit()
    c.close(conn)
    return time

def analyzeResults(withCacheResults, withoutCacheResults):
    highestDiffMean = 0
    highestDiffMeanIndex = 0
    means = [stat.mean(results) for results in withCacheResults]
    means2 = [stat.mean(results) for results in withoutCacheResults]
    for i in range(1, len(means)):
        diff = abs(means[i] - means2[i])
        if diff > highestDiffMean:
            highestDiffMean = diff
            highestDiffMeanRowCount = rowCounts[i]
    print('The highest difference in means is between cached results and no cached results at rowcount' + 
          str(highestDiffMeanIndex + 1) + ' with a difference of ' + str(highestDiffMean))
    print('meanWithCache[' + str(highestDiffMeanRowCount) + ']: ' + str(means[highestDiffMeanIndex]))
    print('meanNoCache[' + str(highestDiffMeanRowCount) + ']: ' + str(means2[highestDiffMeanIndex]))
    print('standard deviation with Cache[' + str(highestDiffMeanRowCount) + ']: ' + str(stat.stdev(withCacheResults[highestDiffMeanIndex])))
    print('standard deviation no Cache[' + str(highestDiffMeanRowCount) + ']: ' + str(stat.stdev(withoutCacheResults[highestDiffMeanIndex])))
    PSV = (stat.stdev(withCacheResults[highestDiffMeanIndex]) + stat.stdev(withoutCacheResults[highestDiffMeanIndex])) / 2
    print('PSV: ', PSV)


def plot_function(withResults, withoutResults):
    x_values = rowCounts
    plt.plot(x_values, withResults, label='With Cache')
    plt.plot(x_values, withoutResults, label='Without Cache')
    plt.xlabel('Amount of rows')
    plt.ylabel('Milliseconds')
    plt.title('Function Plot')
    plt.grid(True)
    plt.legend()
    plt.show()

def runTests():
    #setup()
    withoutCacheResults = []
    withCacheResults = []

    # Select whole table
    for rowCount in rowCounts:
        setup(rowCount)
        tempWithoutCacheResults = []
        tempWithCacheResults = []
        for i in range(amountOfTests):
            withoutCache = time_function(qf.selectTable, "without", i)
            tempWithoutCacheResults.append(withoutCache)
        print("Without cache: ", stat.fmean(tempWithoutCacheResults))
        for i in range(amountOfTests):
            withCache = time_function(qf.selectTable, "with", i)
            tempWithCacheResults.append(withCache)
        print("With cache: ", stat.fmean(tempWithCacheResults))
        withoutCacheResults.append(stat.fmean(tempWithoutCacheResults))
        withCacheResults.append(stat.fmean(tempWithCacheResults))

    plot_function(withCacheResults, withoutCacheResults)

def runTestAnalyse():
    #setup()
    withoutCacheResults = []
    withCacheResults = []

    # Select whole table
    for rowCount in rowCounts:
        setup(rowCount)
        tempWithoutCacheResults = []
        tempWithCacheResults = []
        for i in range(amountOfTests):
            withoutCache = time_function(qf.selectTable, "without", i)
            tempWithoutCacheResults.append(withoutCache)
        print("Without cache: ", stat.fmean(tempWithoutCacheResults))
        for i in range(amountOfTests):
            withCache = time_function(qf.selectTable, "with", i)
            tempWithCacheResults.append(withCache)
        print("With cache: ", stat.fmean(tempWithCacheResults))
        withoutCacheResults.append(tempWithoutCacheResults)
        withCacheResults.append(tempWithCacheResults)

    print("Analyzing results")
    print("Without cache: ", str(withoutCacheResults))
    print("With cache: ", str(withCacheResults))
    analyzeResults(withoutCacheResults, withCacheResults)
    plot_function([stat.mean(withCacheResults[i]) for i in range(len(withCacheResults))], 
                    [stat.mean(withoutCacheResults[i]) for i in range(len(withoutCacheResults))])

runTestAnalyse()