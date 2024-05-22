import connection as c
import bddFunctions as bf
import dictFunctions as df
import tableDataFunctions as tdf
import tableFunctions as tf
import queryFunctions as qf

schemaName = "testschema"
dictionarySize = 100
rowCount = 20
amountOfPossibilities = 10
conn = c.connect()

# df.dropDictionary(conn, schemaName)
# df.createDictionary(conn, schemaName)
# df.addDictionaryEntries(conn, schemaName, dictionarySize // amountOfPossibilities, amountOfPossibilities)

tf.drop_table(conn, schemaName, "drives")
tf.create_table(conn, schemaName, "drives")
tdf.insertRows(conn, schemaName, "drives", rowCount, dictionarySize // amountOfPossibilities, amountOfPossibilities, 5)

conn.commit()
c.close(conn)