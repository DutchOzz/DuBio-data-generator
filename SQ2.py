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

dictionarySize = 1000
rowCount = 2520
schemaName = "testSchema"
maxBDDsize = 10
runsPerSize = 100
amountOfPossibilities = 1

def setup(bddSize):
    conn = c.connect()

    df.dropDictionary(conn, schemaName)
    df.createDictionary(conn, schemaName)
    df.addDictionaryEntries(conn, schemaName, dictionarySize // amountOfPossibilities, amountOfPossibilities)

    tf.drop_table(conn, schemaName, "drives")
    tf.create_table(conn, schemaName, "drives")
    tdf.insertRowsNoRandomness(conn, schemaName, "drives", rowCount, dictionarySize // amountOfPossibilities, amountOfPossibilities, bddSize)

    conn.commit()
    c.close(conn)
