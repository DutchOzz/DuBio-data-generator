import connection as c
import bddFunctions as bf
import dictFunctions as df
import tableDataFunctions as tdf
import tableFunctions as tf
import queryFunctions as qf

schemaName = "testschema"
columnAmount = 10
dictionarySize = 100
rowCount = 2520
amountOfPossibilities = 10
conn = c.connect()
bddSize = 1

tf.drop_table(conn, schemaName, "with")
tf.create_table(conn, schemaName, "with", columnAmount)
tdf.insertRows(conn, schemaName, "with", columnAmount, rowCount, dictionarySize, amountOfPossibilities, bddSize=bddSize)

conn.commit()
c.close(conn)