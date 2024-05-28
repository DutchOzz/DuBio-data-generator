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
rowCountFrank = 25200
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
    tdf.insertRowsWithCache(conn, schemaName, "with", rowCountFrank, dictionarySize // amountOfPossibilities, amountOfPossibilities, bddSize, '&', "Frank")
    # tdf.insertRowsWithCache(conn, schemaName, "with", rowCount-rowCountFrank, dictionarySize // amountOfPossibilities, amountOfPossibilities, bddSize, '&')

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

def plot_function(results):

    # set width of bar 
    barWidth = 0.25
    
    # Set position of bar on X axis 
    br1 = range(1) 
    br2 = [x + barWidth for x in br1]
    br3 = [x + barWidth for x in br2]
    
    # Make the plot
    plt.bar(br1, results[0], color ='r', width = barWidth, 
            edgecolor ='grey', label ='Results without cache') 
    plt.bar(br2, results[1], color ='g', width = barWidth, 
            edgecolor ='grey', label ='Results updating only cache to be updated in table')
    plt.bar(br3, results[2], color ='b', width = barWidth,
            edgecolor ='grey', label ='Results updating all cache in table')
    
    
    # Adding Xticks 
    plt.xlabel('Results', fontweight ='bold', fontsize = 15) 
    plt.ylabel('Time', fontweight ='bold', fontsize = 15) 
    plt.xticks([r + barWidth - 0.125 for r in range(1)], 
            ['Update\nDictionary'])
    plt.legend()
    plt.show() 

def runTests():
    setup()
    results = []
    tempResults = []

    # Update Dictionary
    for i in range(amountOfTests):
        tempResults.append(time_function(qf.updateDictionary, "without", i)) # updateDictionary has another parameter: amountOfPossibilities = 10
    results.append(stat.fmean(tempResults))
    setup()
    for i in range(amountOfTests):
        tempResults.append(time_function(qf.updateDictionaryWithCache, "with", i))
    results.append(stat.fmean(tempResults))
    setup()
    for i in range(amountOfTests):
        tempResults.append(time_function(qf.smartUpdateDictionaryWithCache, "with", i))
    results.append(stat.fmean(tempResults))
    results.append(stat.fmean(tempResults))
    results.append(stat.fmean(tempResults))

    plot_function(results)

runTests()