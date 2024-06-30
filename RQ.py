import queryFunctions as qf
import RQcreateFunction as rq

print(rq.runsPerInput)

def selectTable():
    withQuery = qf.selectTable
    withoutQuery = qf.selectTable
    results = rq.rowCount(withQuery, withoutQuery)
    results2 = rq.bddSize(withQuery, withoutQuery)
    # results3 = rq.dictionarySize(query)
    # results4 = rq.amountOfPossibilities(query)
    # results5 = rq.columnAmount(query)

def calculateProbabilities():
    withQuery = qf.getCachedProbabilities
    withoutQuery = qf.calculateProbabilities

    with open('results.txt', 'a') as file:
    #     # Store results to a file
        # file.write(f"CALCULATE PROBABILITY: \n{rq.runsPerInput} runs\n")
        # results = rq.rowCount(withQuery, withoutQuery)
        # file.write(f"Row count: {list(results)}\n")
        # results2 = rq.bddSize(withQuery, withoutQuery)
        # file.write(f"BDD size: {list(results2)}\n")
        # results3 = rq.dictionarySize(withQuery, withoutQuery)
        # file.write(f"Dictionary size: {list(results3)}\n")
        # results4 = rq.amountOfPossibilities(withQuery, withoutQuery)
        # file.write(f"Amount of possibilities: {list(results4)}\n")
        results5 = rq.columnAmount(withQuery, withoutQuery)
        file.write(f"Column amount: {list(results5)}\n")

    

def updateDictionary():
    withQuery = qf.updateDictionaryWithCache
    withoutQuery = qf.updateDictionary
    with open('results.txt', 'a') as file:
        # Store results to a file
        file.write(f"UPDATE DICTIONARY: \n{rq.runsPerInput} runs\n")
        # results = rq.rowCount(withQuery, withoutQuery)
        # file.write(f"Row count: {list(results)}\n")
        # results2 = rq.bddSize(withQuery, withoutQuery)
        # file.write(f"BDD size: {list(results2)}\n")
        # results3 = rq.dictionarySize(withQuery, withoutQuery)
        # file.write(f"Dictionary size: {list(results3)}\n")
        results4 = rq.amountOfPossibilities(withQuery, withoutQuery)
        file.write(f"Amount of possibilities: {list(results4)}\n")
        # results5 = rq.columnAmount(withQuery, withoutQuery)
        # file.write(f"Column amount: {list(results5)}\n")


def runTests():
    calculateProbabilities()
    # updateDictionary()
    #smartUpdateDictionary()
    # selectTable()

runTests()