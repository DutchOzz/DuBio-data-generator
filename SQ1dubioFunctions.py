import matplotlib.pyplot as plt
import statistics as stat
import connection as c
import bddFunctions as bf
import dictFunctions as df
import tableDataFunctions as tdf
import tableFunctions as tf
import queryFunctions as qf

dictionarySize = 1000
rowCount = 25200
schemaName = "testSchema"
amountOfPossibilities = 10 # if this is changed, change Update Dictionary in queryFunctions.py
bddSize = 1
amountOfTests = 30


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

    print("set up!")

def time_function(queryfunction, tableName, i):
    conn = c.connect()
    time = queryfunction(conn, schemaName, tableName)
    conn.commit()
    c.close(conn)

    print("run " + str(i) + ", " + tableName + " = " + str(time))
    return time

def plot_function(withResults, withoutResults):

    # set width of bar 
    barWidth = 0.25
    
    # Set position of bar on X axis 
    br1 = range(len(withResults)) 
    br2 = [x + barWidth for x in br1]
    
    # Make the plot
    plt.bar(br1, withResults, color ='r', width = barWidth, 
            edgecolor ='grey', label ='Results with cache') 
    plt.bar(br2, withoutResults, color ='g', width = barWidth, 
            edgecolor ='grey', label ='Results without cache')
    
    # Adding Xticks 
    plt.xlabel('Results', fontweight ='bold', fontsize = 15) 
    plt.ylabel('Time', fontweight ='bold', fontsize = 15) 
    plt.xticks([r + barWidth - 0.125 for r in range(len(withResults))], 
            ['Calculate\nProbabilities',
             'Update\nDictionary'
             ])
    plt.legend()
    plt.show() 

def runTests():
    setup()
    withoutCacheResults = []
    withCacheResults = []

    tempWithoutCacheResults = []
    tempWithCacheResults = []

    # Calculate Probabilities
    for i in range(amountOfTests):
        withoutCache = time_function(qf.calculateProbabilities, "without", i)
        withCache = time_function(qf.getCachedProbabilities, "with", i)
        tempWithoutCacheResults.append(withoutCache)
        tempWithCacheResults.append(withCache)
    withoutCacheResults.append(stat.fmean(tempWithoutCacheResults))
    withCacheResults.append(stat.fmean(tempWithCacheResults))

    tempWithoutCacheResults = []
    tempWithCacheResults = []

    # Update Dictionary
    for i in range(amountOfTests):
        withoutCache = time_function(qf.updateDictionary, "without", i) # updateDictionary has another parameter: amountOfPossibilities = 10
        withCache = time_function(qf.updateDictionaryWithCache, "with", i) # same here
        tempWithoutCacheResults.append(withoutCache)
        tempWithCacheResults.append(withCache)
    withoutCacheResults.append(stat.fmean(tempWithoutCacheResults))
    withCacheResults.append(stat.fmean(tempWithCacheResults))

    plot_function(withCacheResults, withoutCacheResults)

runTests()