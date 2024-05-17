import connection as c
import bddFunctions as bf
import dictFunctions as df
import tableDataFunctions as tdf
import tableFunctions as tf
import queryFunctions as qf

schemaName = "testSchema"
dictionarySize = 10
rowCount = 2000
amountOfPossibilities = 10
conn = c.connect()

df.dropDictionary(conn, schemaName)
df.createDictionary(conn, schemaName)
df.addDictionaryEntries(conn, schemaName, dictionarySize, amountOfPossibilities)

tf.drop_table(conn, schemaName, "drives")
tf.create_table(conn, schemaName, "drives")
tdf.insertRowsRandomBdd(conn, schemaName, "drives", rowCount, dictionarySize, amountOfPossibilities, 1)

qf.calculateProbabilities(conn, schemaName, "drives")

conn.commit()
c.close(conn)