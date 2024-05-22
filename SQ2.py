import matplotlib.pyplot as plt
import statistics as stat
import connection as c
import bddFunctions as bf
import dictFunctions as df
import tableDataFunctions as tdf
import tableFunctions as tf
import queryFunctions as qf

### -------------------------- SQ2.py -------------------------- ###
# This tests the time taken to calculate the probabilities of a table 
#    with a varying amount of BDD sizes
# The time taken to calculate the probabilities is measured and plotted against the BDD size
# the BDDS are all constrained to have the variables [aaa, aab, ... , zzz] in that order

dictionarySize = 1000
rowCount = 2520
schemaName = "testSchema"
maxBDDsize = 10
runsPerSize = 1000
amountOfPossibilities = 10
bddCombiners = ['&', '|', '&!', '|!']

def generalSetup():
    conn = c.connect()

    df.dropDictionary(conn, schemaName)
    df.createDictionary(conn, schemaName)
    df.addDictionaryEntries(conn, schemaName, dictionarySize // amountOfPossibilities, amountOfPossibilities)

    conn.commit()
    c.close(conn)

def setup(bddSize, combiner):
    conn = c.connect()

    tf.drop_table(conn, schemaName, "drives")
    tf.create_table(conn, schemaName, "drives")
    tdf.insertRows(conn, schemaName, "drives", rowCount, dictionarySize // amountOfPossibilities, amountOfPossibilities, bddSize, combiner)

    conn.commit()
    c.close(conn)

def time_function(bddSize, runNumber, conn):
    #conn = c.connect()
    time = qf.calculateProbabilities(conn, schemaName, "drives")
    conn.commit()
    #c.close(conn)

    #print("bddSize: ", bddSize, "run#: ", runNumber, "time: ", time)
    return time

def analyzeResults(allResults):
    allMeans = []
    highestDiffMean = 0
    highestDiffMeanIndex = 0
    for combiner in range(len(allResults)):
        means = [stat.mean(results) for results in allResults[combiner]]
        for i in range(1, len(means)):
            for j in range(len(allMeans)):
                diff = abs(means[i] - allMeans[j][i])
                if diff > highestDiffMean:
                    highestDiffMean = diff
                    highestDiffMeanIndex = i
                    highestDiffMeanCombiner1 = combiner
                    highestDiffMeanCombiner2 = j
        allMeans.append(means)
    print('The highest difference in means is between ' + 
          str(highestDiffMeanCombiner1) + ' and ' + str(highestDiffMeanCombiner2) + ' at bdd size ' + 
          str(highestDiffMeanIndex + 1) + ' with a difference of ' + str(highestDiffMean))
    print('mean[' + str(highestDiffMeanCombiner1) + ']: ' + str(allMeans[highestDiffMeanCombiner1][highestDiffMeanIndex]))
    print('mean[' + str(highestDiffMeanCombiner2) + ']: ' + str(allMeans[highestDiffMeanCombiner2][highestDiffMeanIndex]))
    print('standard deviation[' + str(highestDiffMeanCombiner1) + ']: ' + str(stat.stdev(allResults[highestDiffMeanCombiner1][highestDiffMeanIndex])))
    print('standard deviation[' + str(highestDiffMeanCombiner2) + ']: ' + str(stat.stdev(allResults[highestDiffMeanCombiner2][highestDiffMeanIndex])))
    PSV = (stat.stdev(allResults[highestDiffMeanCombiner1][highestDiffMeanIndex]) + stat.stdev(allResults[highestDiffMeanCombiner2][highestDiffMeanIndex])) / 2
    print('PSV: ', PSV)

def plot_function(results1, results2, results3, results4):
    x_values = range(1, maxBDDsize + 1)
    plt.plot(x_values, results1, label='&')
    plt.plot(x_values, results2, label='|')
    plt.plot(x_values, results3, label='not &')
    plt.plot(x_values, results4, label='not |')
    plt.xlabel('BDD Size')
    plt.ylabel('Milliseconds')
    plt.title('Function Plot')
    plt.grid(True)
    plt.legend()
    plt.show()

def runTest():
    generalSetup()
    allResults = []
    for combiner in bddCombiners:
        averageOutputs = []
        for i in range(1, maxBDDsize + 1):
            setup(i, combiner)
            total = 0
            for j in range(1, runsPerSize + 1):
                total += time_function(i, j)
            averageOutputs.append(total/runsPerSize)
        allResults.append(averageOutputs)
    plot_function(allResults[0], allResults[1], allResults[2], allResults[3])

def runTestAnalyse():
    generalSetup()
    allResults = []
    for combiner in bddCombiners:
        print("combiner: ", combiner)
        allOutputs = []
        for i in range(1, maxBDDsize + 1):
            print("bddSize: ", i)
            setup(i, combiner)
            outputs = []
            conn = c.connect()
            for j in range(1, runsPerSize + 1):
                outputs.append(time_function(i, j, conn))
            allOutputs.append(outputs)
            c.close(conn)
        allResults.append(allOutputs)
    analyzeResults(allResults)
    plot_function([stat.mean(allResults[0][i]) for i in range(len(allResults[0]))], 
                  [stat.mean(allResults[1][i]) for i in range(len(allResults[1]))],
                    [stat.mean(allResults[2][i]) for i in range(len(allResults[2]))],
                    [stat.mean(allResults[3][i]) for i in range(len(allResults[3]))])
runTestAnalyse()
