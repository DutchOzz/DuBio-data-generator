import connection as c
import bddFunctions as bf
import dictFunctions as df
import tableDataFunctions as tdf
import tableFunctions as tf
import queryFunctions as qf

schemaName = "testschema"
dictionarySize = 100
rowCount = 2520
amountOfPossibilities = 10
conn = c.connect()
bddSize = 1
rowCountFrank = 10

df.dropDictionary(conn, schemaName)
df.createDictionary(conn, schemaName)
df.addDictionaryEntries(conn, schemaName, dictionarySize // amountOfPossibilities, amountOfPossibilities)

tf.drop_table(conn, schemaName, "with")
tf.create_table(conn, schemaName, "with")
tf.add_column(conn, schemaName, "with", "probability", "FLOAT")
tdf.insertRowsWithCache(conn, schemaName, "with", rowCountFrank, dictionarySize // amountOfPossibilities, amountOfPossibilities, bddSize, '&', "Frank")
tdf.insertRowsWithCache(conn, schemaName, "with", rowCount-rowCountFrank, dictionarySize // amountOfPossibilities, amountOfPossibilities, bddSize, '&')

conn.commit()
qf.smartUpdateDictionaryWithCache(conn, schemaName, "with")
conn.commit()
c.close(conn)